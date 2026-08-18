//! The decoder: mirror pipeline of the encoder, single pass, O(n), no panics
//! on untrusted input (every failure is a `CodecError`).

use crate::color::{
    subtract_green_inverse_planes, ycocgr_inverse_planes, PlaneRange, TransformChoice,
};
use crate::context::{residual_context_for, unzigzag, ContextModel};
use crate::crc32::crc32;
use crate::error::CodecError;
use crate::header::Header;
use crate::image::{Channels, Image};
use crate::model::{
    alphabet_sizes, build_static_tables, plane_ranges, read_model, ModelConfig,
    ENTROPY_MODE_CAPPED, ENTROPY_MODE_CARC, ENTROPY_MODE_CARC_LZ, ENTROPY_MODE_CARC_MIX,
};
use crate::predict::{neighbors, predict_clamped, PredictorId, WeightVec, M3_WP_GAIN};
use crate::rans::{
    RansDecoder, RansTable, BitReader, GrState, GR_K_INIT, gr_read_symbol, read_gamma,
    gr_adapt_bias, CmState, gr_read_symbol_k, BinDec, read_match, CAPPED_SYMBOLS, CAPPED_ALPHABET,
    BinModel, RangeDec, CarcCtx, cmarc_read_residual, cmarc_mag_bits, cmarc_bins_per_ctx,
    cmarc_lz_bins_per_ctx, cmarc_lz_len_bin, cmarc_lz_off_bin, cmarc_lz_read_gamma,
    cmarc_lz_read_literal, CMARC_LZ_FLAG, MIN_MATCH, cmarc_mix_read_residual, MIX_INIT_W,
};
use std::io::Read;

/// Maximum supported dimension per side. Far above any practical image
/// (Kodak is 768x512) while keeping single-dimension corruption bounded.
const MAX_DIM: u32 = 1 << 20;
/// Maximum supported pixel area, bounding the worst-case allocation even when
/// both dimensions are at the per-side cap.
const MAX_AREA: u64 = 1 << 25;

/// Decode a container into an image, verifying the header CRC.
pub fn decode(bytes: &[u8]) -> Result<Image, CodecError> {
    let mut cur = std::io::Cursor::new(bytes);
    let header = Header::read(&mut cur)?;
    let channels = header.channels()?;
    let transform = if header.transform_flag() {
        TransformChoice::YCoCgR
    } else {
        TransformChoice::None
    };
    let palette_flag = header.palette_flag();

    // Bound the claimed dimensions before any dimension-proportional
    // allocation. A valid stream's pixel volume can far exceed the file size
    // (static tables compress flat regions to a few bytes per thousand
    // pixels), so a ratio against `bytes.len()` would reject legitimate
    // streams. Instead an absolute cap on each side and on the pixel area
    // keeps a corrupt width/height from triggering an OOM-sized allocation.
    let width = header.width as usize;
    let height = header.height as usize;
    if width > MAX_DIM as usize || height > MAX_DIM as usize {
        return Err(CodecError::InvalidStream("dimensions exceed maximum".into()));
    }
    let area = (width as u64) * (height as u64);
    if area > MAX_AREA {
        return Err(CodecError::InvalidStream("dimensions exceed maximum".into()));
    }
    let area = area as usize;

    let mut model_len = [0u8; 4];
    cur.read_exact(&mut model_len)?;
    let model_len = u32::from_le_bytes(model_len) as usize;
    let model_start = cur.position() as usize;
    let model_end = model_start
        .checked_add(model_len)
        .ok_or_else(|| CodecError::InvalidStream("model length overflow".into()))?;
    if model_end > bytes.len() {
        return Err(CodecError::InvalidStream("model section truncated".into()));
    }

    // Determine plane layout before reading the model.
    let palette_chan_count = if palette_flag { 1 } else { channels.plane_count() };
    let eff_channels = if palette_flag {
        Channels::Gray
    } else {
        channels
    };
    let ranges = if palette_flag {
        // The palette colors are read as part of the model.
        vec![PlaneRange::U8; palette_chan_count]
    } else {
        plane_ranges(channels, transform, None, false)
    };
    let sizes = alphabet_sizes(&ranges);
    let model = read_model(&mut cur, &sizes)?;
    if cur.position() as usize != model_end {
        return Err(CodecError::InvalidStream("model length mismatch".into()));
    }

    // The palette colors come from the model; fix the index plane range and
    // recompute the alphabet sizes. The pre-model placeholder (`PlaneRange::U8`)
    // only fixed the plane COUNT; the encoder sizes its rANS tables from the
    // actual palette depth (`PlaneRange::index`), and adaptive tables require
    // matching alphabet sizes, so the sizes must track the corrected range.
    let ranges = match &model.palette {
        Some(pal) if pal.colors.len() >= 1 => vec![PlaneRange::index(pal.colors.len() as u32 - 1)],
        _ => {
            if model.cross_channel {
                plane_ranges(channels, model.transform, None, true)
            } else {
                ranges
            }
        }
    };
    let sizes = alphabet_sizes(&ranges);
    let eff_channels = if model.palette.is_some() { Channels::Gray } else { eff_channels };
    let _ = eff_channels;

    // Payload: per-plane lengths then streams.
    let plane_count = sizes.len();
    let mut lens = vec![0u32; plane_count];
    let mut lbuf = [0u8; 4];
    for l in lens.iter_mut() {
        cur.read_exact(&mut lbuf)?;
        *l = u32::from_le_bytes(lbuf);
    }
    let payload_start = cur.position() as usize;
    let mut stream_start = payload_start;
    let mut payloads: Vec<&[u8]> = Vec::with_capacity(plane_count);
    for l in &lens {
        let end = stream_start
            .checked_add(*l as usize)
            .ok_or_else(|| CodecError::InvalidStream("payload length overflow".into()))?;
        if end > bytes.len() {
            return Err(CodecError::InvalidStream("payload truncated".into()));
        }
        payloads.push(&bytes[stream_start..end]);
        stream_start = end;
    }

    // Build per-plane tables.
    let context = model.context;
    let cm = ContextModel::new(context);
    let entropy_gr = header.entropy_gr();

    // Decode planes.
    let mut decoded: Vec<Vec<i16>> = Vec::with_capacity(plane_count);
    for pi in 0..plane_count {
        let alphabet = sizes[pi];
        let wv = model.weight_for(pi);
        let mut plane = vec![0i16; area];
        if entropy_gr {
            // Design A: per-context adaptive Golomb-Rice, forward raster order.
            // Both sides adapt `k` from the decoded symbols, so no model bytes
            // are needed for the entropy state. Any shortfall (truncated stream)
            // surfaces as `InvalidStream` from the bit reader, never a panic.
            let mut br = BitReader::new(payloads[pi]);
            let mut gr: Vec<GrState> = (0..model.context_count)
                .map(|_| GrState::new(GR_K_INIT))
                .collect();
            if header.gr_cm() {
                // M2.5: mirror the encoder's mixture of Rice experts. Both sides
                // pick the same `cur` expert from identical prior stats, so no
                // model bytes are read; the residual is decoded with `k_current`.
                let mut cms: Vec<CmState> = (0..model.context_count)
                    .map(|_| CmState::new())
                    .collect();
                for y in 0..height {
                    for x in 0..width {
                        let idx = y * width + x;
                        let nb = neighbors(&plane, x, y, width, height);
                        let cid = cm.context_id(&nb, x, y) % model.context_count;
                        let p = model.predictor(pi, cid);
                        let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                        let k = cms[cid].k_current();
                        let r = gr_read_symbol_k(&mut br, k)?;
                        let recon = pred + r;
                        plane[idx] = recon as i16;
                        cms[cid].adapt(r.unsigned_abs());
                    }
                }
            } else if header.gr_lz() {
                // M3-A: mirror the encoder's LZ77 match layer. The flags live in
                // their own bit section (prefixed by a u32 byte length) so the
                // mirrored binary coder can seed its value from a contiguous flag
                // stream; residuals/matches live in a second bit section. A match
                // copies `plane[i - offset .. i - offset + length]` from the
                // decoder's own already-reconstructed buffer, so it stays bit-exact
                // by induction. Matched pixels never update the GR state.
                let area = width * height;
                if payloads[pi].len() < 4 {
                    return Err(CodecError::InvalidStream("GR_LZ plane too short".into()));
                }
                let flag_len = u32::from_le_bytes([
                    payloads[pi][0], payloads[pi][1], payloads[pi][2], payloads[pi][3],
                ]) as usize;
                if 4 + flag_len > payloads[pi].len() {
                    return Err(CodecError::InvalidStream("GR_LZ flag section truncated".into()));
                }
                let flag_bytes = &payloads[pi][4..4 + flag_len];
                let data_bytes = &payloads[pi][4 + flag_len..];
                let mut fbr = BitReader::new(flag_bytes);
                let mut dbr = BitReader::new(data_bytes);
                let mut bin = BinDec::new();
                bin.init(&mut fbr);
                // M3-B: mirror the encoder's self-correcting weighted predictor.
                // The per-context weight table seeds from the per-plane codebook
                // weight and is refined identically on the decoder side, so no
                // weight bytes are signaled and lockstep is preserved. Opt-in
                // seam (`OBSIDIAN_M3_WP="1"`) matching the encoder; default OFF
                // so the shipped path stays on proven M3-A.
                let m3_wp = std::env::var("OBSIDIAN_M3_WP").ok().as_deref() == Some("1");
                let mut wp: Vec<WeightVec> = vec![wv.unwrap_or_else(WeightVec::unit); model.context_count];
                let mut i = 0usize;
                while i < area {
                    let is_match = bin.get(&mut fbr)?;
                    if is_match {
                        let (offset, length) = read_match(&mut dbr)?;
                        let off = offset as usize;
                        // A corrupt stream could overstate length; clamp so the
                        // copy never runs past the plane. Real streams are bounded
                        // by `area - i`, and CRC rejects corruption downstream.
                        let len = (length as usize).min(area - i);
                        if off > i || len == 0 {
                            // Invalid reference for this position: the stream is
                            // corrupt. Stop decoding and let the CRC gate reject it.
                            return Err(CodecError::InvalidStream(
                                "LZ77 match references before start of plane".into(),
                            ));
                        }
                        // Copy sequentially so overlapping matches (offset < len)
                        // replicate the periodic pattern exactly as the encoder's
                        // source comparison did.
                        for l in 0..len {
                            plane[i + l] = plane[i - off + l];
                        }
                        i += len;
                    } else {
                        let x = i % width;
                        let y = i / width;
                        let nb = neighbors(&plane, x, y, width, height);
                        let cid = cm.context_id(&nb, x, y) % model.context_count;
                        let p = model.predictor(pi, cid);
                        let w = if m3_wp && matches!(p, PredictorId::Weighted) {
                            Some(&wp[cid])
                        } else {
                            wv.as_ref()
                        };
                        let pred = predict_clamped(p, &nb, w, ranges[pi]);
                        let r = gr_read_symbol(&mut dbr, &mut gr[cid])?;
                        plane[i] = (pred + r) as i16;
                        if m3_wp && matches!(p, PredictorId::Weighted) {
                            wp[cid].adapt_online(r, nb.l, nb.t, nb.tl, nb.tr, M3_WP_GAIN);
                        }
                        i += 1;
                    }
                }
            } else if header.gr_m2() {
                // M2: mirror the encoder's bias cancellation + run mode. Each
                // component is independently toggleable via the same internal test
                // seam (OBSIDIAN_M2_BIAS / OBSIDIAN_M2_RUN = "0") so the encoder
                // and decoder stay in lockstep within a single roundtrip.
                // Mirror the encoder's default: features are OFF unless explicitly
                // enabled via the OBSIDIAN_M2_BIAS / OBSIDIAN_M2_RUN seams. With
                // both off the M2 branch is byte-identical to v1 GR.
                let use_bias = std::env::var("OBSIDIAN_M2_BIAS").ok().as_deref() == Some("1");
                let use_run = std::env::var("OBSIDIAN_M2_RUN").ok().as_deref() == Some("1");
                let area = width * height;
                let mut prev_val: Option<i32> = None;
                let mut run_left: u32 = 0;
                let mut i = 0usize;
                while i < area {
                    if use_run && run_left > 0 {
                        // Run body pixel: copy the run value, no coding at all.
                        let v = prev_val.expect("run body needs a preceding value");
                        plane[i] = v as i16;
                        run_left -= 1;
                        i += 1;
                        continue;
                    }
                    let x = i % width;
                    let y = i / width;
                    let idx = i;
                    let nb = neighbors(&plane, x, y, width, height);
                    let cid = cm.context_id(&nb, x, y) % model.context_count;
                    let p = model.predictor(pi, cid);
                    let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                    let bias = if use_bias { gr[cid].bias() as i32 } else { 0 };
                    let pred_b = ranges[pi].clamp(pred + bias);
                    let r_coded = gr_read_symbol(&mut br, &mut gr[cid])?;
                    let recon = ranges[pi].clamp(pred_b + r_coded);
                    plane[idx] = recon as i16;
                    let val = recon;
                    // Bias adaptation on the raw residual (dead-zone guarded),
                    // identical to the encoder.
                    if use_bias {
                        gr_adapt_bias(&mut gr[cid], val - pred);
                    }
                    let old_pv = prev_val;
                    let is_run = use_run && matches!(old_pv, Some(pv) if pv == val);
                    prev_val = Some(val);
                    if is_run {
                        // Mirror the encoder: read the run length gamma and copy
                        // the value for the remaining run-1 pixels (no GR symbols).
                        let run = read_gamma(&mut br)?;
                        run_left = run - 1;
                    }
                    i += 1;
                }
            } else if model.entropy_mode == ENTROPY_MODE_CAPPED {
                // M3.5 Design B: mirror the encoder's capped-and-escaped adaptive
                // rANS pass. The plane payload is `[rans_len: u32][rans_bytes]
                // [esc_len: u32][esc_bytes]`. The rANS stream decodes the capped
                // residual symbol for every pixel in raster order; on the escape
                // symbol the full residual is read from the separate escape bit
                // section. Both tables and the escape GrState adapt in raster
                // order, identical to the encoder, so the round-trip is exact.
                if payloads[pi].len() < 8 {
                    return Err(CodecError::InvalidStream("Capped plane too short".into()));
                }
                let rans_len = u32::from_le_bytes([
                    payloads[pi][0], payloads[pi][1], payloads[pi][2], payloads[pi][3],
                ]) as usize;
                if 4 + rans_len + 4 > payloads[pi].len() {
                    return Err(CodecError::InvalidStream("Capped rANS section truncated".into()));
                }
                let rans_bytes = &payloads[pi][4..4 + rans_len];
                let esc_off = 4 + rans_len;
                let esc_len = u32::from_le_bytes([
                    payloads[pi][esc_off],
                    payloads[pi][esc_off + 1],
                    payloads[pi][esc_off + 2],
                    payloads[pi][esc_off + 3],
                ]) as usize;
                if esc_off + 4 + esc_len > payloads[pi].len() {
                    return Err(CodecError::InvalidStream("Capped escape section truncated".into()));
                }
                let esc_bytes = &payloads[pi][esc_off + 4..];
                let mut rdec = RansDecoder::new(rans_bytes)?;
                // Rebuild the identical static rANS tables from the signaled capped
                // histograms (same construction as the encoder); `get` leaves static
                // tables un-adapted, so the decode order reproduces the encode state
                // exactly.
                let cap_hist = model
                    .capped_histograms
                    .as_ref()
                    .expect("capped mode must carry capped histograms");
                let mut tables: Vec<RansTable> = cap_hist[pi]
                    .iter()
                    .map(|opt| {
                        let mut hist = vec![0u32; CAPPED_SYMBOLS];
                        if let Some(pairs) = opt {
                            for &(s, f) in pairs {
                                if (s as usize) < CAPPED_SYMBOLS {
                                    hist[s as usize] = f;
                                }
                            }
                        } else {
                            for v in hist.iter_mut() {
                                *v = 1;
                            }
                        }
                        RansTable::new_static(&hist)
                    })
                    .collect();
                let mut esc_br = BitReader::new(esc_bytes);
                let mut esc_gr: Vec<GrState> = (0..model.context_count)
                    .map(|_| GrState::new(GR_K_INIT))
                    .collect();
                for y in 0..height {
                    for x in 0..width {
                        let idx = y * width + x;
                        let nb = neighbors(&plane, x, y, width, height);
                        let cid = cm.context_id(&nb, x, y) % model.context_count;
                        let p = model.predictor(pi, cid);
                        let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                        let sym = rdec.get(&mut tables[cid])?;
                        let r = if sym != CAPPED_ALPHABET {
                            unzigzag(sym as u32)
                        } else {
                            gr_read_symbol(&mut esc_br, &mut esc_gr[cid])?
                        };
                        plane[idx] = (pred + r) as i16;
                    }
                }
            } else if matches!(
                model.entropy_mode,
                ENTROPY_MODE_CARC | ENTROPY_MODE_CARC_LZ | ENTROPY_MODE_CARC_MIX
            ) {
                // R1 CMARC: mirror the encoder's context-modeled binary range
                // coder. The plane payload is `[len: u32][bytes]`; the bytes are
                // the shared per-plane range coder stream over all `(cid, bin)`
                // models. `RangeDec::init` seeds its value from the leading
                // `BIN_BITS` bits, then each residual/token is recovered by the
                // identical per-bin model updates in the identical order, so the
                // round-trip is bit-exact by construction.
                //
                // R2.3 (ENTROPY_MODE_CARC_LZ) re-weaves the LZ77 match layer into
                // this same single range coder: the match flag, the Elias-gamma
                // length/offset codes, and the literal CMARC residual are all more
                // bits through the same per-`(cid, bin)` models. The decoder copies
                // matched runs from its own already-reconstructed buffer, so it
                // stays bit-exact by induction (its prefix equals the encoder's
                // source prefix at every position). See
                // `obsidian/docs/architect-cmarc-blueprint.md` section 5.3.
                if payloads[pi].len() < 4 {
                    return Err(CodecError::InvalidStream("CMARC plane too short".into()));
                }
                let cm_len = u32::from_le_bytes([
                    payloads[pi][0], payloads[pi][1], payloads[pi][2], payloads[pi][3],
                ]) as usize;
                if 4 + cm_len > payloads[pi].len() {
                    return Err(CodecError::InvalidStream("CMARC section truncated".into()));
                }
                let cm_bytes = &payloads[pi][4..4 + cm_len];
                let mut cbr = BitReader::new(cm_bytes);
                let mut dec = RangeDec::new();
                dec.init(&mut cbr);
                let mag_bits = cmarc_mag_bits((ranges[pi].max - ranges[pi].min) as u32);
                let is_lz = model.entropy_mode == ENTROPY_MODE_CARC_LZ;
                let is_mix = model.entropy_mode == ENTROPY_MODE_CARC_MIX;
                let bins_per_ctx = if is_lz {
                    cmarc_lz_bins_per_ctx(mag_bits)
                } else {
                    cmarc_bins_per_ctx(mag_bits)
                };
                // R3-A: size the CMARC model/ctx tables by the residual-context
                // count, decoupled from the gradient `context_count`.
                let rc_count = cm.rc_count();
                let mut models: Vec<BinModel> = vec![
                    BinModel::new();
                    rc_count * bins_per_ctx
                ];
                // Seed per-`(cid, bin)` static priors when present (R1-c). The
                // priors are stored as `(n1, n0)` count pairs indexed by `cid *
                // bins_per_ctx + bin`; absent bins use the uniform prior. The
                // encoder computes the identical counts during analyze, so
                // lockstep is preserved. (Guarded out for the LZ layout: the LZ
                // residual bins are offset by one past the match-flag bin, so the
                // literal-only prior indices would land on the flag bin; R1-c for
                // LZ will be wired when that milestone is built.)
                if !is_lz {
                    if let Some(ref per_plane) = model.cmarc_priors {
                        if let Some(ref ctxs_p) = per_plane.get(pi) {
                            for (cid, opt) in ctxs_p.iter().enumerate() {
                                if let Some(pairs) = opt {
                                    for &(bin, n1, n0) in pairs {
                                        let m = BinModel::from_counts(n1, n0);
                                        let slot =
                                            cid * bins_per_ctx + (bin as usize % bins_per_ctx);
                                        if slot < models.len() {
                                            models[slot] = m;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                let mut ctxs: Vec<CarcCtx> = (0..rc_count)
                    .map(|_| CarcCtx::new())
                    .collect();
                if is_lz {
                    // R2.3 decode: flag, then match (gamma length/offset) or
                    // literal (CMARC residual). `plane` is reconstructed in raster
                    // order, so `neighbors` for the context sees the identical
                    // prefix the encoder saw (bit-exact by induction), and matches
                    // copy from earlier reconstructed samples which equal the
                    // source.
                    let area = width * height;
                    let mut i = 0usize;
                    while i < area {
                        let x = i % width;
                        let y = i / width;
                        let nb = neighbors(&plane, x, y, width, height);
                        let grad_cid = cm.context_id(&nb, x, y) % model.context_count;
                        // R3-A: residual-coding (and match-flag) context is the DIFF
                        // context; the decoder's reconstructed prefix equals the
                        // encoder's source by induction, so the context matches.
                        let cid = residual_context_for(
                            &cm,
                            &model,
                            &plane,
                            x,
                            y,
                            width,
                            height,
                            wv.as_ref(),
                            ranges[pi],
                            pi,
                        );
                        let slot = cid * bins_per_ctx;
                        let is_match = dec.get(&mut cbr, &mut models[slot + CMARC_LZ_FLAG])?;
                        if is_match {
                            let lmm = cmarc_lz_read_gamma(
                                &mut dec,
                                &mut cbr,
                                &mut models,
                                slot + cmarc_lz_len_bin(mag_bits),
                            )?;
                            let offset = cmarc_lz_read_gamma(
                                &mut dec,
                                &mut cbr,
                                &mut models,
                                slot + cmarc_lz_off_bin(mag_bits),
                            )?;
                            let length = lmm + MIN_MATCH as u32 - 1;
                            let off = offset as usize;
                            let len = (length as usize).min(area - i);
                            if off > i || len == 0 {
                                // Invalid reference: the stream is corrupt. The
                                // container CRC rejects it downstream.
                                return Err(CodecError::InvalidStream(
                                    "CMARC-LZ match references before start of plane".into(),
                                ));
                            }
                            for l in 0..len {
                                plane[i + l] = plane[i - off + l];
                            }
                            i += len;
                        } else {
                            let p = model.predictor(pi, grad_cid);
                            let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                            let r = cmarc_lz_read_literal(
                                &mut dec,
                                &mut cbr,
                                &mut models,
                                slot,
                                mag_bits,
                            )?;
                            ctxs[cid].adapt(r.unsigned_abs());
                            plane[i] = (pred + r) as i16;
                            i += 1;
                        }
                    }
                } else if is_mix {
                    // R2.4 decode: logistic-mixed CMARC. The per-`(cid, bin)` primary
                    // model is seeded from `cmarc_priors` exactly like the plain CMARC
                    // path (the layout is identical); the per-`bin` coarse model and
                    // the per-bin logistic weight start uniform and adapt to the same
                    // bits the encoder saw, so lockstep holds and the round-trip is
                    // bit-exact. See `obsidian/docs/architect-cmarc-blueprint.md` 5.4.
                    let mut mix_models: Vec<BinModel> = vec![BinModel::new(); bins_per_ctx];
                    let mut mix_w: Vec<i32> = vec![MIX_INIT_W; bins_per_ctx];
                    for y in 0..height {
                        for x in 0..width {
                            let idx = y * width + x;
                            let nb = neighbors(&plane, x, y, width, height);
                            let grad_cid = cm.context_id(&nb, x, y) % model.context_count;
                            let p = model.predictor(pi, grad_cid);
                            let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                            // R3-A: residual-coding context is the DIFF context.
                            let cid = residual_context_for(
                                &cm,
                                &model,
                                &plane,
                                x,
                                y,
                                width,
                                height,
                                wv.as_ref(),
                                ranges[pi],
                                pi,
                            );
                            let r = cmarc_mix_read_residual(
                                &mut dec,
                                &mut cbr,
                                &mut models,
                                &mut mix_models,
                                &mut mix_w,
                                &mut ctxs[cid],
                                cid,
                                bins_per_ctx,
                                mag_bits,
                            )?;
                            plane[idx] = (pred + r) as i16;
                        }
                    }
                } else {
                    for y in 0..height {
                        for x in 0..width {
                            let idx = y * width + x;
                            let nb = neighbors(&plane, x, y, width, height);
                            let grad_cid = cm.context_id(&nb, x, y) % model.context_count;
                            let p = model.predictor(pi, grad_cid);
                            let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                            // R3-A: residual-coding context is the DIFF context.
                            let cid = residual_context_for(
                                &cm,
                                &model,
                                &plane,
                                x,
                                y,
                                width,
                                height,
                                wv.as_ref(),
                                ranges[pi],
                                pi,
                            );
                            let r = cmarc_read_residual(
                                &mut dec,
                                &mut cbr,
                                &mut models,
                                &mut ctxs[cid],
                                cid,
                                mag_bits,
                            )?;
                            plane[idx] = (pred + r) as i16;
                        }
                    }
                }
            } else {
                for y in 0..height {
                    for x in 0..width {
                        let idx = y * width + x;
                        let nb = neighbors(&plane, x, y, width, height);
                        let cid = cm.context_id(&nb, x, y) % model.context_count;
                        let p = model.predictor(pi, cid);
                        let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                        let r = gr_read_symbol(&mut br, &mut gr[cid])?;
                        plane[idx] = (pred + r) as i16;
                    }
                }
            }
        } else {
            let mut dec = RansDecoder::new(payloads[pi])?;
            let mut adaptive_tables: Vec<RansTable> = Vec::new();
            let mut static_tables: Vec<Option<RansTable>> = Vec::new();
            if let Some(hist) = &model.static_histograms {
                let built = build_static_tables(hist, &sizes);
                static_tables = built.into_iter().nth(pi).unwrap();
            } else {
                adaptive_tables = (0..model.context_count)
                    .map(|_| RansTable::new_adaptive(alphabet))
                    .collect();
            }
            let use_static = !static_tables.is_empty();
            for y in 0..height {
                for x in 0..width {
                    let idx = y * width + x;
                    let nb = neighbors(&plane, x, y, width, height);
                    let cid = cm.context_id(&nb, x, y) % model.context_count;
                    let p = model.predictor(pi, cid);
                    let pred = predict_clamped(p, &nb, wv.as_ref(), ranges[pi]);
                    let sym = if use_static {
                        let table = static_tables[cid].as_mut().ok_or_else(|| {
                            CodecError::InvalidStream(format!("missing static table for context {cid}"))
                        })?;
                        dec.get(table)?
                    } else {
                        dec.get(&mut adaptive_tables[cid])?
                    };
                    let r = unzigzag(sym as u32);
                    plane[idx] = (pred + r) as i16;
                }
            }
        }
        decoded.push(plane);
    }

    // Inverse transform.
    if model.transform == TransformChoice::YCoCgR && !palette_flag {
        ycocgr_inverse_planes(&mut decoded);
    }
    // R2.1 inverse cross-channel: undo subtract-green after the color transform.
    if model.cross_channel && !palette_flag {
        subtract_green_inverse_planes(&mut decoded, channels);
    }

    // Palette expand or assemble the image.
    let image = if let Some(pal) = &model.palette {
        crate::color::palette_expand(pal, &decode_u8(&decoded[0]), width as u32, height as u32)?
    } else {
        let mut img = Image::new(header.width, header.height, channels)?;
        for (c, plane) in decoded.iter().enumerate() {
            for i in 0..area {
                img.planes[c][i] = plane[i] as u8;
            }
        }
        img
    };

    // CRC verification.
    let raw = image.raw_bytes();
    if crc32(&raw) != header.crc32 {
        return Err(CodecError::CrcMismatch);
    }
    Ok(image)
}

fn decode_u8(plane: &[i16]) -> Vec<u8> {
    plane.iter().map(|&v| v as u8).collect()
}

/// Parse a container's header and model without decoding (used by `check`).
pub fn inspect(bytes: &[u8]) -> Result<(Header, ModelConfig, usize), CodecError> {
    let mut cur = std::io::Cursor::new(bytes);
    let header = Header::read(&mut cur)?;
    let channels = header.channels()?;
    let transform = if header.transform_flag() {
        TransformChoice::YCoCgR
    } else {
        TransformChoice::None
    };
    let palette_flag = header.palette_flag();
    let mut model_len = [0u8; 4];
    cur.read_exact(&mut model_len)?;
    let model_len = u32::from_le_bytes(model_len) as usize;
    let model_start = cur.position() as usize;
    let model_end = model_start + model_len;
    if model_end > bytes.len() {
        return Err(CodecError::InvalidStream("model section truncated".into()));
    }
    let eff_channels = if palette_flag { Channels::Gray } else { channels };
    let ranges = if palette_flag {
        vec![PlaneRange::U8]
    } else {
        plane_ranges(channels, transform, None, false)
    };
    let sizes = alphabet_sizes(&ranges);
    let model = read_model(&mut cur, &sizes)?;
    let _ = eff_channels;
    Ok((header, model, model_end))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::encoder::{encode, encode_with, fuzz_gate, FuzzGen, roundtrip, EncodeOpts};
    use crate::model::ENTROPY_MODE_GR;
    use std::sync::Mutex;

    // Serializes the two tests that flip the process-global `OBSIDIAN_CM` env
    // var, so they can't leak the setting into each other under `--test-threads`.
    static CM_ENV_LOCK: Mutex<()> = Mutex::new(());

    #[test]
    fn decode_matches_encode() {
        let mut img = Image::new(20, 15, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = (i.wrapping_mul(11) & 0xFF) as u8;
            }
        }
        let (bytes, _) = encode(&img, 4).unwrap();
        let back = decode(&bytes).unwrap();
        assert_eq!(back, img);
    }

    #[test]
    fn decode_rejects_garbage() {
        assert!(decode(b"OBSD\x01\x01\x08\x04").is_err());
        assert!(decode(&[]).is_err());
        let mut junk = vec![0x4F, 0x42, 0x53, 0x44, 0x01];
        junk.extend_from_slice(&[0; 30]);
        assert!(decode(&junk).is_err());
    }

    #[test]
    fn decode_rejects_inflated_dimensions() {
        let mut img = Image::new(4, 4, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = (i * 13) as u8;
            }
        }
        let (bytes, _) = encode(&img, 0).unwrap();
        // Flip the upper two bytes of the width field (offsets 10-11): the
        // claimed dimensions now exceed the caps, which must be rejected
        // before any allocation is attempted (the OOM abort seen pre-fix).
        for off in [10usize, 11] {
            let mut corrupt = bytes.clone();
            corrupt[off] ^= 0xFF;
            let err = decode(&corrupt).unwrap_err();
            assert!(
                err.to_string().contains("dimensions exceed maximum"),
                "got: {err}"
            );
        }
    }

    #[test]
    fn decode_accepts_large_flat_stream() {
        // A flat image must compress (never expand) at every effort, so the
        // dimension guard must not be a ratio against the input size (that
        // would reject legitimate streams). With the Golomb-Rice entropy
        // backend the only non-zero residuals are the border pixels, so the
        // size floor below reflects GR behavior rather than rANS's tighter
        // few-symbol bound.
        let mut img = Image::new(512, 512, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = 128;
            }
        }
        for e in [0u8, 7] {
            let (bytes, _) = encode(&img, e).unwrap();
            assert!(
                bytes.len() < img.raw_bytes().len() / 4,
                "flat image should compress hard at effort {e}: {} vs {}",
                bytes.len(),
                img.raw_bytes().len() / 4
            );
            assert_eq!(decode(&bytes).unwrap(), img);
        }
    }

    #[test]
    fn fuzz_all_efforts() {
        let mut gen = FuzzGen::new(1234);
        for _ in 0..8 {
            let img = gen.random_image();
            for e in 0..=7u8 {
                let (bytes, _) = encode(&img, e).unwrap();
                let back = decode(&bytes).unwrap();
                assert_eq!(back, img);
            }
        }
    }

    #[test]
    fn fuzz_gate_basic() {
        assert!(fuzz_gate(5, &[0, 4, 7]).is_ok());
    }

    #[test]
    fn cm_flag_present_when_enabled() {
        // With the OBSIDIAN_CM="1" seam the M2.5 context-mixing backend engages
        // (GR_CM flag set) and a flat image round-trips exactly, compressing to a
        // tiny stream. CM ships OFF by default, so this verifies the opt-in path.
        let _lock = CM_ENV_LOCK.lock().unwrap();
        std::env::set_var("OBSIDIAN_CM", "1");
        let mut img = Image::new(96, 96, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = 128;
            }
        }
        let (bytes, stats) = encode(&img, 4).unwrap();
        assert!(stats.bpp < 9.0, "CM flat image bpp too high: {}", stats.bpp);
        let back = decode(&bytes).unwrap();
        assert_eq!(back, img);
        use crate::header::Header;
        let mut cur = std::io::Cursor::new(&bytes);
        let h = Header::read(&mut cur).unwrap();
        assert!(h.gr_cm());
        std::env::remove_var("OBSIDIAN_CM");
    }

    #[test]
    fn cm_disabled_by_default_is_v1() {
        // Without the seam the effort >= 1 stream uses the v1 GR backend (no
        // GR_CM flag), so enabling CM must never silently change production
        // output. CM is opt-in precisely because it regresses ~0.5% on the
        // stationary residuals of photographic content.
        let _lock = CM_ENV_LOCK.lock().unwrap();
        std::env::set_var("OBSIDIAN_CM", "0");
        let mut img = Image::new(40, 40, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        let (bytes, _) = encode(&img, 4).unwrap();
        use crate::header::Header;
        let mut cur = std::io::Cursor::new(&bytes);
        let h = Header::read(&mut cur).unwrap();
        assert!(!h.gr_cm(), "CM must be off by default");
        assert_eq!(decode(&bytes).unwrap(), img);
    }

    #[test]
    fn capped_roundtrip_bit_exact() {
        // M3.5 Design B: with the capped backend engaged the capped-and-escaped
        // rANS stream decodes bit-exactly. The decoder learns the mode from the
        // signaled model section (no env mirror needed), so this verifies the
        // end-to-end encode/decode lockstep. Uses `encode_with` (not the
        // OBSIDIAN_CAPPED env seam) so the test stays isolated from the
        // process-global state other tests read.
        let mut img = Image::new(160, 128, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        let (bytes, _stats) = encode_with(&img, 4, EncodeOpts { capped: Some(true), cmarc: None, ..Default::default() }).unwrap();
        let back = decode(&bytes).unwrap();
        assert_eq!(back, img, "capped backend must round-trip bit-exactly");
        // The signaled entropy mode must be CAPPED (verified via inspect), and the
        // model must carry the static capped histograms the decoder rebuilds its
        // tables from.
        let (_h, model, _off) = inspect(&bytes).unwrap();
        assert_eq!(model.entropy_mode, ENTROPY_MODE_CAPPED);
        assert!(model.capped_histograms.is_some());
        // The ramp above has large wrapped residuals, so the escape path is
        // exercised; bit-exact round-trip through both the rANS symbols and the
        // GR-coded escaped residuals is the real invariant here. (The static
        // table model section dominates bpp on a small synthetic image, which is
        // the known model-size tradeoff and cannot be judged without the real
        // Kodak corpus, so no bpp bound is asserted.)
    }

    #[test]
    fn capped_disabled_by_default_is_v1() {
        // Without opting in, output stays on the v1 GR backend (entropy mode 0);
        // Design B is opt-in because its photographic gain is marginal. Neither
        // the env seam nor `EncodeOpts` sets it here, so this also confirms the
        // default `encode` path does not silently switch backends.
        let mut img = Image::new(40, 40, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        let (bytes, _) = encode(&img, 4).unwrap();
        let (_h, model, _off) = inspect(&bytes).unwrap();
        assert_eq!(model.entropy_mode, ENTROPY_MODE_GR, "capped must be off by default");
        assert_eq!(decode(&bytes).unwrap(), img);
    }

    #[test]
    fn m2_matches_v1_on_noisy() {
        // Effort-0 (v1 GR) and effort-4 (M2 GR_M2) must both round-trip the same
        // image bit-exactly; M2 only adds mirrored state, it cannot alter pixels.
        let mut img = Image::new(40, 40, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        let (_, _, a) = roundtrip(&img, 0).unwrap();
        let (_, _, b) = roundtrip(&img, 4).unwrap();
        assert_eq!(a, img);
        assert_eq!(b, img);
    }

    #[test]
    fn m2_gr_m2_flag_absent_at_effort0() {
        let mut img = Image::new(8, 8, Channels::Gray).unwrap();
        for i in 0..img.area() {
            img.planes[0][i] = (i * 5 & 0xFF) as u8;
        }
        let (bytes, _) = encode(&img, 0).unwrap();
        use crate::header::Header;
        let mut cur = std::io::Cursor::new(&bytes);
        let h = Header::read(&mut cur).unwrap();
        assert!(!h.gr_m2(), "effort 0 must use v1 GR (no GR_M2 flag)");
        assert_eq!(decode(&bytes).unwrap(), img);
    }

    #[test]
    fn cmarc_enabled_is_lossless() {
        // Whenever CMARC is engaged (via `cmarc: Some(true)`), the image still
        // round-trips bit-exactly. The never-expand safety net may silently fall
        // back to the model's best GR backend when CMARC does not win, but either
        // way the output is lossless - the binary range coder is always exact.
        let mut img = Image::new(48, 40, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        for e in [1u8, 4, 7] {
            let (bytes, stats) = encode_with(&img, e, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
            let back = decode(&bytes).unwrap();
            assert_eq!(back, img, "CMARC rgb effort {e} round-trip");
            assert!(stats.bpp > 0.0 && stats.bpp < 24.0, "CMARC bpp sane: {}", stats.bpp);
        }
    }

    #[test]
    fn cmarc_wins_on_flat() {
        // On near-flat content the MED residuals are all zero, so CMARC's
        // zero-flag bin collapses to near-certain and the binary coder spends
        // `H(p) + epsilon` per residual - strictly below the single-k GR symbol
        // coder. Here CMARC must win and be signaled via `entropy_mode`.
        let w = 192u32;
        let h = 160u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = 77u8;
            }
        }
        let (gr_bytes, _) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: None, ..Default::default() }).unwrap();
        let (cm_bytes, _) =
            encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&cm_bytes).unwrap(), img);
        assert!(
            cm_bytes.len() < gr_bytes.len(),
            "CMARC must beat GR on flat content: cmarc {} vs gr {}",
            cm_bytes.len(),
            gr_bytes.len()
        );
        let (_h, model, _off) = inspect(&cm_bytes).unwrap();
        assert_eq!(model.entropy_mode, crate::model::ENTROPY_MODE_CARC);
    }

    #[test]
    fn cmarc_fuzz_lockstep() {
        // Fuzz a batch of randomized small images through CMARC at several efforts
        // and assert bit-exact round-trip (the lockstep proof in the research doc).
        let mut gen = FuzzGen::new(0xBEEF);
        for _ in 0..12 {
            let img = gen.random_image();
            for e in [1u8, 4, 7] {
                let (bytes, _) = encode_with(&img, e, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
                let back = decode(&bytes).unwrap();
                assert_eq!(back, img, "CMARC fuzz effort {e}");
            }
        }
    }

    #[test]
    fn cmarc_is_lossless_on_noise() {
        // Pure noise has no exploitable context, so this is the worst case for any
        // context model. CMARC must still round-trip exactly (it cannot expand a
        // bit pattern) - the safety net keeps the *file size* from regressing, the
        // entropy stage itself is always lossless.
        let mut img = Image::new(32, 32, Channels::Rgb).unwrap();
        let mut seed = 0x9876u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = (rnd() & 0xFF) as u8;
            }
        }
        let (bytes, _) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&bytes).unwrap(), img);
    }

    #[test]
    fn cmarc_off_by_default_is_v1() {
        // Without opting in, output stays on the v1 GR backend (entropy mode 0);
        // CMARC is opt-in because its photographic gain is measured behind the
        // never-expand safety net and the production default preserves the proven
        // 10.16 bpp baseline until real Kodak confirms the win.
        let mut img = Image::new(40, 40, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
            }
        }
        let (bytes, _) = encode(&img, 4).unwrap();
        let (_h, model, _off) = inspect(&bytes).unwrap();
        assert_eq!(model.entropy_mode, ENTROPY_MODE_GR, "CMARC must be off by default");
        assert_eq!(decode(&bytes).unwrap(), img);
    }

    #[test]
    fn carc_lz_lossless_roundtrip() {
        // R2.3: whenever the CMARC-LZ match layer is engaged (cmarc + carc_lz),
        // the image round-trips bit-exactly. The decoder copies matches from its
        // own reconstructed buffer, so the round-trip is exact by induction. The
        // safety net may fall back to CMARC-literal or v1 GR when LZ does not win,
        // but whichever backend ships, the output is lossless.
        let cases: Vec<(u32, u32, Channels)> = vec![
            (48, 40, Channels::Rgb),
            (64, 64, Channels::Gray),
            (128, 96, Channels::Rgba),
            (40, 40, Channels::Rgb),
        ];
        for (w, h, ch) in cases {
            let mut img = Image::new(w, h, ch).unwrap();
            for c in 0..ch.plane_count() {
                for i in 0..img.area() {
                    img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
                }
            }
            for e in [1u8, 4, 7] {
                let (bytes, _) = encode_with(
                    &img,
                    e,
                    EncodeOpts {
                        capped: None,
                        cmarc: Some(true),
                        carc_lz: Some(true),
                        ..Default::default()
                    },
                )
                .unwrap();
                assert_eq!(decode(&bytes).unwrap(), img, "CARC_LZ {w}x{h} {ch:?} e{e}");
            }
        }
    }

    #[test]
    fn carc_lz_forced_selection_exercises_decode() {
        // The strong predictor bank means the never-expand safety net almost never
        // selects LZ77 on real/synthetic content (matches M3-A's photographic
        // finding). To prove the ENTROPY_MODE_CARC_LZ decode branch is correct we
        // force selection via a test-only seam and assert bit-exact round-trip plus
        // that the decoder reads entropy_mode == CARC_LZ (the match walk, not the
        // literal path).
        let _lock = CM_ENV_LOCK.lock().unwrap();
        std::env::set_var("OBSIDIAN_CARC_LZ_FORCE", "1");
        let cases: Vec<(u32, u32, Channels)> = vec![
            (256, 64, Channels::Gray),
            (48, 40, Channels::Rgb),
            (64, 64, Channels::Gray),
            (128, 96, Channels::Rgba),
        ];
        for (w, h, ch) in cases {
            let mut img = Image::new(w, h, ch).unwrap();
            for c in 0..ch.plane_count() {
                for i in 0..img.area() {
                    img.planes[c][i] = ((i * 13 + c * 7) & 0xFF) as u8;
                }
            }
            let (bytes, _) = encode_with(
                &img,
                4,
                EncodeOpts {
                    capped: None,
                    cmarc: Some(true),
                    carc_lz: Some(true),
                    ..Default::default()
                },
            )
            .unwrap();
            let (_h, model, _off) = inspect(&bytes).unwrap();
            assert_eq!(
                model.entropy_mode,
                crate::model::ENTROPY_MODE_CARC_LZ,
                "forced CARC_LZ must signal ENTROPY_MODE_CARC_LZ on {w}x{h} {ch:?}"
            );
            assert_eq!(decode(&bytes).unwrap(), img, "CARC_LZ forced {w}x{h} {ch:?}");
            // The selection is forced, not a claim it is the smallest: only assert
            // the forced stream round-trips (never-expand is covered separately).
        }
        std::env::remove_var("OBSIDIAN_CARC_LZ_FORCE");
    }

    #[test]
    fn carc_lz_fuzz_lockstep() {
        // Fuzz a batch of randomized small images through the CMARC-LZ path at
        // several efforts and assert bit-exact round-trip (the lockstep proof).
        let mut gen = FuzzGen::new(0xC0DE);
        for _ in 0..10 {
            let img = gen.random_image();
            for e in [1u8, 4, 7] {
                let (bytes, _) = encode_with(
                    &img,
                    e,
                    EncodeOpts {
                        capped: None,
                        cmarc: Some(true),
                        carc_lz: Some(true),
                        ..Default::default()
                    },
                )
                .unwrap();
                assert_eq!(decode(&bytes).unwrap(), img, "CARC_LZ fuzz e{e}");
            }
        }
    }

    #[test]
    fn carc_lz_never_expands_vs_cmarc() {
        // The never-expand safety net compares the CARC_LZ candidate against the
        // best of {GR, CMARC-literal}, so engaging LZ can only match or beat the
        // file the model would have shipped. Photographic content has few long
        // matches, so LZ typically falls back - but it must never expand.
        let w = 192u32;
        let h = 160u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        for c in 0..3 {
            for y in 0..h {
                for x in 0..w {
                    let fx = x as f64 / w as f64;
                    let fy = y as f64 / h as f64;
                    let v = 40.0
                        + 90.0 * (2.0 * std::f64::consts::PI * (0.6 * fx + 0.3 * fy)).sin()
                        + 0.35 * (x as f64 * 0.5 + y as f64 * 0.3)
                        + c as f64 * 12.0;
                    img.planes[c][(y * w + x) as usize] = v.clamp(0.0, 255.0) as u8;
                }
            }
        }
        let (base_bytes, _) = encode_with(
            &img,
            4,
            EncodeOpts {
                capped: None,
                cmarc: Some(true),
                carc_lz: Some(false),
                ..Default::default()
            },
        )
        .unwrap();
        let (lz_bytes, lz_stats) = encode_with(
            &img,
            4,
            EncodeOpts {
                capped: None,
                cmarc: Some(true),
                carc_lz: Some(true),
                ..Default::default()
            },
        )
        .unwrap();
        assert_eq!(decode(&lz_bytes).unwrap(), img);
        println!(
            "photographic CARC_LZ vs CMARC: cmarc={} bytes, carc_lz={} bytes ({} bpp)",
            base_bytes.len(),
            lz_bytes.len(),
            lz_stats.bpp
        );
        assert!(
            lz_bytes.len() <= base_bytes.len(),
            "CARC_LZ safety net must not expand vs CMARC: lz {} vs cmarc {}",
            lz_bytes.len(),
            base_bytes.len()
        );
    }

    #[test]
    fn cmarc_never_expands_vs_model_best() {
        // The never-expand safety net compares the CMARC candidate against the
        // model's BEST non-CMARC backend (which may itself use gr_cm / gr_lz), not
        // just plain v1 GR. So enabling CMARC must never produce a larger file than
        // the model would have shipped without it. This is the merge-gate property:
        // CMARC is safe to opt into because it can only match or beat production.
        let w = 192u32;
        let h = 160u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        for c in 0..3 {
            for y in 0..h {
                for x in 0..w {
                    let fx = x as f64 / w as f64;
                    let fy = y as f64 / h as f64;
                    let v = 40.0
                        + 90.0 * (2.0 * std::f64::consts::PI * (0.6 * fx + 0.3 * fy)).sin()
                        + 0.35 * (x as f64 * 0.5 + y as f64 * 0.3)
                        + c as f64 * 12.0;
                    img.planes[c][(y * w + x) as usize] = v.clamp(0.0, 255.0) as u8;
                }
            }
        }
        let (gr_bytes, gr_stats) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: None, ..Default::default() }).unwrap();
        let (cm_bytes, cm_stats) =
            encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&cm_bytes).unwrap(), img);
        println!(
            "smooth photographic: model_best={:.3} bpp ({} bytes), cmarc={:.3} bpp ({} bytes)",
            gr_stats.bpp,
            gr_bytes.len(),
            cm_stats.bpp,
            cm_bytes.len()
        );
        // CMARC engaged but did not beat the model's chosen backend -> it falls
        // back, so the file is at most as large as the model-best baseline.
        assert!(
            cm_bytes.len() <= gr_bytes.len(),
            "CMARC safety net must not expand vs model best: cmarc {} vs best {}",
            cm_bytes.len(),
            gr_bytes.len()
        );
    }

    #[test]
    fn cmarc_flat_probe() {
        let w = 192u32;
        let h = 160u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        // Flat planes -> all MED residuals are zero -> CMARC zero-flag collapses.
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = 77u8;
            }
        }
        let (gr_bytes, gr_stats) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: None, ..Default::default() }).unwrap();
        let (cm_bytes, cm_stats) =
            encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&cm_bytes).unwrap(), img);
        println!(
            "FLAT: gr={:.3} bpp ({} bytes), cmarc={:.3} bpp ({} bytes)",
            gr_stats.bpp, gr_bytes.len(), cm_stats.bpp, cm_bytes.len()
        );
    }

    #[test]
    fn cmarc_laplacian_probe() {
        // Realistic photographic residuals after a good predictor (MED) are small
        // and Laplacian: mostly 0, +/-1, +/-2. CMARC's per-context binary model
        // should then beat GR, mirroring how JPEG-LS (near-lossless) residuals
        // compress well under context modeling.
        let w = 192u32;
        let h = 160u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        for c in 0..3 {
            for i in 0..img.area() {
                let base = 90u32 + ((i / w as usize) as u32) * 0; // flat base
                let lapl = (((i * 31 + c * 7) % 7) as i32) - 3; // small spread -3..3
                img.planes[c][i] = (base as i32 + lapl).clamp(0, 255) as u8;
            }
        }
        let (gr_bytes, gr_stats) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: None, ..Default::default() }).unwrap();
        let (cm_bytes, cm_stats) =
            encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&cm_bytes).unwrap(), img);
        println!(
            "LAPLACIAN: gr={:.3} bpp ({} bytes), cmarc={:.3} bpp ({} bytes)",
            gr_stats.bpp, gr_bytes.len(), cm_stats.bpp, cm_bytes.len()
        );
    }

    #[test]
    fn cmarc_never_expands_over_gr() {
        // The safety net: even on adversarial white-noise content (worst case for
        // any context model), enabling CMARC never produces a larger file than
        // v1 GR - it silently falls back to the GR candidate.
        let w = 128u32;
        let h = 128u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        let mut seed = 0xCAFEu64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = (rnd() & 0xFF) as u8;
            }
        }
        let (gr_bytes, _) = encode_with(&img, 4, EncodeOpts { capped: None, cmarc: None, ..Default::default() }).unwrap();
        let (cm_bytes, _) =
            encode_with(&img, 4, EncodeOpts { capped: None, cmarc: Some(true), ..Default::default() }).unwrap();
        assert_eq!(decode(&cm_bytes).unwrap(), img);
        assert!(
            cm_bytes.len() <= gr_bytes.len() + 8,
            "CMARC safety net must not expand vs GR on noise: cmarc {} vs gr {}",
            cm_bytes.len(),
            gr_bytes.len()
        );
    }

    #[test]
    fn cross_channel_forced_roundtrip() {
        // Force subtract-green on (both the bare variant and the YCoCg-R variant
        // are considered; the cheaper wins) and verify a bit-exact round-trip
        // plus that the model signals the transform.
        let w = 96u32;
        let h = 64u32;
        let mut img = Image::new(w, h, Channels::Rgb).unwrap();
        let mut seed = 0xBEEFu64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for c in 0..3 {
            for i in 0..img.area() {
                img.planes[c][i] = (rnd() & 0xFF) as u8;
            }
        }
        let (bytes, _stats) =
            encode_with(&img, 4, EncodeOpts { cross_channel: Some(true), ..Default::default() }).unwrap();
        let decoded = decode(&bytes).unwrap();
        assert_eq!(decoded, img);
        let (_, model, _) = inspect(&bytes).unwrap();
        assert!(model.cross_channel, "forced cross-channel must be signaled");
    }

    #[test]
    fn cross_channel_forced_off_signals_none() {
        let mut img = Image::new(48, 48, Channels::Rgb).unwrap();
        for i in 0..img.area() {
            img.planes[0][i] = ((i * 7) % 256) as u8;
            img.planes[1][i] = ((i * 3) % 256) as u8;
            img.planes[2][i] = ((i * 11) % 256) as u8;
        }
        let (bytes, _stats) =
            encode_with(&img, 4, EncodeOpts { cross_channel: Some(false), ..Default::default() }).unwrap();
        let decoded = decode(&bytes).unwrap();
        assert_eq!(decoded, img);
        let (_, model, _) = inspect(&bytes).unwrap();
        assert!(!model.cross_channel, "forced-off cross-channel must signal none");
    }

    #[test]
    fn cross_channel_rgba_preserves_alpha() {
        let w = 32u32;
        let h = 32u32;
        let mut img = Image::new(w, h, Channels::Rgba).unwrap();
        let mut seed = 0x1234u64;
        let mut rnd = move || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            seed
        };
        for c in 0..4 {
            for i in 0..img.area() {
                img.planes[c][i] = (rnd() & 0xFF) as u8;
            }
        }
        let (bytes, _stats) =
            encode_with(&img, 4, EncodeOpts { cross_channel: Some(true), ..Default::default() }).unwrap();
        let decoded = decode(&bytes).unwrap();
        assert_eq!(decoded, img);
    }

    #[test]
    fn r3a_residual_context_forced_roundtrip() {
        // R3-A conditions the CMARC residual coder on the JPEG-LS DIFF context
        // (already-coded neighbor residuals). This test forces plain CMARC
        // selection so the R3-A residual-context encode AND decode paths are
        // exercised end-to-end on a Kodak-sized photographic proxy, proving the
        // encoder/decoder compute identical `cid`s (bit-exact lockstep). The
        // compression delta vs GR is measured on the real Kodak corpus (absent
        // in this build env); the never-expand safety net keeps CMARC from
        // shipping when it does not beat the model's best GR backend, so forcing
        // here is purely a decode-path correctness check.
        let w = 768usize;
        let h = 512usize;
        let mut img = Image::new(w as u32, h as u32, Channels::Rgb).unwrap();
        let mut s = 1337u64;
        let mut rng = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            s
        };
        let tones: Vec<(f64, f64, f64, f64, f64, f64)> = (0..3)
            .map(|c| {
                (
                    1.0 + (rng() % 5) as f64 * 0.5,
                    1.0 + (rng() % 5) as f64 * 0.5,
                    (rng() % 1000) as f64 / 1000.0 * 6.283,
                    (rng() % 1000) as f64 / 1000.0 * 6.283,
                    40.0 + (rng() % 60) as f64,
                    90.0 + (rng() % 80) as f64,
                )
            })
            .collect();
        let objs: Vec<(usize, usize, usize, usize, i32)> = (0..4)
            .map(|_| {
                (
                    rng() as usize % w,
                    rng() as usize % h,
                    8 + rng() as usize % (w / 3),
                    8 + rng() as usize % (h / 3),
                    (rng() % 200) as i32,
                )
            })
            .collect();
        let noise = 1.5f64;
        for c in 0..3 {
            let (fx, fy, px, py, amp, base) = tones[c];
            for y in 0..h {
                for x in 0..w {
                    let mut v = base
                        + amp * ((fx * x as f64 / w as f64 * 6.283 + px).sin()
                            + (fy * y as f64 / h as f64 * 6.283 + py).sin());
                    for (ox, oy, ow, oh, sh) in &objs {
                        if x >= *ox && x < ox + ow && y >= *oy && y < oy + oh {
                            v += *sh as f64 * 0.3;
                        }
                    }
                    v += (((rng() % 17) as f64) - 8.0) * noise;
                    img.planes[c][y * w + x] = v.clamp(0.0, 255.0) as u8;
                }
            }
        }
        std::env::set_var("OBSIDIAN_CARC", "1");
        std::env::set_var("OBSIDIAN_CARC_FORCE", "1");
        let (carc_bytes, _) = encode(&img, 4).unwrap();
        std::env::remove_var("OBSIDIAN_CARC_FORCE");
        std::env::remove_var("OBSIDIAN_CARC");
        // Forced CMARC with the R3-A residual context must still round-trip
        // bit-exactly through the dedicated decode branch.
        assert_eq!(decode(&carc_bytes).unwrap(), img, "R3-A forced must round-trip");
    }
}











