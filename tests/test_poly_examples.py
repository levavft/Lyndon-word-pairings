"""Catalog self-check: handmade poly / P_w goldens agree with the poly oracle."""

import pytest
from word import Word
from fixtures.poly_examples import (
    POLY_EXAMPLES,
    PWORD_EXAMPLES,
    as_terms,
)
from oracles.nc_polynomial_oracle import (
    P as oracle_P,
    normalize,
    str_map_from_terms,
    terms_from_str_map,
)


@pytest.mark.parametrize("ex", POLY_EXAMPLES, ids=lambda ex: ex.name)
def test_poly_example_str_map_roundtrip(ex):
    terms = terms_from_str_map(ex.terms)
    assert normalize(terms) == terms
    assert as_terms(ex) == terms
    # Round-trip: str map → terms → str map recovers the nonzero catalog
    recovered = str_map_from_terms(terms)
    assert recovered == {k: v for k, v in ex.terms.items() if v != 0}


@pytest.mark.parametrize("ex", PWORD_EXAMPLES, ids=lambda ex: ex.word)
def test_pword_example_agrees_with_oracle_P(ex):
    got = oracle_P(Word(ex.word))
    expected = terms_from_str_map(ex.p_terms)
    assert got == expected
    assert as_terms(ex) == expected
