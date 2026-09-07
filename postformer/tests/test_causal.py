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
        assert diff <= 1e-6, (fam, diff)


def test_step_prefix_invariance_at_window_boundary():
    """Recurrent step() outputs over a shared prefix match the full forward
    there, even across the sliding-window boundary (MINI window=8; the
    prefix of length 10 spans it)."""
    seed_all(14, "t3-step")
    for fam in FAMILIES:
        m, _ = build_model(fam, "tiny", dict(MINI))
        m.eval()
        pre = torch.randint(0, MINI["vocab_size"], (1, 10))
        tail = torch.randint(0, MINI["vocab_size"], (1, 6))
        ids = torch.cat([pre, tail], dim=1)
        assert ids.shape[1] > MINI["window"]
        with torch.no_grad():
            full = m(ids)
            st = m.init_state(1, "cpu", torch.float32)
            outs = [m.step(ids[:, i:i + 1], st)[0] for i in range(ids.shape[1])]
        stepped = torch.cat(outs, dim=1)
        diff = (stepped[:, :10, :] - full[:, :10, :]).abs().max().item()
        # Same 1e-4 bar as T1 parity (step reorders reductions vs forward).
        assert diff <= 1e-4, (fam, diff)
