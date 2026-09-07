"""T2: candidate within +-2% of baseline non-embedding params, both scales.

Also writes the committed counting-script output (params_*.txt in ledger/)."""

import os

from postformer.models.factory import count_params

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "ledger", "params")


def test_param_parity():
    os.makedirs(OUT_DIR, exist_ok=True)
    for scale in ("tiny", "small"):
        base, _ = count_params(f"transformer-{scale}", scale)
        with open(os.path.join(OUT_DIR, f"params_baseline_{scale}.txt"), "w") as f:
            f.write(f"transformer-{scale} non-embed params: {base}\n")
        for fam in ("p1", "p5"):
            n, _ = count_params(f"{fam}-{scale}", scale)
            with open(os.path.join(OUT_DIR, f"params_{fam}_{scale}.txt"), "w") as f:
                f.write(f"{fam}-{scale} non-embed params: {n} "
                        f"(drift {(n - base) / base * 100:+.3f}%)\n")
            assert abs(n - base) / base <= 0.02, (fam, scale, n, base)
