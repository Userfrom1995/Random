//! Obsidian web bindings (wasm32).
//!
//! A hand-rolled, dependency-free ABI that exports the codec core to
//! JavaScript through the wasm linear memory. No wasm-bindgen: the specimen
//! page calls `obsd_alloc`/`obsd_encode`/`obsd_decode` directly and copies
//! arrays across the boundary as explicit buffers. The core codec library is
//! reused unchanged.
//!
//! On non-wasm targets this crate compiles to an empty cdylib so the
//! workspace builds on the host for tests.

#[cfg(target_arch = "wasm32")]
mod wasm_api {
    use obsidian_core::{decode, encode, image::Image, Effort};
    use std::alloc::{alloc, dealloc, Layout};

    /// Allocate a byte buffer in wasm linear memory for the caller.
    #[no_mangle]
    pub extern "C" fn obsd_alloc(len: usize) -> *mut u8 {
        if len == 0 {
            return std::ptr::null_mut();
        }
        let layout = match Layout::from_size_align(len, 1) {
            Ok(l) => l,
            Err(_) => return std::ptr::null_mut(),
        };
        unsafe { alloc(layout) }
    }

    /// Free a buffer allocated by `obsd_alloc`.
    #[no_mangle]
    pub extern "C" fn obsd_dealloc(ptr: *mut u8, len: usize) {
        if ptr.is_null() || len == 0 {
            return;
        }
        let layout = match Layout::from_size_align(len, 1) {
            Ok(l) => l,
            Err(_) => return,
        };
        unsafe { dealloc(ptr, layout) }
    }

    /// Encode an RGBA8 image into `out` (capacity `out_cap`). Returns the
    /// encoded byte count, or a negative error code.
    #[no_mangle]
    pub extern "C" fn obsd_encode(
        src: *const u8,
        src_len: usize,
        width: u32,
        height: u32,
        channels: u8,
        effort: u8,
        out: *mut u8,
        out_cap: usize,
    ) -> i32 {
        if src.is_null() || out.is_null() {
            return -1;
        }
        let rgba = unsafe { std::slice::from_raw_parts(src, src_len) };
        let img = match Image::from_rgba8(width, height, channels, rgba) {
            Ok(i) => i,
            Err(_) => return -2,
        };
        let e = match Effort::from_u8(effort) {
            Ok(e) => e,
            Err(_) => return -3,
        };
        match encode(&img, e) {
            Ok(enc) => {
                if enc.bytes.len() > out_cap {
                    return -4;
                }
                unsafe {
                    std::ptr::copy_nonoverlapping(enc.bytes.as_ptr(), out, enc.bytes.len());
                }
                enc.bytes.len() as i32
            }
            Err(_) => -5,
        }
    }

    /// Decode an Obsidian container into RGBA8. Writes dimensions and channel
    /// count into the provided out-pointers. Returns the number of RGBA bytes
    /// written, or a negative error code.
    #[no_mangle]
    pub extern "C" fn obsd_decode(
        src: *const u8,
        src_len: usize,
        out: *mut u8,
        out_cap: usize,
        out_w: *mut u32,
        out_h: *mut u32,
        out_channels: *mut u8,
    ) -> i32 {
        if src.is_null() || out.is_null() {
            return -1;
        }
        let bytes = unsafe { std::slice::from_raw_parts(src, src_len) };
        match decode(bytes) {
            Ok(img) => {
                let n = img.width as usize * img.height as usize;
                let rgba_len = n * 4;
                if rgba_len > out_cap {
                    return -4;
                }
                for i in 0..n {
                    for c in 0..img.channels as usize {
                        out[i * 4 + c] = img.planes[c].data[i];
                    }
                    for c in img.channels as usize..4 {
                        out[i * 4 + c] = 255;
                    }
                }
                unsafe {
                    *out_w = img.width;
                    *out_h = img.height;
                    *out_channels = img.channels;
                }
                rgba_len as i32
            }
            Err(_) => -5,
        }
    }
}
