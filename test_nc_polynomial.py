import pytest
from nc_polynomial import NCPolynomial  # adjust if your file has a different name


@pytest.fixture
def setup_vars():
    a, b, c = NCPolynomial.vars(3)
    return a, b, c


def test_basic_repr(setup_vars):
    a, b, c = setup_vars
    assert repr(a) == "a"
    assert repr(b) == "b"
    assert repr(a * b) == "ab"
    assert repr(a * b - b * a) == "ab - ba"
    assert repr(a * b - b * a + 3) == "3 + ab - ba"


def test_integer_multiplication(setup_vars):
    a, b, _ = setup_vars
    p = a * b - b * a
    assert repr(3 * p) == "3ab - 3ba"
    assert repr(p * 2) == "2ab - 2ba"
    assert repr(3 * p + 2) == "2 + 3ab - 3ba"


def test_addition_and_subtraction(setup_vars):
    a, b, c = setup_vars
    p = a * b + b * c
    q = b * c - a * b
    r = p + q
    s = p - q
    assert repr(r) == "2bc"
    assert repr(s) == "2ab"


def test_noncommutativity(setup_vars):
    a, b, _ = setup_vars
    ab = a * b
    ba = b * a
    assert repr(ab) == "ab"
    assert repr(ba) == "ba"
    assert ab != ba
    assert repr(ab - ba) == "ab - ba"


def test_degree(setup_vars):
    a, b, c = setup_vars
    p = a * b - b * a + 3
    q = a * b * a * c
    assert p.degree() == 2
    assert q.degree() == 4


def test_zero_behavior(setup_vars):
    a, b, _ = setup_vars
    zero = a - a
    assert repr(zero) == "0"
    assert zero.degree() == float("-inf")
    assert repr(zero + 5) == "5"
    assert repr(5 + zero) == "5"
    assert repr(zero * a) == "0"
    assert repr(a * zero) == "0"


def test_scalar_addition_and_subtraction(setup_vars):
    a, b, _ = setup_vars
    p = a * b
    assert repr(p + 5) == "5 + ab"
    assert repr(p - 5) == "-5 + ab"
    assert repr(5 + p) == "5 + ab"
    assert repr(5 - p) == "5 - ab"


def test_distributivity(setup_vars):
    a, b, _ = setup_vars
    left = a * (b + 2)
    right = a * b + 2 * a
    assert repr(left) == repr(right)


def test_longer_expressions(setup_vars):
    a, b, c = setup_vars
    p = a * b - b * a + 3
    q = 2 * a - 5 * b * c + 4
    pq = p * q
    s = repr(pq)
    # Basic structural checks
    assert "ab" in s
    assert "ba" in s
    assert "bc" in s
    assert s.count("+") + s.count("-") > 0  # multiple terms
