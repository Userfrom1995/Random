#!/usr/bin/env python3
"""Qubicle - a dependency-free terminal QR-code encoder.

Qubicle turns text into a real, scannable QR code and renders it straight into
your terminal using Unicode half-block characters (which double the effective
vertical resolution) or a plain ASCII fallback. It can also write the code to
PNG or SVG with a tiny hand-rolled writer (no Pillow, no external packages).

Everything is implemented from scratch against the ISO/IEC 18004 QR code
specification: version selection (1-10), numeric/alphanumeric/byte modes,
Galois-field-256 Reed-Solomon error correction, module placement with
finder/timing/alignment/format/version patterns, data masking with penalty
scoring, and a ``--test`` self-verification mode that decodes the rendered
grid back into codewords to prove it is correct.

Usage::

    python3 -m qubicle "https://example.com"
    python3 -m qubicle --ascii "HELLO WORLD"
    python3 -m qubicle --png code.png --svg code.svg --scale 12 "QR text"
    python3 -m qubicle --test "self-verification"
    echo "from stdin" | python3 -m qubicle

Run ``python3 -m qubicle --help`` for the full option reference, or see the
README and the ``docs/`` folder for the detailed guide.
"""

from __future__ import annotations

import argparse
import binascii
import struct
import sys
import zlib
from typing import Dict, List, Optional, Sequence, Tuple

__version__ = "1.0.0"

# --------------------------------------------------------------------------
# QR parameter tables (ISO/IEC 18004, versions 1-10 only)
# --------------------------------------------------------------------------

MIN_VERSION = 1
MAX_VERSION = 10

# The alphanumeric character set (spec table 2).
ALPHANUMERIC = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

# Error-correction level format-info indicators (spec table 25).
EC_INDICATOR: Dict[str, int] = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}
_LEVEL_BY_INDICATOR = {v: k for k, v in EC_INDICATOR.items()}
EC_LEVELS = ("L", "M", "Q", "H")

# Mode indicators (spec table 2).
MODE_INDICATOR: Dict[str, int] = {
    "numeric": 0b0001,
    "alphanumeric": 0b0010,
    "byte": 0b0100,
}

# Character-count-field length in bits, keyed by mode then version group
# (versions 1-9 and 10-26; Qubicle supports only up to version 10).
CHAR_COUNT_BITS: Dict[str, Tuple[int, int]] = {
    "numeric": (10, 12),
    "alphanumeric": (9, 11),
    "byte": (8, 16),
}

# Centre coordinates of the alignment patterns per version (spec annex E).
ALIGNMENT_POS: Dict[int, Tuple[int, ...]] = {
    1: (),
    2: (6, 18),
    3: (6, 22),
    4: (6, 26),
    5: (6, 30),
    6: (6, 34),
    7: (6, 22, 38),
    8: (6, 24, 42),
    9: (6, 26, 46),
    10: (6, 28, 50),
}

# Error-correction block structure per version and level.  Each entry maps a
# level to ``(ec_per_block, ((num_blocks, data_per_block), ...))`` where the
# group list may contain two groups (the first with smaller blocks).
ECC_BLOCKS: Dict[int, Dict[str, Tuple[int, Tuple[Tuple[int, int], ...]]]] = {
    1: {"L": (7, ((1, 19),)), "M": (10, ((1, 16),)), "Q": (13, ((1, 13),)), "H": (17, ((1, 9),))},
    2: {"L": (10, ((1, 34),)), "M": (16, ((1, 28),)), "Q": (22, ((1, 22),)), "H": (28, ((1, 16),))},
    3: {"L": (15, ((1, 55),)), "M": (26, ((1, 44),)), "Q": (18, ((2, 17),)), "H": (22, ((2, 13),))},
    4: {"L": (20, ((1, 80),)), "M": (18, ((2, 32),)), "Q": (26, ((2, 24),)), "H": (16, ((4, 9),))},
    5: {"L": (26, ((1, 108),)), "M": (24, ((2, 43),)),
        "Q": (18, ((2, 15), (2, 16))), "H": (22, ((2, 11), (2, 12)))},
    6: {"L": (18, ((2, 68),)), "M": (16, ((4, 27),)), "Q": (24, ((4, 19),)), "H": (28, ((4, 15),))},
    7: {"L": (20, ((2, 78),)), "M": (18, ((4, 31),)),
        "Q": (18, ((2, 14), (4, 15))), "H": (26, ((4, 13), (1, 14)))},
    8: {"L": (24, ((2, 97),)), "M": (22, ((2, 38), (2, 39))),
        "Q": (22, ((4, 18), (2, 19))), "H": (26, ((4, 14), (2, 15)))},
    9: {"L": (30, ((2, 116),)), "M": (22, ((3, 36), (2, 37))),
        "Q": (20, ((4, 16), (4, 17))), "H": (24, ((4, 12), (4, 13)))},
    10: {"L": (18, ((2, 68), (2, 69))), "M": (26, ((4, 43), (1, 44))),
         "Q": (24, ((6, 19), (2, 20))), "H": (28, ((6, 15), (2, 16)))},
}

# The number of unused (remainder) bits appended to the codeword stream after
# the final bit of the interleaved codewords (spec table 1).
REMAINDER_BITS: Dict[int, int] = {
    1: 0, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7,
    7: 0, 8: 0, 9: 0, 10: 0,
}

# BCH generator polynomials used for the format and version information.
_FORMAT_GEN = 0x537     # BCH(15,5)
_VERSION_GEN = 0x1F25   # BCH(18,6)
_FORMAT_MASK = 0x5412

# Pad codewords used to fill the remaining data capacity (spec 8.4.9).
_PAD_BYTE_0 = 0xEC
_PAD_BYTE_1 = 0x11


class QubicleError(Exception):
    """Raised for any input that cannot be encoded as a QR code."""


# --------------------------------------------------------------------------
# Galois field GF(2^8) arithmetic with the QR code primitive polynomial
# --------------------------------------------------------------------------

def _build_gf_tables() -> Tuple[List[int], List[int]]:
    """Build the exponent and logarithm tables for GF(2^8).

    The QR primitive polynomial is x^8 + x^4 + x^3 + x^2 + 1 (0x11D).  The
    exponent table is doubled in length so products of logarithms can be
    looked up without a modulo in the common case.
    """
    exp = [0] * 512
    log = [0] * 256
    x = 1
    for i in range(255):
        exp[i] = x
        log[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    for i in range(255, 512):
        exp[i] = exp[i - 255]
    return exp, log


_GF_EXP, _GF_LOG = _build_gf_tables()


def gf_mul(a: int, b: int) -> int:
    """Multiply two field elements (0-255)."""
    if a == 0 or b == 0:
        return 0
    return _GF_EXP[(_GF_LOG[a] + _GF_LOG[b]) % 255]


def gf_poly_mul(p: Sequence[int], q: Sequence[int]) -> List[int]:
    """Multiply two polynomials over GF(2^8)."""
    result = [0] * (len(p) + len(q) - 1)
    for i, pi in enumerate(p):
        if pi == 0:
            continue
        for j, qj in enumerate(q):
            result[i + j] ^= gf_mul(pi, qj)
    return result


def rs_generator_poly(ec_count: int) -> List[int]:
    """Return the Reed-Solomon generator polynomial (x-a^0)(x-a^1)..."""
    gen = [1]
    for i in range(ec_count):
        gen = gf_poly_mul(gen, [1, _GF_EXP[i]])
    return gen


def rs_encode(data: Sequence[int], ec_count: int) -> List[int]:
    """Compute the ``ec_count`` Reed-Solomon error-correction codewords for
    ``data`` using synthetic division."""
    gen = rs_generator_poly(ec_count)
    poly = list(data) + [0] * ec_count
    for i in range(len(data)):
        factor = poly[i]
        if factor == 0:
            continue
        for j in range(ec_count + 1):
            poly[i + j] ^= gf_mul(gen[j], factor)
    return poly[-ec_count:]


# --------------------------------------------------------------------------
# Mode encoding
# --------------------------------------------------------------------------

def _char_count(text: str, mode: str) -> int:
    """Return the value stored in the character-count field for ``mode``."""
    if mode == "byte":
        return len(text.encode("utf-8"))
    return len(text)


def _numeric_bits(text: str) -> str:
    result = []
    i = 0
    n = len(text)
    while i + 3 <= n:
        result.append(f"{int(text[i:i + 3]):010b}")
        i += 3
    left = n - i
    if left == 2:
        result.append(f"{int(text[i:i + 2]):07b}")
    elif left == 1:
        result.append(f"{int(text[i:i + 1]):04b}")
    return "".join(result)


def _alphanumeric_bits(text: str) -> str:
    result = []
    i = 0
    n = len(text)
    while i + 2 <= n:
        value = ALPHANUMERIC.index(text[i]) * 45 + ALPHANUMERIC.index(text[i + 1])
        result.append(f"{value:011b}")
        i += 2
    if i < n:
        result.append(f"{ALPHANUMERIC.index(text[i]):06b}")
    return "".join(result)


def _byte_bits(text: str) -> str:
    return "".join(f"{b:08b}" for b in text.encode("utf-8"))


def _validate_mode(text: str, mode: str) -> None:
    if mode == "numeric":
        if not text.isdigit():
            bad = sorted({c for c in text if not c.isdigit()})
            raise QubicleError(
                f"numeric mode requires digits only; found: {''.join(bad)}")
    elif mode == "alphanumeric":
        bad = sorted({c for c in text if c not in ALPHANUMERIC})
        if bad:
            raise QubicleError(
                f"alphanumeric mode has no encoding for: {''.join(bad)}")
    elif mode == "byte":
        try:
            text.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise QubicleError(f"byte mode could not encode text: {exc}") from exc


def auto_mode(text: str) -> str:
    """Pick the most compact mode that can represent ``text``."""
    if text.isdigit():
        return "numeric"
    if all(c in ALPHANUMERIC for c in text):
        return "alphanumeric"
    return "byte"


def mode_data_bits(text: str, mode: str) -> str:
    """Return the mode payload bits for ``text`` in ``mode``."""
    _validate_mode(text, mode)
    if mode == "numeric":
        return _numeric_bits(text)
    if mode == "alphanumeric":
        return _alphanumeric_bits(text)
    return _byte_bits(text)


def data_capacity_bits(version: int, level: str) -> int:
    """Return how many data bits ``version``/``level`` can hold before EC."""
    ec_per_block, groups = ECC_BLOCKS[version][level]
    del ec_per_block
    return sum(num * size for num, size in groups) * 8


def count_field_bits(mode: str, version: int) -> int:
    """Return the character-count-field length in bits for ``mode`` at
    ``version`` (versions 1-9 vs 10-26; Qubicle caps at version 10)."""
    group = 0 if version <= 9 else 1
    return CHAR_COUNT_BITS[mode][group]


def required_bits(text: str, mode: str, version: int) -> int:
    """Total bits needed for the mode indicator, count field, and payload."""
    return (4 + count_field_bits(mode, version)
            + len(mode_data_bits(text, mode)))


def max_chars(mode: str, version: int, level: str) -> int:
    """Return the largest character count that fits ``version``/``level``."""
    capacity = data_capacity_bits(version, level)
    count_bits = count_field_bits(mode, version)
    if mode == "byte":
        per_char = 8
    elif mode == "alphanumeric":
        per_char = 11 / 2
    else:
        per_char = 10 / 3
    return int((capacity - 4 - count_bits) // per_char)


def build_bitstream(text: str, mode: str, version: int, level: str) -> List[int]:
    """Assemble the full padded data codewords for ``text``."""
    capacity = data_capacity_bits(version, level)
    count = _char_count(text, mode)
    bits = (
        f"{MODE_INDICATOR[mode]:04b}"
        + f"{count:0{count_field_bits(mode, version)}b}"
        + mode_data_bits(text, mode)
    )
    if len(bits) > capacity:
        raise QubicleError(
            f"text needs {len(bits)} bits but version {version}-{level} only "
            f"holds {capacity}")
    # Terminator: up to four zero bits, clipped to remaining capacity.
    remaining = capacity - len(bits)
    terminator = min(4, remaining)
    bits += "0" * terminator
    remaining -= terminator
    # Pad to a whole number of codewords with zeros.
    remainder = remaining % 8
    if remainder:
        bits += "0" * remainder
        remaining -= remainder
    # Fill the rest with the alternating pad codewords 0xEC/0x11.
    pad = _PAD_BYTE_0
    while remaining:
        bits += f"{pad:08b}"
        remaining -= 8
        pad = _PAD_BYTE_1 if pad == _PAD_BYTE_0 else _PAD_BYTE_0
    return [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]


# --------------------------------------------------------------------------
# Error-correction block splitting and interleaving
# --------------------------------------------------------------------------

def split_blocks(codewords: Sequence[int], version: int, level: str
                 ) -> Tuple[List[List[int]], List[List[int]]]:
    """Split ``codewords`` into data blocks and compute their EC blocks."""
    ec_per_block, groups = ECC_BLOCKS[version][level]
    data_blocks: List[List[int]] = []
    index = 0
    for num, size in groups:
        for _ in range(num):
            data_blocks.append(list(codewords[index:index + size]))
            index += size
    if index != len(codewords):
        raise QubicleError("internal error: codeword/block size mismatch")
    ec_blocks = [rs_encode(block, ec_per_block) for block in data_blocks]
    return data_blocks, ec_blocks


def interleave(data_blocks: Sequence[Sequence[int]],
               ec_blocks: Sequence[Sequence[int]]) -> List[int]:
    """Interleave data then EC codewords column-wise across the blocks."""
    result: List[int] = []
    max_data = max(len(b) for b in data_blocks)
    for i in range(max_data):
        for block in data_blocks:
            if i < len(block):
                result.append(block[i])
    max_ec = max(len(e) for e in ec_blocks)
    for i in range(max_ec):
        for block in ec_blocks:
            if i < len(block):
                result.append(block[i])
    return result


def deinterleave(codewords: Sequence[int], version: int, level: str
                 ) -> Tuple[List[List[int]], List[List[int]]]:
    """Reverse :func:`interleave`, restoring the data and EC blocks."""
    ec_per_block, groups = ECC_BLOCKS[version][level]
    sizes: List[int] = []
    for num, size in groups:
        sizes.extend([size] * num)
    data_blocks = [[0] * size for size in sizes]
    index = 0
    for i in range(max(sizes)):
        for block in data_blocks:
            if i < len(block):
                block[i] = codewords[index]
                index += 1
    ec_blocks = [[0] * ec_per_block for _ in sizes]
    for i in range(ec_per_block):
        for block in ec_blocks:
            block[i] = codewords[index]
            index += 1
    if index != len(codewords):
        raise QubicleError("internal error: deinterleave size mismatch")
    return data_blocks, ec_blocks


# --------------------------------------------------------------------------
# BCH codes for the format and version information
# --------------------------------------------------------------------------

def bch_remainder(value: int, gen: int) -> int:
    """Return the BCH remainder of ``value`` (already shifted) mod ``gen``."""
    degree = gen.bit_length() - 1
    while value.bit_length() > degree:
        shift = value.bit_length() - degree - 1
        value ^= gen << shift
    return value


def format_info_bits(level: str, mask: int) -> int:
    """Return the 15-bit format information for ``level`` and ``mask``."""
    data = (EC_INDICATOR[level] << 3) | mask
    return ((data << 10) | bch_remainder(data << 10, _FORMAT_GEN)) ^ _FORMAT_MASK


def version_info_bits(version: int) -> int:
    """Return the 18-bit version information for ``version`` (7-10)."""
    return (version << 12) | bch_remainder(version << 12, _VERSION_GEN)


# --------------------------------------------------------------------------
# Module placement
# --------------------------------------------------------------------------

def matrix_size(version: int) -> int:
    """Return the number of modules per side for ``version``."""
    return 21 + 4 * (version - 1)


def _format_coordinates(size: int) -> List[Tuple[int, int]]:
    """The 15 (x, y) format-info cells in bit order (bit 14 first) for the
    primary copy next to the top-left finder.  Bit 0 sits at (8, 0) next to
    the timing column, matching the ISO 18004 placement diagram."""
    return [
        (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (7, 8), (8, 8),
        (8, 7), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0),
    ]


def _format_coordinates_mirror(size: int) -> List[Tuple[int, int]]:
    """The 15 (x, y) format-info cells for the mirrored copy beside the
    top-right finder, in bit order (bit 14 first)."""
    coords = [(8, size - 1 - i) for i in range(7)]
    coords += [(size - 8 + i, 8) for i in range(8)]
    return coords


def function_patterns(version: int
                      ) -> Tuple[List[List[bool]], List[List[bool]]]:
    """Build a ``(modules, is_function)`` pair of grids with all function
    patterns drawn.  ``modules`` holds the light/dark state (True = dark) and
    ``is_function`` marks cells the data placement must skip.  Format-info
    cells are reserved here (values filled later once the mask is known)."""
    size = matrix_size(version)
    mod = [[False] * size for _ in range(size)]
    func = [[False] * size for _ in range(size)]

    def set_module(x: int, y: int, dark: bool) -> None:
        mod[y][x] = dark
        func[y][x] = True

    # --- finder patterns (3 corners) and their light separators ---
    for (cx, cy) in ((3, 3), (size - 4, 3), (3, size - 4)):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = cx + dx, cy + dy
                if not (0 <= x < size and 0 <= y < size):
                    continue
                if max(abs(dx), abs(dy)) == 4:
                    set_module(x, y, False)      # separator ring
                elif max(abs(dx), abs(dy)) == 3:
                    set_module(x, y, True)       # outer border
                elif max(abs(dx), abs(dy)) == 2:
                    set_module(x, y, False)      # inner light ring
                elif max(abs(dx), abs(dy)) == 1:
                    set_module(x, y, True)       # inner dark ring
                else:
                    set_module(x, y, True)       # centre dot

    # --- timing patterns (row 6 and column 6) ---
    for i in range(8, size - 8):
        set_module(i, 6, i % 2 == 0)
        set_module(6, i, i % 2 == 0)

    # --- alignment patterns (skip the ones overlapping the finders) ---
    centers = ALIGNMENT_POS[version]
    for y in centers:
        for x in centers:
            if (x, y) in ((6, 6), (6, size - 7), (size - 7, 6)):
                continue
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    set_module(x + dx, y + dy, max(abs(dx), abs(dy)) != 1)

    # --- dark module ---
    set_module(8, size - 8, True)

    # --- version information (versions 7-10) ---
    if version >= 7:
        bits = version_info_bits(version)
        for bit in range(18):
            dark = (bits >> bit) & 1
            set_module(size - 11 + bit % 3, bit // 3, bool(dark))
            set_module(bit // 3, size - 11 + bit % 3, bool(dark))

    # --- reserve the format-info cells (values drawn after masking) ---
    for x, y in _format_coordinates(size) + _format_coordinates_mirror(size):
        set_module(x, y, False)

    return mod, func


def draw_format_info(mod: List[List[bool]], size: int, level: str,
                     mask: int) -> None:
    """Write the 15 format-info bits (both copies) into ``mod``."""
    bits = format_info_bits(level, mask)
    for coords in (_format_coordinates(size), _format_coordinates_mirror(size)):
        for bit, (x, y) in enumerate(coords):
            dark = (bits >> (14 - bit)) & 1
            mod[y][x] = bool(dark)


def _column_pairs(size: int) -> List[int]:
    """Right-hand column of each column pair, in zigzag order.  The timing
    column (6) is skipped by shifting pair (6, 5) to (5, 4)."""
    pairs: List[int] = []
    right = size - 1
    while right >= 1:
        if right == 6:
            right = 5
        pairs.append(right)
        right -= 2
    return pairs


def mask_bit(mask: int, x: int, y: int) -> bool:
    """Return the mask value for the module at column ``x``, row ``y``."""
    if mask == 0:
        return (x + y) % 2 == 0
    if mask == 1:
        return y % 2 == 0
    if mask == 2:
        return x % 3 == 0
    if mask == 3:
        return (x + y) % 3 == 0
    if mask == 4:
        return (y // 2 + x // 3) % 2 == 0
    if mask == 5:
        return (x * y) % 2 + (x * y) % 3 == 0
    if mask == 6:
        return ((x * y) % 2 + (x * y) % 3) % 2 == 0
    if mask == 7:
        return ((x + y) % 2 + (x * y) % 3) % 2 == 0
    raise QubicleError(f"invalid mask: {mask}")


def _place_data(mod: List[List[bool]], func: List[List[bool]],
                bits: str, mask: int, size: int) -> None:
    """Fill the data modules in zigzag order, applying ``mask``."""
    index = 0
    for right in _column_pairs(size):
        upward = ((right + 1) & 2) == 0
        for vert in range(size):
            y = size - 1 - vert if upward else vert
            for j in range(2):
                x = right - j
                if func[y][x]:
                    continue
                if index >= len(bits):
                    continue
                mod[y][x] = (bits[index] == "1") ^ mask_bit(mask, x, y)
                index += 1


def make_matrix(version: int, level: str, codewords: Sequence[int],
                mask: int) -> List[List[bool]]:
    """Build the complete module matrix for ``version``/``level`` using
    ``codewords`` (interleaved data + EC) and ``mask``."""
    size = matrix_size(version)
    mod, func = function_patterns(version)
    bits = "".join(f"{b:08b}" for b in codewords) + "0" * REMAINDER_BITS[version]
    _place_data(mod, func, bits, mask, size)
    draw_format_info(mod, size, level, mask)
    return mod


# --------------------------------------------------------------------------
# Mask evaluation (penalty scoring)
# --------------------------------------------------------------------------

def _run_penalty_rule1(line: Sequence[bool]) -> int:
    """N1: runs of five or more same-colour modules score 3 + (length - 5)."""
    total = 0
    run_len = 1
    for i in range(1, len(line)):
        if line[i] == line[i - 1]:
            run_len += 1
        else:
            if run_len >= 5:
                total += 3 + (run_len - 5)
            run_len = 1
    if run_len >= 5:
        total += 3 + (run_len - 5)
    return total


def _find_ratio_patterns(line: Sequence[bool]) -> int:
    """N3: finder-like dark:light:dark:light:dark (1:1:3:1:1) runs framed by
    four light modules score 40 each."""
    s = "".join("1" if c else "0" for c in line)
    count = 0
    for pattern in ("10111010000", "00001011101"):
        start = 0
        while True:
            pos = s.find(pattern, start)
            if pos < 0:
                break
            count += 1
            start = pos + 1
    return count * 40


def penalty_score(modules: List[List[bool]]) -> int:
    """Compute the total mask penalty for ``modules`` (four spec rules)."""
    size = len(modules)
    total = 0
    for y in range(size):
        total += _run_penalty_rule1(modules[y])
        total += _find_ratio_patterns(modules[y])
    columns = [[modules[y][x] for y in range(size)] for x in range(size)]
    for x in range(size):
        total += _run_penalty_rule1(columns[x])
        total += _find_ratio_patterns(columns[x])
    for y in range(size - 1):
        for x in range(size - 1):
            cell = modules[y][x]
            if (modules[y][x + 1] == cell
                    and modules[y + 1][x] == cell
                    and modules[y + 1][x + 1] == cell):
                total += 3
    dark = sum(sum(row) for row in modules)
    percent = dark * 100 / (size * size)
    total += int(abs(percent - 50) // 5) * 10
    return total


def best_mask(version: int, level: str, codewords: Sequence[int]
              ) -> Tuple[int, List[List[bool]]]:
    """Return ``(mask, matrix)`` for the lowest-penalty mask."""
    best_mask_id = 0
    best_matrix = make_matrix(version, level, codewords, 0)
    best_score = penalty_score(best_matrix)
    for candidate in range(1, 8):
        matrix = make_matrix(version, level, codewords, candidate)
        score = penalty_score(matrix)
        if score < best_score:
            best_mask_id, best_matrix, best_score = candidate, matrix, score
    return best_mask_id, best_matrix


# --------------------------------------------------------------------------
# Self-verification decoder (used by --test)
# --------------------------------------------------------------------------

def decode_format_info(modules: List[List[bool]]
                       ) -> Optional[Tuple[str, int]]:
    """Read and validate the format information, returning ``(level, mask)``
    or ``None`` if the BCH check fails."""
    size = len(modules)
    value = 0
    for x, y in _format_coordinates(size):
        value = (value << 1) | (1 if modules[y][x] else 0)
    bits = value ^ _FORMAT_MASK
    if bch_remainder(bits, _FORMAT_GEN) != 0:
        return None
    level = _LEVEL_BY_INDICATOR[(bits >> 13) & 0b11]
    mask = (bits >> 10) & 0b111
    return level, mask


def _read_data_bits(modules: List[List[bool]], func: List[List[bool]],
                    mask: int, size: int) -> str:
    bits: List[str] = []
    for right in _column_pairs(size):
        upward = ((right + 1) & 2) == 0
        for vert in range(size):
            y = size - 1 - vert if upward else vert
            for j in range(2):
                x = right - j
                if func[y][x]:
                    continue
                value = modules[y][x] ^ mask_bit(mask, x, y)
                bits.append("1" if value else "0")
    return "".join(bits)


def decode_matrix(modules: List[List[bool]]
                  ) -> Tuple[str, int, bool, str]:
    """Re-read ``modules`` as a scanner would and verify every Reed-Solomon
    block.  Returns ``(level, mask, ok, message)``."""
    size = len(modules)
    if (size - 17) % 4 != 0 or not (MIN_VERSION * 4 + 17 <= size <= MAX_VERSION * 4 + 17):
        return ("?", -1, False, f"matrix size {size} is not a supported QR size")
    version = (size - 17) // 4
    fmt = decode_format_info(modules)
    if fmt is None:
        return ("?", -1, False, "format information failed its BCH check")
    level, mask = fmt
    _, func = function_patterns(version)
    bitstream = _read_data_bits(modules, func, mask, size)
    if REMAINDER_BITS[version]:
        bitstream = bitstream[:-REMAINDER_BITS[version]]
    codewords = [int(bitstream[i:i + 8], 2)
                 for i in range(0, len(bitstream), 8)]
    data_blocks, ec_blocks = deinterleave(codewords, version, level)
    for data, ec in zip(data_blocks, ec_blocks):
        if rs_encode(data, len(ec)) != ec:
            return (level, mask, False,
                    "a Reed-Solomon block does not match its EC codewords")
    return (level, mask, True, f"version {version} verified: all "
            f"{len(data_blocks)} Reed-Solomon blocks decode cleanly")


# --------------------------------------------------------------------------
# Rendering: terminal, ASCII, PNG, SVG
# --------------------------------------------------------------------------

_QUIET_DEFAULT = 4


def _pixel_matrix(modules: List[List[bool]], quiet: int
                  ) -> List[List[bool]]:
    """Surround ``modules`` with a light ``quiet``-module border."""
    size = len(modules)
    full = size + 2 * quiet
    grid = [[False] * full for _ in range(full)]
    for y in range(size):
        for x in range(size):
            grid[y + quiet][x + quiet] = modules[y][x]
    return grid


def render_terminal(modules: List[List[bool]], quiet: int = _QUIET_DEFAULT
                    ) -> str:
    """Render ``modules`` with Unicode half-blocks, stacking two modules per
    terminal cell for double effective vertical resolution."""
    grid = _pixel_matrix(modules, quiet)
    full = len(grid)
    lines = []
    for y in range(0, full, 2):
        top = grid[y]
        bottom = grid[y + 1] if y + 1 < full else [False] * full
        chars = []
        for t, b in zip(top, bottom):
            if t and b:
                chars.append("\u2588")   # full block
            elif t:
                chars.append("\u2580")   # upper half block
            elif b:
                chars.append("\u2584")   # lower half block
            else:
                chars.append(" ")
        lines.append("".join(chars))
    return "\n".join(lines)


def render_ascii(modules: List[List[bool]], quiet: int = _QUIET_DEFAULT,
                 dark: str = "#") -> str:
    """Render ``modules`` with plain ASCII, two columns per module to keep
    the code roughly square in a typical terminal."""
    grid = _pixel_matrix(modules, quiet)
    light = " " * len(dark)
    lines = []
    for row in grid:
        lines.append("".join(dark if cell else light for cell in row))
    return "\n".join(lines)


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path: str, modules: List[List[bool]], scale: int = 10,
              quiet: int = _QUIET_DEFAULT) -> None:
    """Write a black-and-white 1-bit grayscale PNG with a minimal hand-rolled
    writer (signature, IHDR, a single zlib-compressed IDAT, IEND)."""
    if scale < 1:
        raise QubicleError(f"scale must be at least 1, got {scale}")
    grid = _pixel_matrix(modules, quiet)
    full = len(grid)
    pixel = full * scale
    row_bytes = (pixel + 7) // 8
    raw = bytearray()
    for py in range(pixel):
        raw.append(0)  # filter type None for every row
        my = py // scale
        for byte_i in range(row_bytes):
            byte = 0
            for bit in range(8):
                px = byte_i * 8 + bit
                if px >= pixel:
                    continue
                mx = px // scale
                if not grid[my][mx]:
                    byte |= 1 << (7 - bit)  # light module -> white (1)
            raw.append(byte)
    ihdr = struct.pack(">IIBBBBB", pixel, pixel, 1, 0, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + _png_chunk(b"IHDR", ihdr)
           + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _png_chunk(b"IEND", b""))
    with open(path, "wb") as handle:
        handle.write(png)


def write_svg(path: str, modules: List[List[bool]], scale: int = 10,
              quiet: int = _QUIET_DEFAULT) -> None:
    """Write a compact SVG made of one black ``<rect>`` per dark module."""
    if scale < 1:
        raise QubicleError(f"scale must be at least 1, got {scale}")
    grid = _pixel_matrix(modules, quiet)
    full = len(grid)
    pixel = full * scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{pixel}" height="{pixel}" '
        f'viewBox="0 0 {pixel} {pixel}" shape-rendering="crispEdges">',
        f'<rect width="{pixel}" height="{pixel}" fill="#ffffff"/>',
    ]
    for y, row in enumerate(grid):
        for x, dark in enumerate(row):
            if dark:
                parts.append(
                    f'<rect x="{x * scale}" y="{y * scale}" width="{scale}" '
                    f'height="{scale}" fill="#000000"/>')
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(parts))


# --------------------------------------------------------------------------
# Encoding driver + CLI
# --------------------------------------------------------------------------

class QrCode:
    """The result of encoding text into a QR code."""

    def __init__(self, text: str, version: int, level: str, mode: str,
                 mask: int, modules: List[List[bool]],
                 codewords: List[int]) -> None:
        self.text = text
        self.version = version
        self.level = level
        self.mode = mode
        self.mask = mask
        self.modules = modules
        self.codewords = codewords

    @property
    def size(self) -> int:
        """Number of modules per side."""
        return len(self.modules)


def encode(text: str, level: str = "M", mode: str = "auto",
           version: Optional[int] = None,
           mask: Optional[int] = None) -> QrCode:
    """Encode ``text`` into a :class:`QrCode`.

    ``level`` is an EC level from ``L/M/Q/H``.  ``mode`` is
    ``auto/numeric/alphanumeric/byte``.  ``version`` and ``mask`` default to
    the smallest fitting version and the lowest-penalty mask.
    """
    if not isinstance(text, str):
        raise QubicleError("input must be a string")
    if not text:
        raise QubicleError("nothing to encode: input is empty")
    if level not in EC_LEVELS:
        raise QubicleError(f"invalid EC level: {level!r} (choose from L, M, Q, H)")
    if mode == "auto":
        mode = auto_mode(text)
    if mode not in MODE_INDICATOR:
        raise QubicleError(f"invalid mode: {mode!r}")
    if version is None:
        version = choose_version(text, mode, level)
    _validate_mode(text, mode)
    codewords = build_bitstream(text, mode, version, level)
    data_blocks, ec_blocks = split_blocks(codewords, version, level)
    interleaved = interleave(data_blocks, ec_blocks)
    if mask is None:
        mask, modules = best_mask(version, level, interleaved)
    else:
        modules = make_matrix(version, level, interleaved, mask)
    return QrCode(text, version, level, mode, mask, modules, interleaved)


def choose_version(text: str, mode: str, level: str) -> int:
    """Pick the smallest version 1-10 that fits ``text`` in ``mode``."""
    for version in range(MIN_VERSION, MAX_VERSION + 1):
        if required_bits(text, mode, version) <= data_capacity_bits(version, level):
            return version
    raise QubicleError(
        "text is too long for any supported QR version (1-10); "
        "try a lower error-correction level or shorter text")


def capacity_table() -> str:
    """Render a numeric/alphanumeric/byte character-capacity table."""
    header = f"{'':>3} {'':>3} " + " ".join(
        f"{mode:>14}" for mode in ("numeric", "alphanumeric", "byte"))
    lines = [header]
    for version in range(MIN_VERSION, MAX_VERSION + 1):
        for level in EC_LEVELS:
            row = [f"v{version:>2}", f"{level:>3}"]
            for mode in ("numeric", "alphanumeric", "byte"):
                row.append(f"{max_chars(mode, version, level):>14}")
            lines.append(" ".join(row))
    return "\n".join(lines)


def _read_input(text: Optional[str], file: Optional[str]) -> str:
    if text is not None:
        return text
    if file == "-" or (text is None and file is None):
        return sys.stdin.read()
    with open(file, "r", encoding="utf-8") as handle:
        return handle.read()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qubicle",
        description=(
            "Qubicle - a dependency-free terminal QR-code encoder. Prints a "
            "scannable QR code to the terminal (Unicode half-blocks or ASCII) "
            "and can also write PNG/SVG files."),
        epilog=(
            "examples:\n"
            "  python3 -m qubicle 'https://example.com'\n"
            "  python3 -m qubicle --ascii 'HELLO WORLD'\n"
            "  python3 -m qubicle --png code.png --scale 12 'text'\n"
            "  echo 'stdin input' | python3 -m qubicle\n"
            "  python3 -m qubicle --test 'verify me'\n"
            "  python3 -m qubicle --capacity"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text", nargs="?", default=None,
        help="text to encode (omit to read from --file or stdin)")
    parser.add_argument(
        "-f", "--file", metavar="FILE", default=None,
        help="read the text from FILE ('-' for stdin)")
    parser.add_argument(
        "-v", "--version", type=int, choices=range(MIN_VERSION, MAX_VERSION + 1),
        default=None,
        help=f"QR version {MIN_VERSION}-{MAX_VERSION} "
             "(default: smallest version that fits)")
    parser.add_argument(
        "-l", "--level", choices=["auto"] + list(EC_LEVELS), default="auto",
        help="error-correction level (default: auto = M)")
    parser.add_argument(
        "-m", "--mode", choices=["auto", "numeric", "alphanumeric", "byte"],
        default="auto",
        help="encoding mode (default: auto = most compact that fits)")
    parser.add_argument(
        "-M", "--mask", type=int, choices=range(8), default=None,
        help="force a data mask 0-7 (default: lowest-penalty mask)")
    parser.add_argument(
        "--ascii", action="store_true",
        help="render with plain ASCII instead of Unicode half-blocks")
    parser.add_argument(
        "--png", metavar="FILE", default=None,
        help="also write a PNG image to FILE")
    parser.add_argument(
        "--svg", metavar="FILE", default=None,
        help="also write an SVG image to FILE")
    parser.add_argument(
        "--scale", type=int, default=10,
        help="pixels per module for PNG/SVG output (default: 10)")
    parser.add_argument(
        "--quiet", type=int, default=_QUIET_DEFAULT,
        help="light modules of quiet zone around the code (default: 4)")
    parser.add_argument(
        "--test", action="store_true",
        help="decode the rendered grid back into codewords to verify it, "
             "then exit 0 on success or 1 on failure")
    parser.add_argument(
        "--capacity", action="store_true",
        help="print the character-capacity table and exit")
    parser.add_argument(
        "--charset", action="store_true",
        help="print the alphanumeric character set and exit")
    parser.add_argument(
        "--version-action", action="version",
        version=f"qubicle {__version__}")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point; returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.capacity:
        print(capacity_table())
        return 0
    if args.charset:
        print(f"Alphanumeric character set ({len(ALPHANUMERIC)} chars):")
        print(ALPHANUMERIC)
        return 0

    try:
        text = _read_input(args.text, args.file)
    except OSError as exc:
        print(f"qubicle: cannot read input: {exc}", file=sys.stderr)
        return 2
    if text.endswith("\n"):
        text = text[:-1]
    if not text:
        print("qubicle: nothing to encode: input is empty", file=sys.stderr)
        return 2

    level = "M" if args.level == "auto" else args.level
    try:
        qr = encode(text, level=level, mode=args.mode,
                    version=args.version, mask=args.mask)
    except QubicleError as exc:
        print(f"qubicle: {exc}", file=sys.stderr)
        return 2

    meta = (f"qubicle {__version__} | version {qr.version} | level {qr.level} "
            f"| mode {qr.mode} | mask {qr.mask} | {qr.size}x{qr.size} "
            f"| {len(qr.text)} chars")
    print(meta, file=sys.stderr)

    if args.test:
        level_out, mask_out, ok, message = decode_matrix(qr.modules)
        if not ok or level_out != qr.level or mask_out != qr.mask:
            print(f"qubicle: SELF-TEST FAILED: {message}", file=sys.stderr)
            return 1
        print(f"qubicle: self-test OK ({message})", file=sys.stderr)

    if args.png:
        try:
            write_png(args.png, qr.modules, scale=args.scale, quiet=args.quiet)
        except OSError as exc:
            print(f"qubicle: cannot write PNG: {exc}", file=sys.stderr)
            return 2
        print(f"qubicle: wrote {args.png}", file=sys.stderr)
    if args.svg:
        try:
            write_svg(args.svg, qr.modules, scale=args.scale, quiet=args.quiet)
        except OSError as exc:
            print(f"qubicle: cannot write SVG: {exc}", file=sys.stderr)
            return 2
        print(f"qubicle: wrote {args.svg}", file=sys.stderr)

    render = render_ascii(qr.modules, quiet=args.quiet) if args.ascii \
        else render_terminal(qr.modules, quiet=args.quiet)
    print(render)
    return 0


if __name__ == "__main__":
    sys.exit(main())
