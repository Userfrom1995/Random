#include "prism/codec/analyze.h"
#include "prism/codec/color.h"

namespace prism::codec {

AnalyzeResult analyze(const Raster& r, uint8_t effort) {
    AnalyzeResult res;
    // Color: B5 enables YCoCg-R for BD8 (verified reversible dense lattice). BD16 stays None until M2 widening.
    if (r.num_channels() >= 3 && r.bd == BitDepth::BD8) {
        ColorChoice cc = choose_color_transform(r);
        res.color_transform_id = static_cast<uint8_t>(cc.id);
        res.cfl_scales = cc.cfl_scales;
        if (res.cfl_scales.empty()) res.cfl_scales.assign(std::max(0, (int)r.num_channels() - 1), 0);
    } else {
        res.color_transform_id = 0;
        res.cfl_scales.assign(std::max(0, (int)r.num_channels() - 1), 0);
    }
    // Squeeze: M0 always 0 (B7 lands Squeeze)
    res.squeeze_levels.assign(r.num_channels(), 0);
    if (effort >= 7) {
        // Future: search squeeze levels
    }
    // Trees: one single-leaf tree per group/band
    MATreeGroup g;
    g.group_id = 0;
    g.band_class = 0;
    g.tree = MATree::single_leaf();
    res.trees.push_back(g);
    // Predictor: B5 selects best predictor per plane (global fallback if all same)
    Raster tr = r;
    ColorTransform ct = static_cast<ColorTransform>(res.color_transform_id);
    if (ct != ColorTransform::None && r.num_channels() >= 3) tr = apply_color(r, ct, res.cfl_scales);
    std::vector<uint8_t> per_plane_best;
    per_plane_best.reserve(tr.planes.size());
    for (size_t c = 0; c < tr.planes.size(); ++c) {
        if (tr.ch == Channels::RGBA && c == 3) {
            // Alpha: keep MED (often already compact)
            per_plane_best.push_back(3);
            continue;
        }
        uint64_t best_cost = UINT64_MAX;
        uint8_t best_pred = 3;
        for (uint8_t pid = 0; pid <= 8; ++pid) {
            PredId id = static_cast<PredId>(pid);
            auto resids = compute_residuals(tr.planes[c], tr.w, tr.h, id);
            uint64_t cost = 0;
            for (int32_t v : resids) cost += (uint64_t)(v < 0 ? -v : v);
            if (cost < best_cost) { best_cost = cost; best_pred = pid; }
        }
        per_plane_best.push_back(best_pred);
    }
    // If all planes share same predictor, use global mode (more compact)
    bool all_same = true;
    for (size_t i = 1; i < per_plane_best.size(); ++i) if (per_plane_best[i] != per_plane_best[0]) all_same = false;
    if (all_same) {
        res.predictor_mode = 0;
        res.global_pred_id = per_plane_best[0];
    } else {
        res.predictor_mode = 1;
        res.global_pred_id = per_plane_best[0];
        res.per_leaf_pred = per_plane_best;
    }
    return res;
}

} // namespace prism::codec
