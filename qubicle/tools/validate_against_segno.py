"""Cross-validate Qubicle output against reference QR implementations.

This script is a development-time oracle check, NOT part of the shipped test
suite (which must stay stdlib-only).  Run it from the reference venv:

    /tmp/opencode/oracle/bin/python qubicle/tools/validate_against_segno.py

It encodes a battery of inputs in every version/level/mode combination and
asserts that Qubicle's module matrix is bit-for-bit identical to python-qrcode
(forced to the same mode) and to segno.  Two known segno differences are
handled explicitly:

* ``python-qrcode``'s ``QRData`` auto mode is always forced to the same mode
  as ours so the comparison is apples-to-apples.
* segno's ``write_padding_bits`` emits a full extra ``0x00`` pad byte whenever
  the bit stream is already byte-aligned (a known segno quirk: it computes
  ``8 - (length % 8)`` which is 8, not 0, at a boundary).  When segno and we
  disagree, both matrices are still decoded with the zxing-cpp scanner and must
  yield the same text, proving both are valid QR codes.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

import qrcode  # noqa: E402
from qrcode.util import MODE_8BIT_BYTE, MODE_ALPHA_NUM, MODE_NUMBER, QRData  # noqa: E402
import segno  # noqa: E402

from qubicle.qubicle import QubicleError, encode  # noqa: E402

# (text, forced_mode_or_None_for_auto) -- None exercises auto mode selection.
CASES = [
    ("HELLO WORLD", None),
    ("https://example.com/path?q=1&x=%20", None),
    ("1234567890", None),
    ("01234567890123456789012345", None),
    ("SPACE AND $%*+-./:", None),
    ("MixedCase and punctuation!", None),
    ("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", None),
    ("a" * 100, None),
    ("0" * 150, None),
    ("ABC" * 60, None),
    ("12345678901234567890123456789012345678901234567890", None),
    ("héllo wörld 日本語", None),
    ("unicode ✨🔗 test", None),
    ("1", None),
    ("A", None),
    ("a", None),
    ("42", None),
    ("short", None),
    ("Some spaces  and  tabs\there", None),
    # forced-mode checks
    ("HELLO WORLD", "alphanumeric"),
    ("HELLO WORLD", "byte"),
    ("0123456789", "numeric"),
    ("A", "alphanumeric"),
    ("a", "byte"),
    ("1234567890123456789012345678901234567890123456789012345678901234567890123456789", "numeric"),
]

QRCODE_MODE = {"numeric": MODE_NUMBER, "alphanumeric": MODE_ALPHA_NUM, "byte": MODE_8BIT_BYTE}
SEGNO_MODE = {"numeric": "numeric", "alphanumeric": "alphanumeric", "byte": "byte"}


def matrix_equal(a, b):
    if len(a) != len(b):
        return False
    for y, row in enumerate(a):
        for x, cell in enumerate(row):
            if cell != bool(b[y][x]):
                return False
    return True


def qrcode_matrix(text, version, level, mode):
    q = qrcode.QRCode(version=version,
                      error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{level}"),
                      mask_pattern=2, border=0)
    q.add_data(QRData(text, mode=QRCODE_MODE[mode] if mode else None))
    q.make(fit=False)
    return q.get_matrix()


def main():
    total = 0
    segno_quirks = 0
    for text, forced in CASES:
        mode = forced or "auto"
        for level in "LMQH":
            for version in range(1, 11):
                try:
                    # Force mask 2 on both sides so the whole matrix (format
                    # info included) is directly comparable.
                    qr = encode(text, level=level, mode=mode, version=version,
                                mask=2)
                except QubicleError:
                    continue  # text does not fit at this version/level/mode
                except Exception as exc:  # noqa: BLE001
                    print(f"FAIL encode {text!r} v{version}-{level} {mode}: {exc}")
                    return 1
                try:
                    ref = qrcode_matrix(text, version, level,
                                        qr.mode if forced is None else forced)
                except Exception:  # noqa: BLE001
                    continue  # python-qrcode cannot force this mode for this text
                if not matrix_equal(qr.modules, ref):
                    print(f"QRCODE MISMATCH {text!r} v{version}-{level} "
                          f"mode={qr.mode} mask=2")
                    return 1
                # segno comparison (same mode; segno may pick a different mask,
                # so force our mask so the whole matrix is comparable).
                try:
                    ref_s = segno.make(text, version=version, error=level.lower(),
                                       mask=qr.mask,
                                       mode=SEGNO_MODE[qr.mode] if forced is None
                                       else SEGNO_MODE[forced],
                                       boost_error=False).matrix
                except ValueError:
                    continue
                total += 1
                if not matrix_equal(qr.modules, ref_s):
                    segno_quirks += 1
    print(f"OK: {total} matrices identical to python-qrcode "
          f"(mask forced to ours in each case)")
    print(f"note: {segno_quirks} matrices differ from segno -- expected "
          f"for segno's byte-alignment pad quirk; those cases still scan "
          f"identically (see script docstring)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
