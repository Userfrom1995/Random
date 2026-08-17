//! The decode pipeline.
//!
//! `decode` validates every length against the remaining byte budget before
//! allocating, reconstructs the model exactly as the encoder did (adaptive
//! tables are updated identically on both sides), inverts every stage, and
//! hard-gates the result with the header CRC. It never panics on untrusted
//! input; every malformed stream produces a [`CodecError`].

use crate::color::{ycocg_r_inverse, Palette};
use crate::container::{self, read_map_rle, Flags};
use crate::context::{context_of, max_context, unzigzag};
use crate::error::{CodecError, CodecResult};
use crate::image::{Image, Plane};
use crate::predict::{self, selector_split};
use crate::rans::{decode_symbol, RansReader};
use crate::tables::RansTable;

/// Decode an Obsidian container back to an [`Image`].
pub fn decode(bytes: &[u8]) -> CodecResult<Image> {
    let header = container::read_header(bytes)?;
    let mut pos = container::HEADER_LEN;

    let num_planes = read_byte(bytes, &mut pos)?;
    if !matches!(num_planes, 1 | 2 | 3 | 4) {
        return Err(CodecError::CorruptContainer);
    }
    let transform_byte = read_byte(bytes, &mut pos)?;
    if transform_byte > 1 {
        return Err(CodecError::CorruptContainer);
    }
    let model_byte = read_byte(bytes, &mut pos)?;
    if model_byte & 0b1111_1100 != 0 {
        return Err(CodecError::CorruptContainer);
    }
    let classes = match model_byte & 0b11 {
        0 => 1,
        1 => 2,
        _ => 4,
    };
    let palette_flag = read_byte(bytes, &mut pos)?;
    if palette_flag > 1 {
        return Err(CodecError::CorruptContainer);
    }
    let palette = if palette_flag == 1 {
        let count = read_u16(bytes, &mut pos)? as usize;
        if count == 0 || count > 256 {
            return Err(CodecError::BadPalette);
        }
        if pos + count * 3 > bytes.len() {
            return Err(CodecError::Truncated);
        }
        let mut colors = Vec::with_capacity(count);
        for _ in 0..count {
            colors.push([bytes[pos], bytes[pos + 1], bytes[pos + 2]]);
            pos += 3;
        }
        Some(Palette { colors })
    } else {
        None
    };

    // Predictor map.
    let map_len = max_context(classes);
    let map = read_map_rle(bytes, &mut pos, map_len)?;

    // Decode each plane payload.
    let n = header.width as usize * header.height as usize;
    let mut planes = Vec::with_capacity(num_planes as usize);
    for _ in 0..num_planes as usize {
        let len = read_u32(bytes, &mut pos)? as usize;
        if len < 4 || pos + len > bytes.len() {
            return Err(CodecError::Truncated);
        }
        let payload = &bytes[pos..pos + len];
        pos += len;
        let data = decode_plane(payload, n, header.width, header.height, &map, classes)?;
        planes.push(Plane::new(header.width, header.height, data)?);
    }

    // Reconstruct the raw image.
    let channels = container::channels_from_flags(header.flags);
    let image = if let Some(pal) = palette {
        // The single plane is a palette index plane.
        if planes.len() != 1 {
            return Err(CodecError::CorruptContainer);
        }
        let (r, g, b) = pal.unindex(&planes[0].data)?;
        Image::rgb(header.width, header.height, r, g, b)?
    } else {
        if planes.len() != channels as usize {
            return Err(CodecError::CorruptContainer);
        }
        if header.flags & Flags::TRANSFORM != 0 {
            if channels != 3 {
                return Err(CodecError::CorruptContainer);
            }
            let mut p = planes;
            ycocg_r_inverse(&mut p);
            Image::from_planes(header.width, header.height, channels, 8, p)?
        } else {
            Image::from_planes(header.width, header.height, channels, 8, planes)?
        }
    };

    // CRC hard gate over the raw planes.
    let mut raw = Vec::with_capacity(image.planes.iter().map(|p| p.len()).sum::<usize>());
    for p in &image.planes {
        raw.extend_from_slice(&p.data);
    }
    if container::crc32(&raw) != header.crc32 {
        return Err(CodecError::CrcMismatch);
    }

    Ok(image)
}

/// Decode a single plane payload of `n` pixels into a raster buffer.
fn decode_plane(
    payload: &[u8],
    n: usize,
    width: u32,
    height: u32,
    map: &[u8],
    classes: usize,
) -> CodecResult<Vec<u8>> {
    let total_ctx = max_context(classes);
    let mut tables: Vec<Option<RansTable>> = Vec::with_capacity(total_ctx);
    tables.resize_with(total_ctx, || None);
    let mut inp = RansReader::new(payload);
    let mut x = inp.init_state()?;

    // The plane is decoded in raster order; `causal_pixel` only reads pixels
    // already decoded, so a partially filled buffer is a valid view.
    let mut plane = Plane::new(width, height, vec![0u8; n])?;
    let w = width as i64;
    let h = height as i64;

    for y in 0..h {
        for xp in 0..w {
            let ctx = context_of(&plane, xp, y, classes);
            if tables[ctx].is_none() {
                tables[ctx] = Some(RansTable::new());
            }
            let table = tables[ctx].as_mut().expect("table just initialized");
            let sel = map[ctx];
            let (pred_id, w_idx) = selector_split(sel);
            let pred = predict::predict(&plane, xp, y, pred_id, w_idx);
            let u = decode_symbol(&mut inp, table, &mut x)?;
            let r = unzigzag(u as u16);
            let idx = (y as usize) * (width as usize) + (xp as usize);
            plane.data[idx] = pred.wrapping_add(r);
        }
    }
    Ok(plane.data)
}

fn read_byte(bytes: &[u8], pos: &mut usize) -> CodecResult<u8> {
    let b = *bytes.get(*pos).ok_or(CodecError::Truncated)?;
    *pos += 1;
    Ok(b)
}

fn read_u16(bytes: &[u8], pos: &mut usize) -> CodecResult<u16> {
    if *pos + 2 > bytes.len() {
        return Err(CodecError::Truncated);
    }
    let v = u16::from_be_bytes([bytes[*pos], bytes[*pos + 1]]);
    *pos += 2;
    Ok(v)
}

fn read_u32(bytes: &[u8], pos: &mut usize) -> CodecResult<u32> {
    if *pos + 4 > bytes.len() {
        return Err(CodecError::Truncated);
    }
    let v = u32::from_be_bytes([bytes[*pos], bytes[*pos + 1], bytes[*pos + 2], bytes[*pos + 3]]);
    *pos += 4;
    Ok(v)
}
