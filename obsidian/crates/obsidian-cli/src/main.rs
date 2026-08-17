//! Obsidian command line tool.
//!
//! Subcommands:
//! - `encode <in.ppm> -o <out.obsd> [-e 0..7]`
//! - `decode <in.obsd> -o <out.ppm>`
//! - `verify <a> <b>` (byte-identity check, drives the fidelity gates)
//! - `info <in.obsd>`
//! - `bench --dir <dir> [-e 0..7] [-o <csv>]`
//!
//! Strict arg validation, non-zero exit on error, clean stdout for piping,
//! no interactive input.

use std::path::{Path, PathBuf};

use obsidian_core::{decode, encode, image::Image, CodecError, Effort};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match run(&args) {
        Ok(code) => std::process::exit(code),
        Err(msg) => {
            eprintln!("error: {msg}");
            std::process::exit(2);
        }
    }
}

fn usage() -> &'static str {
    "usage: obsidian <command> [options]\n\
     commands:\n\
       encode <in.ppm> -o <out.obsd> [-e 0..7]\n\
       decode <in.obsd> -o <out.ppm>\n\
       verify <a> <b>\n\
       info <in.obsd>\n\
       bench --dir <dir> [-e 0..7] [-o <csv>]\n\
     options:\n\
       -o <path>   output file\n\
       -e <0..7>   effort level (default 3)\n\
       -h, --help  show this help"
}

fn run(args: &[String]) -> Result<i32, String> {
    if args.is_empty() {
        return Err(usage().to_string());
    }
    match args[0].as_str() {
        "encode" => cmd_encode(&args[1..]),
        "decode" => cmd_decode(&args[1..]),
        "verify" => cmd_verify(&args[1..]),
        "info" => cmd_info(&args[1..]),
        "bench" => cmd_bench(&args[1..]),
        "-h" | "--help" => {
            println!("{}", usage());
            Ok(0)
        }
        other => Err(format!("unknown command '{other}'\n\n{}", usage())),
    }
}

fn read_file(path: &str) -> Result<Vec<u8>, String> {
    std::fs::read(path).map_err(|e| format!("cannot read '{path}': {e}"))
}

fn write_file(path: &str, bytes: &[u8]) -> Result<(), String> {
    std::fs::write(path, bytes).map_err(|e| format!("cannot write '{path}': {e}"))
}

fn parse_effort(s: &str) -> Result<Effort, String> {
    let e: u8 = s.parse().map_err(|_| format!("invalid effort '{s}'"))?;
    Effort::from_u8(e).map_err(|_| format!("invalid effort '{s}'"))
}

struct EncodeArgs {
    input: String,
    output: String,
    effort: Effort,
}

fn parse_encode_args(args: &[String]) -> Result<EncodeArgs, String> {
    let mut input = None;
    let mut output = None;
    let mut effort = Effort::E3;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "-o" => {
                i += 1;
                output = Some(args.get(i).ok_or("missing value after -o")?.clone());
            }
            "-e" => {
                i += 1;
                let v = args.get(i).ok_or("missing value after -e")?;
                effort = parse_effort(v)?;
            }
            "-h" | "--help" => return Err(usage().to_string()),
            a if a.starts_with('-') => return Err(format!("unknown option '{a}'")),
            a => {
                if input.is_some() {
                    return Err(format!("unexpected argument '{a}'"));
                }
                input = Some(a.to_string());
            }
        }
        i += 1;
    }
    Ok(EncodeArgs {
        input: input.ok_or("missing input file")?,
        output: output.ok_or("missing -o <out.obsd>")?,
        effort,
    })
}

fn cmd_encode(args: &[String]) -> Result<i32, String> {
    let a = parse_encode_args(args)?;
    let ppm = read_file(&a.input)?;
    let img = Image::from_ppm(&ppm).map_err(codec_err)?;
    let enc = encode(&img, a.effort).map_err(codec_err)?;
    write_file(&a.output, &enc.bytes)?;
    println!(
        "bytes={} bpp={:.4} effort={} transform={:?} contexts={} planes={}",
        enc.stats.bytes,
        enc.stats.bpp,
        enc.stats.effort,
        enc.stats.transform,
        enc.stats.contexts_used,
        enc.stats.per_plane_bytes.len()
    );
    Ok(0)
}

fn parse_single_input(args: &[String], cmd: &str) -> Result<(String, String), String> {
    let mut input = None;
    let mut output = None;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "-o" => {
                i += 1;
                output = Some(args.get(i).ok_or("missing value after -o")?.clone());
            }
            "-h" | "--help" => return Err(usage().to_string()),
            a if a.starts_with('-') => return Err(format!("unknown option '{a}'")),
            a => {
                if input.is_some() {
                    return Err(format!("unexpected argument '{a}'"));
                }
                input = Some(a.to_string());
            }
        }
        i += 1;
    }
    let input = input.ok_or(format!("missing input file for '{cmd}'"))?;
    let output = output.ok_or(format!("missing -o <out> for '{cmd}'"))?;
    Ok((input, output))
}

fn cmd_decode(args: &[String]) -> Result<i32, String> {
    let (input, output) = parse_single_input(args, "decode")?;
    let bytes = read_file(&input)?;
    let img = decode(&bytes).map_err(codec_err)?;
    let ppm = img.to_ppm();
    write_file(&output, &ppm)?;
    println!(
        "decoded {}x{} channels={} -> {} bytes",
        img.width,
        img.height,
        img.channels,
        ppm.len()
    );
    Ok(0)
}

fn cmd_verify(args: &[String]) -> Result<i32, String> {
    if args.len() != 2 || args.iter().any(|a| a.starts_with('-')) {
        return Err("usage: obsidian verify <a> <b>".to_string());
    }
    let a = read_file(&args[0])?;
    let b = read_file(&args[1])?;
    if a == b {
        println!("identical ({} bytes)", a.len());
        Ok(0)
    } else {
        eprintln!("differ: {}-byte vs {}-byte", a.len(), b.len());
        Ok(1)
    }
}

fn cmd_info(args: &[String]) -> Result<i32, String> {
    let (input, _) = parse_single_input(args, "info")?;
    let bytes = read_file(&input)?;
    let img = decode(&bytes).map_err(codec_err)?;
    println!(
        "obsidian container: {}x{} channels={} decoded-ok",
        img.width, img.height, img.channels
    );
    Ok(0)
}

fn parse_bench_args(args: &[String]) -> Result<(PathBuf, Effort, Option<PathBuf>), String> {
    let mut dir = None;
    let mut effort = Effort::E3;
    let mut out = None;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--dir" => {
                i += 1;
                dir = Some(args.get(i).ok_or("missing value after --dir")?.clone());
            }
            "-e" => {
                i += 1;
                let v = args.get(i).ok_or("missing value after -e")?;
                effort = parse_effort(v)?;
            }
            "-o" => {
                i += 1;
                out = Some(args.get(i).ok_or("missing value after -o")?.clone());
            }
            "-h" | "--help" => return Err(usage().to_string()),
            a if a.starts_with('-') => return Err(format!("unknown option '{a}'")),
            a => return Err(format!("unexpected argument '{a}'")),
        }
        i += 1;
    }
    let dir = dir.ok_or("missing --dir <dir>")?;
    Ok((PathBuf::from(dir), effort, out.map(PathBuf::from)))
}

fn cmd_bench(args: &[String]) -> Result<i32, String> {
    let (dir, effort, out_csv) = parse_bench_args(args)?;
    let mut entries: Vec<PathBuf> = std::fs::read_dir(&dir)
        .map_err(|e| format!("cannot read dir '{}': {e}", dir.display()))?
        .filter_map(|r| r.ok())
        .map(|e| e.path())
        .filter(|p| {
            p.extension().is_some_and(|e| e == "ppm" || e == "pgm" || e == "pnm")
        })
        .collect();
    entries.sort();

    let mut rows = Vec::new();
    rows.push(String::from("image,codec,bytes,bpp,enc_ms,dec_ms,effort,width,height,contexts"));
    for p in &entries {
        let ppm = std::fs::read(p).map_err(|e| format!("read {}: {e}", p.display()))?;
        let img = match Image::from_ppm(&ppm) {
            Ok(i) => i,
            Err(e) => {
                eprintln!("skip {}: {e}", p.display());
                continue;
            }
        };
        let t0 = std::time::Instant::now();
        let enc = match encode(&img, effort) {
            Ok(e) => e,
            Err(e) => {
                eprintln!("encode {}: {e}", p.display());
                continue;
            }
        };
        let enc_ms = t0.elapsed().as_secs_f64() * 1000.0;
        let t1 = std::time::Instant::now();
        let dec = match decode(&enc.bytes) {
            Ok(d) => d,
            Err(e) => {
                eprintln!("decode {}: {e}", p.display());
                continue;
            }
        };
        let dec_ms = t1.elapsed().as_secs_f64() * 1000.0;
        if dec != img {
            eprintln!("FIDELITY FAIL for {}", p.display());
            return Err("round-trip fidelity failure in bench".to_string());
        }
        let name = p.file_name().map(|f| f.to_string_lossy().to_string()).unwrap_or_default();
        rows.push(format!(
            "{name},obsidian,{},{:.4},{:.2},{:.2},{},{},{},{}",
            enc.stats.bytes,
            enc.stats.bpp,
            enc_ms,
            dec_ms,
            enc.stats.effort,
            img.width,
            img.height,
            enc.stats.contexts_used
        ));
    }

    let csv = rows.join("\n");
    match out_csv {
        Some(path) => {
            std::fs::write(&path, &csv).map_err(|e| format!("write {}: {e}", path.display()))?;
            println!("wrote {} rows to {}", rows.len() - 1, path.display());
        }
        None => println!("{csv}"),
    }
    Ok(0)
}

fn codec_err(e: CodecError) -> String {
    e.to_string()
}

// Keep Path import used across rustc versions.
#[allow(dead_code)]
fn _path_marker(_p: &Path) {}
