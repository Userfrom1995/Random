//! The effort-driven encode pipeline.
//!
//! `encode` validates the image, picks the model (activity resolution,
//! predictor map, transform, optional palette), codes each channel plane with
//! adaptive rANS, and assembles the container. Effort changes only how the
//! encoder searches: the bitstream meaning is identical for every effort.

use crate::color::{ycocg_r_forward, Palette};
use crate::container::{self, write_map_rle, Flags, Header, ModelInfo, MAGIC, VERSION};
use crate::context::{context_of, max_context, zigzag};
use crate::error::{CodecError, CodecResult};
use crate::image::{Image, Plane};
use crate::predict::{self, selector_split};
use crate::rans::{encode_symbol, RansWriter};
use crate::select::{analyze_map, default_map, med_map};
use crate::stats::{EncodeStats, TransformChoice};
use crate::tables::{RansTable, RANS_L};

/// The effort knob. Higher effort spends more encoder time searching the
/// model; the decode cost is identical for all efforts.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Effort {
    E0,
    E1,
    E2,
    E3,
    E4,
    E5,
    E6,
    E7,
}

impl Effort {
    pub fn from_u8(e: u8) -> CodecResult<Effort> {
        Ok(match e {
            0 => Effort::E0,
            1 => Effort::E1,
            2 => Effort::E2,
            3 => Effort::E3,
            4 => Effort::E4,
            5 => Effort::E5,
            6 => Effort::E6,
            7 => Effort::E7,
            _ => return Err(CodecError::InvalidEffort(e)),
        })
    }

    pub fn as_u8(self) -> u8 {
        match self {
            Effort::E0 => 0,
            Effort::E1 => 1,
            Effort::E2 => 2,
            Effort::E3 => 3,
            Effort::E4 => 4,
            Effort::E5 => 5,
            Effort::E6 => 6,
            Effort::E7 => 7,
        }
    }
}

/// Encoded output: container bytes plus encode-time statistics.
#[derive(Debug, Clone)]
pub struct Encoded {
    pub bytes: Vec<u8>,
    pub stats: EncodeStats,
}

struct Model {
    classes: usize,
    analysis: bool,
    palette_trial: bool,
}

fn model_for(effort: Effort) -> Model {
    match effort {
        Effort::E0 => Model { classes: 1, analysis: false, palette_trial: false },
        Effort::E1 => Model { classes: 1, analysis: false, palette_trial: false },
        Effort::E2 => Model { classes: 2, analysis: false, palette_trial: false },
        Effort::E3 => Model { classes: 4, analysis: false, palette_trial: false },
        Effort::E4 => Model { classes: 2, analysis: true, palette_trial: false },
        Effort::E5 => Model { classes: 4, analysis: true, palette_trial: false },
        Effort::E6 => Model { classes: 4, analysis: true, palette_trial: true },
        Effort::E7 => Model { classes: 4, analysis: true, palette_trial: true },
    }
}

/// Encode an image to the Obsidian container format.
pub fn encode(image: &Image, effort: Effort) -> CodecResult<Encoded> {
    if image.width == 0 || image.height == 0 {
        return Err(CodecError::InvalidDimensions(image.width, image.height));
    }
    let model = model_for(effort);

    // Plain (direct) encode.
    let direct = encode_inner(image, effort, model.classes, model.analysis, None)?;

    // Palette trial at high effort for RGB images with few distinct colors.
    if model.palette_trial && image.channels == 3 {
        let (r, g, b) = (&image.planes[0].data, &image.planes[1].data, &image.planes[2].data);
        if let Some(pal) = Palette::from_image_rgb(image.width, image.height, r, g, b) {
            if let Ok(idx) = pal.index_plane(r, g, b) {
                let idx_plane = Plane::new(image.width, image.height, idx)?;
                let pal_img = Image::from_planes(image.width, image.height, 1, 8, vec![idx_plane])?;
                let pal_enc = encode_inner(&pal_img, effort, model.classes, model.analysis, Some(pal))?;
                if pal_enc.bytes.len() < direct.bytes.len() {
                    return Ok(pal_enc);
                }
            }
        }
    }
    Ok(direct)
}

fn encode_inner(
    image: &Image,
    effort: Effort,
    classes: usize,
    analysis: bool,
    palette: Option<Palette>,
) -> CodecResult<Encoded> {
    // Working planes.
    let mut planes: Vec<Plane>;
    let transform: TransformChoice;
    let mut palette_out: Option<Palette> = None;

    match palette {
        Some(pal) => {
            // Image is the single index plane.
            planes = image.planes.clone();
            transform = TransformChoice::Palette;
            palette_out = Some(pal);
        }
        None => {
            planes = image.planes.clone();
            if image.channels == 3 {
                ycocg_r_forward(&mut planes);
                transform = TransformChoice::YCoCgR;
            } else {
                transform = TransformChoice::None;
            }
        }
    }

    // Predictor map.
    let map: Vec<u8> = if effort == Effort::E0 {
        med_map(classes)
    } else if analysis {
        analyze_map(&planes, classes)?
    } else {
        default_map(classes)
    };

    // CRC over the raw source planes.
    let crc: u32 = {
        let mut raw = Vec::with_capacity(image.planes.iter().map(|p| p.len()).sum::<usize>());
        for p in &image.planes {
            raw.extend_from_slice(&p.data);
        }
        container::crc32(&raw)
    };

    let mut stats = EncodeStats {
        bytes: 0,
        bpp: 0.0,
        effort: effort.as_u8(),
        transform,
        per_plane_bytes: Vec::new(),
        predictor_histogram: [0u32; 8],
        contexts_used: 0,
        activity_classes: classes,
    };

    // Assemble header.
    let mut flags: u8 = match image.channels {
        1 => container::CHANNELS_GRAY,
        3 => container::CHANNELS_RGB,
        4 => container::CHANNELS_RGBA,
        _ => return Err(CodecError::InvalidChannels(image.channels)),
    };
    if transform == TransformChoice::YCoCgR {
        flags |= Flags::TRANSFORM;
    }
    if palette_out.is_some() {
        flags |= Flags::PALETTE;
    }
    let activity_mode = match classes {
        1 => 0,
        2 => 1,
        _ => 2,
    };
    let header = Header {
        magic: MAGIC,
        version: VERSION,
        flags,
        bit_depth: 8,
        effort: effort.as_u8(),
        width: image.width,
        height: image.height,
        crc32: crc,
    };

    let mut out = Vec::with_capacity(64 + image.width as usize * image.height as usize + 1024);
    container::write_header(&header, &mut out);
    out.push(planes.len() as u8); // num_planes
    out.push(if transform == TransformChoice::YCoCgR { 1 } else { 0 });
    out.push(ModelInfo { activity_mode, static_tables: false }.activity_mode);
    out.push(if palette_out.is_some() { 1 } else { 0 });
    // Palette data.
    if let Some(pal) = &palette_out {
        out.extend_from_slice(&(pal.colors.len() as u16).to_be_bytes());
        for c in &pal.colors {
            out.extend_from_slice(c);
        }
    }
    write_map_rle(&map, &mut out);

    // Encode each plane and append length-prefixed payloads.
    for plane in &planes {
        let payload = code_plane(plane, &map, classes, &mut stats);
        out.extend_from_slice(&(payload.len() as u32).to_be_bytes());
        out.extend_from_slice(&payload);
    }

    stats.bytes = out.len();
    let pixels = image.width as usize * image.height as usize;
    stats.bpp = if pixels == 0 { 0.0 } else { 8.0 * out.len() as f64 / pixels as f64 };

    Ok(Encoded { bytes: out, stats })
}

fn code_plane(plane: &Plane, map: &[u8], classes: usize, stats: &mut EncodeStats) -> Vec<u8> {
    let total_ctx = max_context(classes);
    let n = plane.len();
    let mut tables: Vec<Option<RansTable>> = Vec::with_capacity(total_ctx);
    tables.resize_with(total_ctx, || None);
    let mut tables_used = 0usize;
    let mut writer = RansWriter::with_capacity(n);
    let mut x = RANS_L;
    let w = plane.w as i64;
    let h = plane.h as i64;

    for y in 0..h {
        for xp in 0..w {
            let ctx = context_of(plane, xp, y, classes);
            if tables[ctx].is_none() {
                tables[ctx] = Some(RansTable::new());
                tables_used += 1;
            }
            let table = tables[ctx].as_mut().expect("table just initialized");
            let sel = map[ctx];
            let (pred_id, w_idx) = selector_split(sel);
            stats.predictor_histogram[pred_id as usize] += 1;
            let pred = predict::predict(plane, xp, y, pred_id, w_idx);
            let r = plane.pixel(xp, y).wrapping_sub(pred);
            let u = zigzag(r) as usize;
            encode_symbol(&mut writer, table, &mut x, u);
        }
    }

    let payload = writer.finish(x);
    stats.per_plane_bytes.push(payload.len());
    stats.contexts_used = stats.contexts_used.max(tables_used);
    payload
}
