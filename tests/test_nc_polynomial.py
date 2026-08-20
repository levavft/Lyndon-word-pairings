"""NCPolynomial: catalog goldens and algebra laws vs the poly oracle (terms = truth)."""

import pytest
from nc_polynomial import NCPolynomial
from fixtures.poly_examples import POLY_EXAMPLES, PolyExample, as_terms
from oracles.nc_polynomial_oracle import (
    add as oracle_add,
    mul as oracle_mul,
    degree as oracle_degree,
)


def build_poly_example(ex: PolyExample) -> NCPolynomial:
    """Evaluate the expression implied by each catalog entry (not a terms round-trip)."""
    a, b, c = NCPolynomial.vars(3)
    builders = {
        "zero": lambda: a - a,
        "a": lambda: a,
        "b": lambda: b,
        "ab": lambda: a * b,
        "ba": lambda: b * a,
        "ab-ba": lambda: a * b - b * a,
        "3+ab-ba": lambda: 3 + (a * b - b * a),
        "3*(ab-ba)": lambda: 3 * (a * b - b * a),
        "(ab-ba)*2": lambda: (a * b - b * a) * 2,
        "3*(ab-ba)+2": lambda: 3 * (a * b - b * a) + 2,
        "2bc": lambda: (a * b + b * c) + (b * c - a * b),
        "2ab": lambda: (a * b + b * c) - (b * c - a * b),
        "ab+5": lambda: a * b + 5,
        "ab-5": lambda: a * b - 5,
        "5-ab": lambda: 5 - a * b,
        "constant-5": lambda: (a - a) + 5,
        "abac": lambda: a * b * a * c,
    }
    try:
        return builders[ex.name]()
    except KeyError as err:
        raise AssertionError(
            f"No expression builder for POLY_EXAMPLES entry {ex.name!r}"
        ) from err


@pytest.fixture
def setup_vars():
    return NCPolynomial.vars(3)


# ---------- Catalog goldens (evaluate expressions) ----------


@pytest.mark.parametrize("ex", POLY_EXAMPLES, ids=lambda ex: ex.name)
def test_poly_example_expression_matches_catalog(ex):
    p = build_poly_example(ex)
    assert p.terms == as_terms(ex)


# ---------- Repr smoke (readability only; terms remain source of truth) ----------


def test_repr_smoke(setup_vars):
    a, b, _ = setup_vars
    assert repr(a) == "a"
    assert repr(a * b - b * a) == "ab - ba"
    assert repr(a - a) == "0"
    assert repr(a * b + 3) == "3 + ab"


# ---------- Algebra laws vs oracle ----------


def test_addition_associativity_and_commutativity(setup_vars):
    a, b, c = setup_vars
    p = a * b + 2
    q = b * c - a
    r = 3 * a - b

    assert (p + q).terms == oracle_add(p.terms, q.terms)
    assert (p + q).terms == (q + p).terms
    assert ((p + q) + r).terms == (p + (q + r)).terms
    assert ((p + q) + r).terms == oracle_add(oracle_add(p.terms, q.terms), r.terms)


def test_zero_absorber(setup_vars):
    a, b, _ = setup_vars
    zero = a - a
    p = a * b - b * a + 3

    assert zero.terms == {}
    assert (zero + p).terms == p.terms == oracle_add({}, p.terms)
    assert (p + zero).terms == p.terms
    assert (zero * p).terms == {} == oracle_mul({}, p.terms)
    assert (p * zero).terms == {}
    assert (zero * a).terms == {}
    assert (a * zero).terms == {}
    assert zero.degree() == float("-inf") == oracle_degree({})


def test_scalar_multiplication(setup_vars):
    a, b, _ = setup_vars
    p = a * b - b * a

    assert (3 * p).terms == oracle_mul(3, p.terms)
    assert (p * 2).terms == oracle_mul(p.terms, 2)
    assert (0 * p).terms == {}
    assert (p * 0).terms == {}
    assert (3 * p + 2).terms == oracle_add(oracle_mul(3, p.terms), 2)


def test_distributivity(setup_vars):
    a, b, _ = setup_vars
    left = a * (b + 2)
    right = a * b + 2 * a
    expected = oracle_mul(a.terms, oracle_add(b.terms, 2))

    assert left.terms == right.terms == expected

    left2 = (a + b) * (a - 1)
    right2 = a * a - a + b * a - b
    expected2 = oracle_mul(oracle_add(a.terms, b.terms), oracle_add(a.terms, -1))
    assert left2.terms == right2.terms == expected2


def test_hand_built_ops_match_oracle(setup_vars):
    a, b, c = setup_vars
    p = a * b + b * c
    q = b * c - a * b

    assert (p + q).terms == oracle_add(p.terms, q.terms)
    assert (p - q).terms == oracle_add(p.terms, oracle_mul(-1, q.terms))
    assert (p * q).terms == oracle_mul(p.terms, q.terms)
    assert (p + 5).terms == oracle_add(p.terms, 5)
    assert (5 - p).terms == oracle_add(5, oracle_mul(-1, p.terms))
    assert p.degree() == oracle_degree(p.terms)
    assert (a * b * a * c).degree() == 4 == oracle_degree((a * b * a * c).terms)
