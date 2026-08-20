"""
Slow definitional oracles for sparse noncommutative polynomials over Z.

Circularity: does not call NCPolynomial methods for arithmetic or P.
P uses word_oracle.standard_factorization (not Word.standard_factorization).
Uses Word only for construction / type checks, .letters, and .to_tuple.
Independent of production NCPolynomial control flow.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping

from config import Config
from oracles.word_oracle import standard_factorization
from word import Word

Terms = dict[tuple[int, ...], int]


def normalize(terms: Mapping[tuple[int, ...], int]) -> Terms:
    """Drop zero coefficients; coerce coeffs to int and keys to tuples."""
    return {tuple(w): int(c) for w, c in terms.items() if int(c) != 0}


def _coerce(x: Terms | int) -> Terms:
    if isinstance(x, int):
        return {(): int(x)} if x != 0 else {}
    if isinstance(x, Mapping):
        return normalize(x)
    raise TypeError(f"expected poly terms dict or int, got {type(x)!r}")


def add(a: Terms | int, b: Terms | int) -> Terms:
    """Poly + poly; ints are constant terms ``(): n``."""
    out: dict[tuple[int, ...], int] = defaultdict(int, _coerce(a))
    for w, c in _coerce(b).items():
        out[w] += c
    return normalize(out)


def neg(a: Terms | int) -> Terms:
    return {w: -c for w, c in _coerce(a).items()}


def sub(a: Terms | int, b: Terms | int) -> Terms:
    return add(a, neg(b))


def mul(a: Terms | int, b: Terms | int) -> Terms:
    """Noncommutative poly–poly multiply; either side may be an int scalar."""
    if isinstance(a, int) and not isinstance(b, int):
        if a == 0:
            return {}
        return normalize({w: a * c for w, c in _coerce(b).items()})
    if isinstance(b, int) and not isinstance(a, int):
        if b == 0:
            return {}
        return normalize({w: c * b for w, c in _coerce(a).items()})
    left, right = _coerce(a), _coerce(b)
    out: dict[tuple[int, ...], int] = defaultdict(int)
    for w1, c1 in left.items():
        for w2, c2 in right.items():
            out[w1 + w2] += c1 * c2
    return normalize(out)


def degree(terms: Mapping[tuple[int, ...], int]) -> int | float:
    """Max monomial length, or ``-inf`` for the zero polynomial."""
    t = normalize(terms)
    return max(len(w) for w in t) if t else float("-inf")


def monomial(word_tuple_or_letters, coeff: int = 1) -> Terms:
    """
    Monomial from a letter-index tuple/iterable, or an alphabet string (e.g. ``\"ab\"``).
    """
    if int(coeff) == 0:
        return {}
    if isinstance(word_tuple_or_letters, str):
        alphabet = Config.alphabet
        key = tuple(alphabet.index(ch) for ch in word_tuple_or_letters)
    else:
        key = tuple(word_tuple_or_letters)
    return {key: int(coeff)}


def from_word(word: Word, coeff: int = 1) -> Terms:
    if not isinstance(word, Word):
        raise TypeError("Expected a Word instance")
    if int(coeff) == 0:
        return {}
    return {word.to_tuple(): int(coeff)}


def get_coefficient(terms: Mapping[tuple[int, ...], int], word: Word) -> int:
    return int(normalize(terms).get(word.to_tuple(), 0))


def P(word: Word) -> Terms:
    """
    Lyndon polynomial P_w: length-1 → monomial; otherwise
    P(u)P(v) − P(v)P(u) for the oracle standard factorization w = uv.
    """
    if not isinstance(word, Word):
        raise TypeError("Expected a Word instance")
    if len(word) == 1:
        return from_word(word)
    u, v = standard_factorization(word)
    pu, pv = P(u), P(v)
    return sub(mul(pu, pv), mul(pv, pu))


def terms_from_str_map(mapping: dict[str, int]) -> Terms:
    """Convert ``{\"ab\": 1, \"ba\": -1}`` using Config.alphabet indices."""
    alphabet = Config.alphabet
    out: dict[tuple[int, ...], int] = defaultdict(int)
    for s, c in mapping.items():
        key = tuple(alphabet.index(ch) for ch in s)
        out[key] += int(c)
    return normalize(out)


def str_map_from_terms(terms: Mapping[tuple[int, ...], int]) -> dict[str, int]:
    """Inverse of terms_from_str_map (empty monomial → ``\"\"``)."""
    alphabet = Config.alphabet
    return {
        "".join(alphabet[i] for i in w): int(c)
        for w, c in normalize(terms).items()
    }
