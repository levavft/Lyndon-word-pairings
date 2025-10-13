import pytest
import random
from word import Word
from nc_polynomial import NCPolynomial


ALPHABET = "abcd"  # small for tractable enumeration


# -------------------------------
# Random word generation helpers
# -------------------------------

def random_word(max_len=6, alphabet=ALPHABET):
    n = random.randint(1, max_len)
    return Word(tuple(random.randint(0, len(alphabet)-1) for _ in range(n)))


def random_polynomial(nterms=3, max_len=5, alphabet=ALPHABET, coeff_range=(-3, 3)):
    """Generate a random sparse NCPolynomial."""
    terms = {}
    for _ in range(nterms):
        w = tuple(random.randint(0, len(alphabet)-1) for _ in range(random.randint(0, max_len)))
        c = 0
        while c == 0:
            c = random.randint(*coeff_range)
        terms[w] = c
    return NCPolynomial(terms)


# -------------------------------
# Property tests for Word
# -------------------------------

def test_random_lyndon_invariance_under_rotation():
    """If a word is Lyndon, all its rotations should not be smaller."""
    for _ in range(100):
        w = random_word()
        if w.is_lyndon():
            for r in w._rotations():
                assert w.letters < r


def test_random_lyndon_factorization_reconstruction():
    """Reconstruct word from its Chen-Fox-Lyndon factors."""
    for _ in range(100):
        w = random_word()
        factors = w.lyndon_factorization()
        reconstructed = tuple(sum([list(f.letters) for f in factors], []))
        assert reconstructed == w.letters


def test_random_standard_bracketing_returns_valid_polynomial():
    """Every word’s bracketing yields a valid NCPolynomial with correct degree."""
    for _ in range(50):
        w = random_word(max_len=5)
        p = w.standard_bracketing()
        assert isinstance(p, NCPolynomial)
        assert p.degree() <= len(w)
        # check coefficients are ints
        assert all(isinstance(c, int) for c in p.terms.values())


def test_random_standard_bracketing_factorization_compatibility():
    """
    If w is not Lyndon, then its standard bracketing should equal the
    product of its Lyndon factors' bracketings.
    """
    for _ in range(50):
        w = random_word(max_len=5)
        if not w.is_lyndon():
            factors = w.lyndon_factorization()
            expected = factors[0].standard_bracketing()
            for f in factors[1:]:
                expected = expected * f.standard_bracketing()
            actual = w.standard_bracketing()
            # They should have identical term sets (since all deterministic)
            assert expected.terms == actual.terms


# -------------------------------
# Property tests for NCPolynomial
# -------------------------------

def test_random_addition_commutativity():
    """Addition must be commutative."""
    for _ in range(100):
        p = random_polynomial()
        q = random_polynomial()
        assert (p + q).terms == (q + p).terms


def test_random_multiplication_associativity():
    """Multiplication should be associative."""
    for _ in range(50):
        p = random_polynomial(nterms=2)
        q = random_polynomial(nterms=2)
        r = random_polynomial(nterms=2)
        left = (p * q) * r
        right = p * (q * r)
        assert left.terms == right.terms


def test_random_distributivity():
    """p*(q+r) = p*q + p*r"""
    for _ in range(50):
        p = random_polynomial(nterms=2)
        q = random_polynomial(nterms=2)
        r = random_polynomial(nterms=2)
        left = p * (q + r)
        right = p * q + p * r
        assert left.terms == right.terms


def test_scalar_multiplication_linear_properties():
    """Check that integer scalar multiplication distributes and is associative."""
    for _ in range(50):
        p = random_polynomial()
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        # scalar distributivity: a*(p + q) = a*p + a*q
        q = random_polynomial()
        assert (a * (p + q)).terms == (a * p + a * q).terms
        # associativity: (a*b)*p = a*(b*p)
        assert ((a * b) * p).terms == (a * (b * p)).terms


def test_degree_monotonicity_under_multiplication():
    """deg(p*q) = deg(p) + deg(q)"""
    for _ in range(100):
        p = random_polynomial(nterms=2, max_len=3)
        q = random_polynomial(nterms=2, max_len=3)
        expected_deg = p.degree() + q.degree()
        assert (p * q).degree() == expected_deg
