"""T3: causal masking - prefix logits invariant to future tokens (planted trigger)."""

import torch

from postformer.models.common import seed_all
from postformer.models.factory import build_model
from .conftest import FAMILIES, MINI


def test_prefix_invariance():
    seed_all(13, "t3")
    for fam in FAMILIES:
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        pre = torch.randint(0, MINI["vocab_size"], (2, 10))
        trig_a = torch.full((2, 6), 3, dtype=torch.long)
        trig_b = torch.randint(0, MINI["vocab_size"], (2, 6))
        a = torch.cat([pre, trig_a], dim=1)
        b = torch.cat([pre, trig_b], dim=1)
        with torch.no_grad():
            la, lb = m(a), m(b)
        diff = (la[:, :10, :] - lb[:, :10, :]).abs().max().item()
        assert diff == 0.0, (fam, diff)
