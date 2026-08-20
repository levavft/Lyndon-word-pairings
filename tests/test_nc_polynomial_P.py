"""NCPolynomial.P: catalog goldens, exhaustive Lyndon, structural, get_coefficient."""

import pytest
from word import Word
from nc_polynomial import NCPolynomial
from fixtures.poly_examples import PWORD_EXAMPLES, as_terms
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    all_words_upto_length,
    standard_factorization as oracle_standard_factorization,
)
from oracles.nc_polynomial_oracle import (
    P as oracle_P,
    mul as oracle_mul,
    sub as oracle_sub,
    get_coefficient as oracle_get_coefficient,
)


# ---------- Catalog P_w goldens ----------


@pytest.mark.parametrize("ex", PWORD_EXAMPLES, ids=lambda ex: ex.word)
def test_pword_example_matches_production_and_oracle(ex):
    w = Word(ex.word)
    got = NCPolynomial.P(w).terms
    expected_catalog = as_terms(ex)
    expected_oracle = oracle_P(w)
    assert got == expected_catalog == expected_oracle


# ---------- Exhaustive Lyndon up to length 4 ----------


@pytest.mark.parametrize(
    "w",
    [w for w in all_words_upto_length(4, 4) if oracle_is_lyndon(w)],
    ids=repr,
)
def test_P_lyndon_exhaustive_matches_oracle(w):
    assert NCPolynomial.P(w).terms == oracle_P(w)


# ---------- Structural: P(w) = [P(u), P(v)] via standard factorization ----------


@pytest.mark.parametrize(
    "w",
    [w for w in all_words_upto_length(4, 4) if len(w) > 1],
    ids=repr,
)
def test_P_structural_commutator_of_factors(w):
    u, v = oracle_standard_factorization(w)
    pu_oracle, pv_oracle = oracle_P(u), oracle_P(v)
    expected_oracle = oracle_sub(
        oracle_mul(pu_oracle, pv_oracle),
        oracle_mul(pv_oracle, pu_oracle),
    )

    pu, pv = NCPolynomial.P(u), NCPolynomial.P(v)
    expected_prod = (pu * pv - pv * pu).terms
    got = NCPolynomial.P(w).terms

    # Production P(w) equals both [P(u), P(v)] and the oracle expansion.
    assert got == expected_prod == expected_oracle


# ---------- get_coefficient ----------


def test_get_coefficient_spot_checks():
    ab = NCPolynomial.P(Word("ab"))
    assert ab.get_coefficient(Word("ab")) == 1
    assert ab.get_coefficient(Word("ba")) == -1
    assert ab.get_coefficient(Word("a")) == 0

    abb = NCPolynomial.P(Word("abb"))
    assert abb.get_coefficient(Word("abb")) == 1
    assert abb.get_coefficient(Word("bab")) == -2
    assert abb.get_coefficient(Word("bba")) == 1
    assert abb.get_coefficient(Word("aaa")) == 0


@pytest.mark.parametrize(
    "v",
    list(Word.lyndon_words_upto(3, packed=False)),
    ids=repr,
)
def test_get_coefficient_vs_oracle_lyndon_upto_3(v):
    p = NCPolynomial.P(v)
    p_terms = oracle_P(v)
    # Probe every word of length ≤ len(v) over the same alphabet size
    k = max(v.letters) + 1 if v.letters else 1
    for w in all_words_upto_length(len(v), k):
        assert p.get_coefficient(w) == oracle_get_coefficient(p_terms, w)


# ---------- Non-Lyndon P (bracketing-on-all-words policy) ----------


@pytest.mark.parametrize("s", ["ba", "aba"])
def test_P_non_lyndon_matches_oracle(s):
    w = Word(s)
    assert not oracle_is_lyndon(w)
    assert NCPolynomial.P(w).terms == oracle_P(w)
