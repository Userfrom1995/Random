//! Obsidian: a lossless image codec built from scratch.
//!
//! The core library implements the v1 specification: a container format with
//! header CRC, a reversible YCoCg-R color transform, an 8-predictor causal
//! bank with per-context selection, a JPEG-LS-style gradient context model
//! with activity classes and border regions, and adaptive 12-bit rANS
//! entropy coding.
//!
//! Standard library only; the encoder is `encode(&Image, Effort)`, the
//! decoder `decode(&[u8])`. Fidelity is guaranteed by construction (every
//! stage is an integer bijection) and hard-gated at decode by the header CRC.
//!
//! ```rust
//! let img = obsidian_core::image::Image::gray(2, 2, vec![1, 2, 3, 4]).unwrap();
//! let enc = obsidian_core::encode(&img, obsidian_core::Effort::E3).unwrap();
//! let dec = obsidian_core::decode(&enc.bytes).unwrap();
//! assert_eq!(img, dec);
//! ```

pub mod color;
pub mod container;
pub mod context;
pub mod decoder;
pub mod encoder;
pub mod error;
pub mod image;
pub mod predict;
pub mod rans;
pub mod select;
pub mod stats;
pub mod tables;

pub use decoder::decode;
pub use encoder::{encode, Effort, Encoded};
pub use error::{CodecError, CodecResult};
pub use stats::{EncodeStats, TransformChoice};
