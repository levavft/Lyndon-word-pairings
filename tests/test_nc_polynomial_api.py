"""API / edge-case coverage for NCPolynomial (ctors, ops, helpers)."""

import pytest
from nc_polynomial import NCPolynomial
from word import Word


def test_monomial():
    p = NCPolynomial.monomial((0, 1), 3)
    assert p.terms == {(0, 1): 3}
    assert repr(p) == "3ab"

    q = NCPolynomial.monomial((1,), -1)
    assert q.terms == {(1,): -1}
    assert repr(q) == "-b"


def test_from_word():
    w = Word("ab")
    p = NCPolynomial.from_word(w)
    assert p.terms == {(0, 1): 1}
    assert NCPolynomial.from_word(w, coeff=4).terms == {(0, 1): 4}


def test_copy_is_independent():
    p = NCPolynomial({(0,): 1, (1,): 2})
    q = p.copy()
    assert q == p
    assert q is not p
    assert q.terms is not p.terms
    q.terms[(0,)] = 99
    assert p.terms[(0,)] == 1


def test_vars_string_sets_arity_only():
    """String form of vars() sets arity; token names do not rename generators."""
    a, b, c = NCPolynomial.vars(3)
    assert a.terms == {(0,): 1}
    assert b.terms == {(1,): 1}
    assert c.terms == {(2,): 1}

    x, y, z = NCPolynomial.vars("x y z")
    assert x.terms == {(0,): 1}
    assert y.terms == {(1,): 1}
    assert z.terms == {(2,): 1}
    assert (x, y, z) == (a, b, c)
    assert (repr(x), repr(y), repr(z)) == ("a", "b", "c")


def test_from_word_and_P_type_error():
    with pytest.raises(TypeError, match="Word"):
        NCPolynomial.from_word("ab")
    with pytest.raises(TypeError, match="Word"):
        NCPolynomial.P("ab")
    with pytest.raises(TypeError, match="Word"):
        NCPolynomial.from_word((0, 1))
    with pytest.raises(TypeError, match="Word"):
        NCPolynomial.P((0, 1))


def test_radd_rsub_rmul_int_and_bad_types():
    a = NCPolynomial.vars(1)[0]
    assert 2 + a == NCPolynomial({(): 2, (0,): 1})
    assert 2 - a == NCPolynomial({(): 2, (0,): -1})
    assert 3 * a == NCPolynomial({(0,): 3})

    with pytest.raises(TypeError, match=r"\+"):
        "x" + a
    with pytest.raises(TypeError, match=r"-"):
        "x" - a
    with pytest.raises(TypeError, match=r"\*"):
        "x" * a


def test_zero_coeff_stripped_on_init():
    p = NCPolynomial({(0,): 0, (1,): 2, (2,): 0})
    assert p.terms == {(1,): 2}


def test_empty_degree_and_missing_coefficient():
    zero = NCPolynomial()
    assert zero.terms == {}
    assert zero.degree() == float("-inf")
    assert zero.get_coefficient(Word("a")) == 0

    p = NCPolynomial.monomial((0,), 5)
    assert p.get_coefficient(Word("a")) == 5
    assert p.get_coefficient(Word("b")) == 0


def test_neg_and_eq():
    a, b = NCPolynomial.vars(2)
    p = a + 2 * b
    assert (-p).terms == {(0,): -1, (1,): -2}
    assert -(-p) == p

    assert a == NCPolynomial({(0,): 1})
    assert a != b
    assert a != "a"
    assert NCPolynomial() == NCPolynomial({})
