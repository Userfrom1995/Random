//! Command surface: strict argument validation, no interactive input.

use obsidian_core::{
    decode, encode, encode_with, roundtrip, EncodeOpts,
    predict::PredictorId,
};
use std::path::PathBuf;
use std::time::Instant;

pub fn run(args: Vec<String>) -> i32 {
    let sub = match args.first() {
        Some(s) => s.as_str(),
        None => {
            eprintln!("obsidian: missing subcommand");
            usage();
            return 1;
        }
    };
    let rest = &args[1..];
    match sub {
        "encode" => cmd_encode(rest),
        "decode" => cmd_decode(rest),
        "roundtrip" => cmd_roundtrip(rest),
        "selftest" => cmd_selftest(rest),
        "check" => cmd_check(rest),
        "bench" => crate::bench::cmd_bench(rest),
        "bench-synth" => crate::bench::cmd_bench_synth(rest),
        "gpu-list" => cmd_gpu_list(rest),
        "help" | "-h" | "--help" => {
            usage();
            0
        }
        _ => {
            eprintln!("obsidian: unknown subcommand '{sub}'");
            usage();
            1
        }
    }
}

fn usage() {
    eprintln!(
        "usage:\n  obsidian encode <in-image> <out.obsd> [--effort N] [--tile N] [--gpu [NAME]] [--json]\n  obsidian decode <in.obsd> <out-image>\n  obsidian roundtrip <in-image> [--effort N] [--json]\n  obsidian selftest [--fuzz N]\n  obsidian check <in.obsd>\n  obsidian bench <image-dir> [--effort N] [--json]\n  obsidian bench-synth [--effort N] [--count N] [--size N] [--seed N]\n  obsidian gpu-list\n\n  --tile 256 splits into 256x256 tiled OBST for parallel encode (rayon, <0.1 bpp loss at 256)\n  --gpu without value uses HighPerformance (RTX 4050); with NAME picks that adapter (see gpu-list)\n  <in-image>/<out-image> may be any of: {} (extension selects format); .obsd/.obst is the codec container.",
        crate::image_io::supported_formats_hint()
    );
}

fn cmd_gpu_list(_args: &[String]) -> i32 {
    let gpus = obsidian_gpu::list_gpus();
    if gpus.is_empty() {
        println!("no GPU adapters found (wgpu returned 0, or built without --features gpu)");
        println!("cpu fallback will be used; for GPU build: cargo build -p obsidian_cli --features gpu or use obsidian_gpu crate");
        return 0;
    }
    for g in &gpus {
        println!("{} [{} {}]", g.name, g.backend, g.device_type);
    }
    0
}

fn parse_effort(rest: &[String]) -> Result<(u8, bool, Vec<String>), i32> {
    let mut effort = 4u8;
    let mut json = false;
    let mut positional: Vec<String> = Vec::new();
    let mut it = rest.iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--effort" | "-e" => match it.next() {
                Some(v) => match v.parse::<u8>() {
                    Ok(e) if e <= 7 => effort = e,
                    _ => {
                        eprintln!("obsidian: --effort must be an integer in 0..=7");
                        return Err(1);
                    }
                },
                None => {
                    eprintln!("obsidian: --effort requires a value");
                    return Err(1);
                }
            },
            "--json" => json = true,
            _ => positional.push(a.clone()),
        }
    }
    Ok((effort, json, positional))
}

fn parse_encode_args(rest: &[String]) -> Result<(u8, usize, Option<Option<String>>, bool, Vec<String>), i32> {
    let mut effort = 4u8;
    let mut tile: usize = 0;
    let mut gpu: Option<Option<String>> = None; // None = no --gpu, Some(None)= --gpu without name, Some(Some(name))= --gpu <name>
    let mut json = false;
    let mut positional: Vec<String> = Vec::new();
    let mut it = rest.iter().peekable();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--effort" | "-e" => match it.next() {
                Some(v) => match v.parse::<u8>() {
                    Ok(e) if e <= 7 => effort = e,
                    _ => { eprintln!("obsidian: --effort must be an integer in 0..=7"); return Err(1); }
                },
                None => { eprintln!("obsidian: --effort requires a value"); return Err(1); }
            },
            "--tile" => match it.next() {
                Some(v) => match v.parse::<usize>() {
                    Ok(n) => tile = n,
                    _ => { eprintln!("obsidian: --tile must be an integer (e.g. 256)"); return Err(1); }
                },
                None => { eprintln!("obsidian: --tile requires a value"); return Err(1); }
            },
            "--gpu" => {
                // --gpu may be followed by a name that does not start with -
                let name = match it.peek() {
                    Some(n) if !n.starts_with('-') => Some(it.next().unwrap().clone()),
                    _ => None,
                };
                gpu = Some(name);
            },
            "--json" => json = true,
            _ => positional.push(a.clone()),
        }
    }
    Ok((effort, tile, gpu, json, positional))
}

fn read_image_file(path: &PathBuf) -> Result<obsidian_core::image::Image, i32> {
    crate::image_io::read_image(path)
}

fn write_image_file(path: &PathBuf, img: &obsidian_core::image::Image) -> Result<(), i32> {
    crate::image_io::write_image(path, img)
}

fn cmd_encode(args: &[String]) -> i32 {
    let (effort, mut tile, gpu, json, positional) = match parse_encode_args(args) {
        Ok(v) => v,
        Err(c) => return c,
    };
    if positional.len() != 2 {
        eprintln!("obsidian: encode requires <in-image> <out.obsd>");
        usage();
        return 1;
    }
    let in_path = PathBuf::from(&positional[0]);
    let out_path = PathBuf::from(&positional[1]);
    let image = match read_image_file(&in_path) {
        Ok(i) => i,
        Err(c) => return c,
    };
    // If --gpu is requested without --tile, default to 256 tiled for parallel GPU dispatch
    if gpu.is_some() && tile == 0 {
        tile = 256;
    }
    // Validate --gpu name if given
    if let Some(Some(ref name)) = gpu {
        let gpus = obsidian_gpu::list_gpus();
        if !gpus.is_empty() && !gpus.iter().any(|g| &g.name == name) {
            eprintln!("obsidian: --gpu adapter '{}' not found. available:", name);
            for g in &gpus { eprintln!("  {} [{} {}]", g.name, g.backend, g.device_type); }
            return 1;
        }
        // Warm up the selected adapter so the tiled path is hot
        let mut dummy = vec![vec![0i16; 1], vec![0i16; 1], vec![0i16; 1]];
        let _ = obsidian_gpu::ycocg_forward_gpu_with_name(&mut dummy, Some(name.as_str()));
    } else if let Some(None) = gpu {
        // --gpu without name: just probe HighPerformance
        let _ = obsidian_gpu::is_gpu_available();
    }
    let start = Instant::now();
    let gpu_name_opt: Option<&str> = match &gpu {
        Some(Some(name)) => Some(name.as_str()),
        Some(None) => None,
        None => None,
    };
    let use_gpu = gpu.is_some();
    if use_gpu && std::env::var("OBSIDIAN_GPU_DEBUG").ok().as_deref() != Some("1") {
        // Always log which GPU will be used when --gpu is explicitly requested, even without DEBUG
        let gpus = obsidian_gpu::list_gpus();
        if let Some(Some(name)) = &gpu {
            eprintln!("[GPU] encode using explicit adapter '{}'", name);
        } else if !gpus.is_empty() {
            let hp = gpus.iter().find(|g| g.device_type.contains("DiscreteGpu")).or_else(|| gpus.first()).unwrap();
            eprintln!("[GPU] encode using HighPerformance: {} [{} {}]", hp.name, hp.backend, hp.device_type);
        } else {
            eprintln!("[GPU] encode: --gpu requested but no adapter found, CPU fallback");
        }
    }
    let (bytes, stats) = if tile != 0 {
        if use_gpu {
            match obsidian_gpu::encode_tiled_with_gpu(&image, effort, tile, gpu_name_opt) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("obsidian: encode_tiled failed: {e}");
                    return 1;
                }
            }
        } else {
            match obsidian_gpu::encode_tiled(&image, effort, tile) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("obsidian: encode_tiled failed: {e}");
                    return 1;
                }
            }
        }
    } else {
        match encode(&image, effort) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("obsidian: encode failed: {e}");
                return 1;
            }
        }
    };
    let encode_ms = start.elapsed().as_secs_f64() * 1000.0;
    if let Err(e) = std::fs::write(&out_path, &bytes) {
        eprintln!("obsidian: cannot write '{}': {e}", out_path.display());
        return 2;
    }
    if json {
        println!(
            "{{\"command\":\"encode\",\"in\":\"{}\",\"out\":\"{}\",\"effort\":{},\"bytes\":{},\"bpp\":{:.4},\"encode_ms\":{:.2}}}",
            in_path.display(),
            out_path.display(),
            effort,
            bytes.len(),
            stats.bpp,
            encode_ms
        );
    } else {
        println!(
            "encoded {} -> {} ({} bytes, {:.4} bpp, {:.2} ms)",
            in_path.display(),
            out_path.display(),
            bytes.len(),
            stats.bpp,
            encode_ms
        );
    }
    0
}

fn cmd_decode(args: &[String]) -> i32 {
    if args.len() != 2 {
        eprintln!("obsidian: decode requires <in.obsd> <out-image>");
        usage();
        return 1;
    }
    let in_path = PathBuf::from(&args[0]);
    let out_path = PathBuf::from(&args[1]);
    let data = match std::fs::read(&in_path) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("obsidian: cannot read '{}': {e}", in_path.display());
            return 2;
        }
    };
    let start = Instant::now();
    let image = match obsidian_gpu::decode_tiled(&data) {
        Ok(i) => i,
        Err(e) => {
            eprintln!("obsidian: decode failed: {e}");
            return 3;
        }
    };
    let decode_ms = start.elapsed().as_secs_f64() * 1000.0;
    if let Err(c) = write_image_file(&out_path, &image) {
        return c;
    }
    println!(
        "decoded {} -> {} ({}x{}, {:.2} ms)",
        in_path.display(),
        out_path.display(),
        image.width,
        image.height,
        decode_ms
    );
    0
}

fn cmd_roundtrip(args: &[String]) -> i32 {
    // R13-A measurement seam: `--predictor <NAME>` forces a single predictor for
    // the whole image so its standalone potential (vs the never-expand net) can be
    // measured directly. Unrecognized names fall back to the default analyzer.
    let mut forced: Option<PredictorId> = None;
    // R13-B measurement seam: `--transform lift|squeeze` forces the reversible
    // group transform kind so R13-B (CDF 5/3 lifting) can be measured directly.
    let mut forced_transform: Option<obsidian_core::transforms::TransformKind> = None;
    let mut rest = args.to_vec();
    if let Some(pos) = rest.iter().position(|a| a == "--predictor") {
        if pos + 1 < rest.len() {
            let name = rest[pos + 1].as_str();
            forced = PredictorId::from_name(name);
            rest.remove(pos + 1);
            rest.remove(pos);
        }
    }
    if let Some(pos) = rest.iter().position(|a| a == "--transform") {
        if pos + 1 < rest.len() {
            forced_transform = match rest[pos + 1].as_str() {
                "lift" => Some(obsidian_core::transforms::TransformKind::Lift),
                "squeeze" => Some(obsidian_core::transforms::TransformKind::Squeeze),
                other => {
                    eprintln!("obsidian: --transform expects 'lift' or 'squeeze' (got '{other}')");
                    return 1;
                }
            };
            rest.remove(pos + 1);
            rest.remove(pos);
        }
    }
    // R15 measurement seam: `--nrp` enables the learned neural residual predictor
    // as a candidate in the never-expand safety net (mirrors `--predictor`).
    let mut nrp = false;
    if let Some(pos) = rest.iter().position(|a| a == "--nrp") {
        nrp = true;
        rest.remove(pos);
    }
    let (effort, json, positional) = match parse_effort(&rest) {
        Ok(v) => v,
        Err(c) => return c,
    };
    if positional.len() != 1 {
        eprintln!("obsidian: roundtrip requires <in-image>");
        usage();
        return 1;
    }
    let in_path = PathBuf::from(&positional[0]);
    let image = match read_image_file(&in_path) {
        Ok(i) => i,
        Err(c) => return c,
    };
    let result = if forced.is_some() || forced_transform.is_some() {
        encode_with(
            &image,
            effort,
            EncodeOpts {
                forced_predictor: forced,
                transform_kind: forced_transform,
                nrp: if nrp { Some(true) } else { None },
                ..Default::default()
            },
        )
        .and_then(|(bytes, stats)| {
            let back = decode(&bytes)?;
            Ok((bytes, stats, back))
        })
    } else {
        roundtrip(&image, effort)
    };
    match result {
        Ok((bytes, stats, back)) => {
            if back != image {
                eprintln!("obsidian: fidelity failure (image differs)");
                return 3;
            }
            if json {
                println!(
                    "{{\"command\":\"roundtrip\",\"in\":\"{}\",\"effort\":{},\"bytes\":{},\"bpp\":{:.4},\"encode_ms\":{:.2},\"decode_ms\":{:.2},\"fidelity\":\"ok\"}}",
                    in_path.display(),
                    effort,
                    bytes.len(),
                    stats.bpp,
                    stats.encode_ms,
                    stats.decode_ms
                );
            } else {
                println!(
                    "roundtrip ok: {} ({} bytes, {:.4} bpp, encode {:.2} ms, decode {:.2} ms, bit-exact)",
                    in_path.display(),
                    bytes.len(),
                    stats.bpp,
                    stats.encode_ms,
                    stats.decode_ms
                );
            }
            0
        }
        Err(e) => {
            eprintln!("obsidian: roundtrip failed: {e}");
            3
        }
    }
}

fn cmd_selftest(args: &[String]) -> i32 {
    let mut fuzz_count = 100usize;
    let mut it = args.iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--fuzz" => match it.next() {
                Some(v) => match v.parse::<usize>() {
                    Ok(n) if n >= 1 => fuzz_count = n,
                    _ => {
                        eprintln!("obsidian: --fuzz requires a positive integer");
                        return 1;
                    }
                },
                None => {
                    eprintln!("obsidian: --fuzz requires a value");
                    return 1;
                }
            },
            _ => {
                eprintln!("obsidian: selftest takes no positional arguments");
                return 1;
            }
        }
    }
    // Run the in-crate test suite (also compiled into the binary as a
    // library test harness would be heavier; we surface the fuzz gate here).
    let start = Instant::now();
    match obsidian_core::fuzz_gate(fuzz_count, &[0, 1, 4, 7]) {
        Ok(verified) => {
            println!(
                "selftest: {verified} fuzz round-trips bit-exact in {:.2} ms",
                start.elapsed().as_secs_f64() * 1000.0
            );
            0
        }
        Err(e) => {
            eprintln!("selftest failed: {e}");
            3
        }
    }
}

fn cmd_check(args: &[String]) -> i32 {
    if args.len() != 1 {
        eprintln!("obsidian: check requires <in.obsd>");
        usage();
        return 1;
    }
    let in_path = PathBuf::from(&args[0]);
    let data = match std::fs::read(&in_path) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("obsidian: cannot read '{}': {e}", in_path.display());
            return 2;
        }
    };
    let start = Instant::now();
    let image = match obsidian_gpu::decode_tiled(&data) {
        Ok(i) => i,
        Err(e) => {
            eprintln!("obsidian: check failed: {e}");
            return 3;
        }
    };
    let ms = start.elapsed().as_secs_f64() * 1000.0;
    println!(
        "check ok: {} -> {}x{} {} (CRC verified, {:.2} ms)",
        in_path.display(),
        image.width,
        image.height,
        match image.channels {
            obsidian_core::image::Channels::Gray => "gray",
            obsidian_core::image::Channels::Rgb => "rgb",
            obsidian_core::image::Channels::Rgba => "rgba",
        },
        ms
    );
    0
}
