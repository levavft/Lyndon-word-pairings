"""Handmade golden examples for NC polynomials and Lyndon P_w.

Edit POLY_EXAMPLES / PWORD_EXAMPLES to add or change curated cases.
Run tests/test_poly_examples.py to check consistency with the poly oracle.
"""

from __future__ import annotations

from dataclasses import dataclass

from oracles.nc_polynomial_oracle import Terms, terms_from_str_map


@dataclass(frozen=True)
class PolyExample:
    name: str
    terms: dict[str, int]  # "" key for constant term; omit zeros
    notes: str = ""


@dataclass(frozen=True)
class PWordExample:
    word: str
    p_terms: dict[str, int]
    notes: str = ""


# Migrated from handmade expectations in tests/test_nc_polynomial.py
POLY_EXAMPLES: tuple[PolyExample, ...] = (
    PolyExample("zero", {}, notes="a - a"),
    PolyExample("a", {"a": 1}),
    PolyExample("b", {"b": 1}),
    PolyExample("ab", {"ab": 1}),
    PolyExample("ba", {"ba": 1}),
    PolyExample("ab-ba", {"ab": 1, "ba": -1}, notes="commutator"),
    PolyExample("3+ab-ba", {"": 3, "ab": 1, "ba": -1}),
    PolyExample("3*(ab-ba)", {"ab": 3, "ba": -3}),
    PolyExample("(ab-ba)*2", {"ab": 2, "ba": -2}),
    PolyExample("3*(ab-ba)+2", {"": 2, "ab": 3, "ba": -3}),
    PolyExample("2bc", {"bc": 2}, notes="(ab+bc)+(bc-ab)"),
    PolyExample("2ab", {"ab": 2}, notes="(ab+bc)-(bc-ab)"),
    PolyExample("ab+5", {"": 5, "ab": 1}),
    PolyExample("ab-5", {"": -5, "ab": 1}),
    PolyExample("5-ab", {"": 5, "ab": -1}),
    PolyExample("constant-5", {"": 5}, notes="zero + 5"),
    PolyExample("abac", {"abac": 1}, notes="a*b*a*c degree-4 monomial"),
)


# Lyndon words from the word catalog.
# p_terms were dumped from oracle.P then hand-reviewed; they are not an
# independent derivation (shared factorization bugs would agree with oracle.P).
# Small hand spot-checks and thesis-verified pairing CSVs are the independent checks.
PWORD_EXAMPLES: tuple[PWordExample, ...] = (
    PWordExample("a", {"a": 1}),
    PWordExample("b", {"b": 1}),
    PWordExample("c", {"c": 1}),
    PWordExample("d", {"d": 1}),
    PWordExample("ab", {"ab": 1, "ba": -1}),
    PWordExample("ac", {"ac": 1, "ca": -1}),
    PWordExample("ad", {"ad": 1, "da": -1}),
    PWordExample("cd", {"cd": 1, "dc": -1}),
    PWordExample("abb", {"abb": 1, "bab": -2, "bba": 1}),
    PWordExample(
        "abc",
        {"abc": 1, "acb": -1, "bca": -1, "cba": 1},
    ),
    PWordExample(
        "acb",
        {"acb": 1, "cab": -1, "bac": -1, "bca": 1},
    ),
    PWordExample(
        "bcd",
        {"bcd": 1, "bdc": -1, "cdb": -1, "dcb": 1},
    ),
    PWordExample(
        "abcd",
        {
            "abcd": 1,
            "abdc": -1,
            "acdb": -1,
            "adcb": 1,
            "bcda": -1,
            "bdca": 1,
            "cdba": 1,
            "dcba": -1,
        },
    ),
    PWordExample(
        "accd",
        {
            "accd": 1,
            "acdc": -2,
            "adcc": 1,
            "ccda": -1,
            "cdca": 2,
            "dcca": -1,
        },
    ),
    PWordExample(
        "acbc",
        {
            "acbc": 1,
            "accb": -1,
            "cabc": -1,
            "cacb": 1,
            "bcac": -1,
            "bcca": 1,
            "cbac": 1,
            "cbca": -1,
        },
    ),
    PWordExample(
        "abac",
        {
            "abac": 1,
            "abca": -1,
            "baac": -1,
            "baca": 1,
            "acab": -1,
            "acba": 1,
            "caab": 1,
            "caba": -1,
        },
    ),
    PWordExample(
        "abad",
        {
            "abad": 1,
            "abda": -1,
            "baad": -1,
            "bada": 1,
            "adab": -1,
            "adba": 1,
            "daab": 1,
            "daba": -1,
        },
        notes="packs to abac",
    ),
)


def poly_examples() -> tuple[PolyExample, ...]:
    return POLY_EXAMPLES


def pword_examples() -> tuple[PWordExample, ...]:
    return PWORD_EXAMPLES


def as_terms(ex: PolyExample | PWordExample) -> Terms:
    """Oracle terms dict from a catalog str→coeff map."""
    if isinstance(ex, PolyExample):
        return terms_from_str_map(ex.terms)
    return terms_from_str_map(ex.p_terms)
