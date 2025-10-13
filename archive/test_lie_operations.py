import pytest
from word import Word
from lie_operations import P, pairing
from nc_polynomial import NCPolynomial


@pytest.fixture
def letters():
    return Word("a"), Word("b"), Word("c")


# --------------------------
# P_w basic structure tests
# --------------------------

def test_P_w_single_letters(letters):
    a, b, c = letters
    Pa = P(a)
    Pb = P(b)
    Pc = P(c)
    assert isinstance(Pa, NCPolynomial)
    assert repr(Pa) == "a"
    assert repr(Pb) == "b"
    assert repr(Pc) == "c"


def test_P_w_simple_lyndon(letters):
    a, b, _ = letters
    w = Word("ab")
    Pab = P(w)
    assert repr(Pab) == "ab - ba"
    assert Pab.degree() == 2
    # Check expected coefficients
    assert Pab.terms.get((0, 1)) == 1  # ab
    assert Pab.terms.get((1, 0)) == -1


def test_P_w_non_lyndon(letters):
    a, b, _ = letters
    w = Word("aba")  # not Lyndon
    Pw = P(w)
    # [ab][a] = (ab - ba)a = aba - baa
    assert repr(Pw) == "aba - baa"
    assert Pw.terms.get((0, 1, 0)) == 1
    assert Pw.terms.get((1, 0, 0)) == -1


def test_P_w_nested_lyndon(letters):
    a, b, c = letters
    w = Word("abc")
    Pabc = P(w)
    # [abc] = [[ab],[c]] = (ab - ba)c - c(ab - ba)
    assert set(Pabc.terms.keys()) == {
        (0, 1, 2),  # abc
        (1, 0, 2),  # bac
        (2, 0, 1),  # cab
        (2, 1, 0),  # cba
    }
    # Check correct signs
    assert Pabc.terms[(0, 1, 2)] == 1
    assert Pabc.terms[(1, 0, 2)] == -1
    assert Pabc.terms[(2, 0, 1)] == -1
    assert Pabc.terms[(2, 1, 0)] == 1


# --------------------------
# Pairing <v, w> tests
# --------------------------

def test_pairing_basic(letters):
    a, b, _ = letters
    ab = Word("ab")
    ba = Word("ba")
    assert pairing(ab, ab) == 1
    assert pairing(ab, ba) == -1
    assert pairing(ab, Word("aa")) == 0


def test_pairing_non_lyndon(letters):
    a, b, _ = letters
    w = Word("aba")
    assert pairing(w, Word("aba")) == 1
    assert pairing(w, Word("baa")) == -1
    assert pairing(w, Word("abb")) == 0


def test_pairing_nested_lyndon(letters):
    a, b, c = letters
    w = Word("abc")
    assert pairing(w, Word("abc")) == 1
    assert pairing(w, Word("bac")) == -1
    assert pairing(w, Word("cab")) == -1
    assert pairing(w, Word("cba")) == 1
    # orthogonality
    assert pairing(w, Word("acb")) == 0


# --------------------------
# Structural / Random checks
# --------------------------

def test_random_consistency_for_small_words():
    import random
    random.seed(42)
    alphabet = "abc"
    for _ in range(50):
        w = Word(tuple(random.randint(0, 2) for _ in range(random.randint(1, 4))), alphabet)
        Pv = P(w)
        # pairing should be within terms
        for term, coeff in Pv.terms.items():
            w2 = Word(term, alphabet)
            assert pairing(w, w2) == coeff
        # coefficient of a random nonterm word should be 0
        random_word = Word(tuple(random.randint(0, 2) for _ in range(random.randint(1, 4))), alphabet)
        if random_word.to_tuple() not in Pv.terms:
            assert pairing(w, random_word) == 0


def test_P_w_degree_matches_word_length():
    for s in ["a", "ab", "aba", "abc", "aab", "bac"]:
        w = Word(s)
        Pw = P(w)
        assert Pw.degree() <= len(s)
