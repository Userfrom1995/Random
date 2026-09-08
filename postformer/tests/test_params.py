"""T2: candidate within +-2% of baseline non-embedding params, both scales."""

from postformer.models.factory import count_params


def test_param_parity(tmp_path):
    out = tmp_path / "params"
    out.mkdir()
    for scale in ("toy", "tiny", "small"):
        base, _ = count_params(f"transformer-{scale}", scale)
        (out / f"params_baseline_{scale}.txt").write_text(
            f"transformer-{scale} non-embed params: {base}\n")
        for fam in ("p1", "p2", "p3", "p4", "p5"):
            n, _ = count_params(f"{fam}-{scale}", scale)
            (out / f"params_{fam}_{scale}.txt").write_text(
                f"{fam}-{scale} non-embed params: {n} "
                f"(drift {(n - base) / base * 100:+.3f}%)\n")
            assert abs(n - base) / base <= 0.02, (fam, scale, n, base)
