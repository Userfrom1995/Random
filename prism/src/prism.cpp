#include "prism/prism.h"
#include "prism/crc32.h"
#include "prism/codec/color.h"
#include "prism/codec/predict.h"
#include "prism/codec/rans.h"
#include "prism/codec/container.h"
#include "prism/codec/analyze.h"
#include "prism/codec/matree.h"
#include <fstream>
#include <stdexcept>

namespace prism {

using namespace codec;

std::vector<uint8_t> encode(const Raster& raster, const EncodeOpts& opts) {
    if (raster.w==0||raster.h==0) throw EncodeError("empty raster");
    uint8_t bd = (raster.bd==BitDepth::BD16)?16:8;
    uint8_t nc = (uint8_t)raster.num_channels();
    // Analyze
    AnalyzeResult ar = analyze(raster, opts.effort);
    if (!opts.use_ycocg) ar.color_transform_id = 0;

    // Apply color transform
    Raster transformed = raster;
    ColorTransform ct = static_cast<ColorTransform>(ar.color_transform_id);
    if (ct != ColorTransform::None) {
        transformed = apply_color(raster, ct, ar.cfl_scales);
    }

    // Build container
    Container c;
    c.hdr.width = raster.w;
    c.hdr.height = raster.h;
    c.hdr.bit_depth = bd;
    c.hdr.num_channels = nc;
    c.hdr.color_transform_id = ar.color_transform_id;
    c.hdr.flags = 0; // CM/LZP off for M0
    c.hdr.effort = opts.effort;
    c.hdr.cfl_scales = ar.cfl_scales;
    c.hdr.squeeze_levels = ar.squeeze_levels;
    c.trees = ar.trees;
    c.predictor_mode = ar.predictor_mode;
    c.global_pred_id = ar.global_pred_id;
    c.per_leaf_pred = ar.per_leaf_pred;

    // For each plane, compute residuals and encode (B5: ResDiff causal context + Rice)
    c.band_payloads.clear();
    for (size_t pi=0; pi< transformed.planes.size(); ++pi) {
        const auto& plane = transformed.planes[pi];
        PredId pred;
        if (c.predictor_mode == 1 && pi < c.per_leaf_pred.size()) {
            pred = static_cast<PredId>(c.per_leaf_pred[pi]);
            if ((uint8_t)pred > 8) pred = PredId::MED;
        } else {
            pred = static_cast<PredId>(c.global_pred_id);
            if ((uint8_t)pred > 8) pred = PredId::MED;
        }
        auto residuals = compute_residuals(plane, transformed.w, transformed.h, pred);
        ModelBank mb = ModelBank::create(44, 16);
        std::vector<uint8_t> bytes;
        rans_encode_residuals_auto(residuals, transformed.w, transformed.h, mb, bytes);
        c.band_payloads.push_back(std::move(bytes));
    }

    return container_encode(transformed, c);
}

Raster decode(const std::vector<uint8_t>& data) {
    return decode(data.data(), data.size());
}

Raster decode(const uint8_t* data, size_t len) {
    if (len < 4) throw DecodeError("too short");
    // Footer crc
    if (len < 4) throw DecodeError("no footer");
    uint32_t crc_stored = read_u32_le_bytes(data + len - 4);
    uint32_t crc_calc = crc32(data, len - 4);
    if (crc_stored != crc_calc) throw DecodeError("crc32_all mismatch - corrupt payload");
    size_t header_end=0;
    Container c = container_decode_header(data, len - 4, header_end);
    // Parse payload bands
    size_t pos = header_end;
    // Compute expected band count from squeeze_levels
    size_t expected = 0;
    for (uint8_t sl : c.hdr.squeeze_levels) expected += 1 + 3u * sl;
    if (expected==0) expected = c.hdr.num_channels; // fallback
    std::vector<std::vector<uint8_t>> payloads;
    for (size_t i=0;i<expected;++i){
        if (pos + 4 > len - 4) throw DecodeError("payload truncated (band_len)");
        uint32_t blen = read_u32_le_bytes(data + pos); pos+=4;
        if (pos + blen > len - 4) throw DecodeError("payload truncated (band_bytes)");
        std::vector<uint8_t> b(data+pos, data+pos+blen);
        payloads.push_back(std::move(b));
        pos+=blen;
    }
    if (pos != len - 4) throw DecodeError("extra bytes after payload");
    // Reconstruct planes
    uint32_t w = c.hdr.width, h = c.hdr.height;
    uint8_t bd = c.hdr.bit_depth;
    PredId pred = static_cast<PredId>(c.global_pred_id);
    if ((uint8_t)pred > 8) pred = PredId::MED;
    Raster out(w,h, static_cast<Channels>(c.hdr.num_channels), bd==16?BitDepth::BD16:BitDepth::BD8);
    if (payloads.size() != expected) {
        throw DecodeError("band count mismatch");
    }
    // For color-transformed rasters, intermediates may exceed 8-bit range (YCoCg-R bias 512)
    uint16_t plane_bd_max = (c.hdr.color_transform_id != 0) ? 65535 : (bd==8? (uint16_t)255 : (uint16_t)65535);
    for (size_t pi=0; pi< out.planes.size(); ++pi) {
        const auto& b = payloads[pi];
        size_t n = (size_t)w * h;
        ModelBank mb = ModelBank::create(44, 16);
        std::vector<int32_t> residuals;
        rans_decode_residuals_auto(b, n, w, h, mb, residuals);
        if (residuals.size() != n) throw DecodeError("residual count mismatch");
        PredId pred;
        if (c.predictor_mode == 1 && pi < c.per_leaf_pred.size()) {
            pred = static_cast<PredId>(c.per_leaf_pred[pi]);
            if ((uint8_t)pred > 8) pred = PredId::MED;
        } else {
            pred = static_cast<PredId>(c.global_pred_id);
            if ((uint8_t)pred > 8) pred = PredId::MED;
        }
        auto plane = reconstruct_plane(residuals, w, h, pred, plane_bd_max);
        out.planes[pi] = std::move(plane);
    }
    // Invert color
    ColorTransform ct = static_cast<ColorTransform>(c.hdr.color_transform_id);
    if (ct != ColorTransform::None) {
        out = invert_color(out, ct, c.hdr.cfl_scales);
    }
    return out;
}

std::vector<uint8_t> read_file(const std::filesystem::path& p){
    std::ifstream f(p, std::ios::binary);
    if (!f) throw std::runtime_error("cannot open "+p.string());
    return std::vector<uint8_t>((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
}
void write_file(const std::filesystem::path& p, const std::vector<uint8_t>& data){
    std::ofstream f(p, std::ios::binary);
    if (!f) throw std::runtime_error("cannot write "+p.string());
    f.write((char*)data.data(), data.size());
}
std::vector<uint8_t> encode_file(const std::filesystem::path& in_path, const EncodeOpts& /*opts*/){
    // This is for encoding raw raster files via frontend decode_to_raster path handled by CLI
    auto data = read_file(in_path);
    (void)data;
    throw EncodeError("encode_file: use frontend decode_to_raster then encode()");
}
Raster decode_file(const std::filesystem::path& in_path){
    auto data = read_file(in_path);
    return decode(data);
}

} // namespace prism
