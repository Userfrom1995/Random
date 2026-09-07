"""Shared miniature configs for fast CPU tests (parity logic is scale-free)."""

MINI = {"layers": 1, "d_model": 32, "heads": 2, "mlp_hid": 64,
        "vocab_size": 48, "d_k": 8, "d_v": 8,
        "win_heads": 1, "win_hd": 8, "window": 8, "chunk": 4}
FAMILIES = ["transformer", "p1", "p5"]
