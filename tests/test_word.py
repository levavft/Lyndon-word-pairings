import pytest
from word import Word
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    standard_factorization as oracle_standard_factorization,
    standard_bracketing as oracle_standard_bracketing,
    all_words_upto_length,
)


@pytest.fixture
def setup_letters():
    return [Word(l) for l in "abc"]


def test_word_basic_repr(setup_letters):
    a, b, _ = setup_letters
    assert repr(a) == "a"
    assert repr(b) == "b"
    assert repr(a + b) == "ab"
    assert repr(b + a) == "ba"
    assert repr(b + b + a + b) == "bbab"
    assert repr(Word(())) == "ε"


def test_word_comparisons(setup_letters):
    a, b, c = setup_letters
    assert a < b < c
    assert Word("ab") < Word("ac")
    assert not (Word("b") < Word("a"))


def test_is_lyndon_basic(setup_letters):
    a, b, c = setup_letters
    assert a.is_lyndon()
    assert b.is_lyndon()
    assert Word("ab").is_lyndon()
    assert not Word("ba").is_lyndon()
    assert Word("abc").is_lyndon()
    assert not Word("aba").is_lyndon()
    assert not Word(()).is_lyndon()


def test_empty_is_packed_and_packed():
    empty = Word(())
    assert empty.is_packed()
    assert empty.packed() == empty


def test_standard_factorization_rejects_short_words():
    with pytest.raises(ValueError, match="length > 1"):
        Word(()).standard_factorization()
    with pytest.raises(ValueError, match="length > 1"):
        Word("a").standard_factorization()


def test_standard_bracketing_rejects_empty():
    with pytest.raises(ValueError, match="nonempty"):
        Word(()).standard_bracketing()


def test_standard_factorization_for_lyndon():
    factorizations = {
        "ab": ("a", "b"),
        "ac": ("a", "c"),
        "ad": ("a", "d"),
        "abb": ("ab", "b"),
        "acb": ("ac", "b"),
        "abcd": ("a", "bcd"),
        "accd": ("a", "ccd"),
        "acbc": ("ac", "bc"),
    }

    for word, fac in factorizations.items():
        w = Word(word)
        factorization = w.standard_factorization()
        assert isinstance(factorization[0], Word)
        assert isinstance(factorization[1], Word)
        assert factorization[1].is_lyndon()
        assert tuple(map(repr, factorization)) == fac


def test_standard_bracketing():
    def wordify(tup):
        for obj in tup:
            if isinstance(obj, str):
                yield Word(obj)
            else:
                yield tuple(wordify(obj))

    bracketings = {
        "ab": ("a", "b"),
        "ac": ("a", "c"),
        "ad": ("a", "d"),
        "cd": ("c", "d"),
        "ba": ("b", "a"),  # non-Lyndon
        "aba": (("a", "b"), "a"),  # non-Lyndon
        "abb": (("a", "b"), "b"),
        "acb": (("a", "c"), "b"),
        "bcd": ("b", ("c", "d")),
        "abcd": ("a", ("b", ("c", "d"))),
        "accd": ("a", ("c", ("c", "d"))),
        "acbc": (("a", "c"), ("b", "c")),
    }

    for word, br in bracketings.items():
        w = Word(word)
        expected = tuple(wordify(br))
        assert w.standard_bracketing() == expected
        assert oracle_standard_bracketing(w) == expected


def test_is_lyndon_exhaustive_len_le_4_alphabet_4():
    for w in all_words_upto_length(4, 4):
        assert w.is_lyndon() == oracle_is_lyndon(w)


def test_standard_factorization_exhaustive_len_le_4_alphabet_4():
    for w in all_words_upto_length(4, 4):
        if len(w) <= 1:
            continue

        expected_u, expected_v = oracle_standard_factorization(w)
        got_u, got_v = w.standard_factorization()

        assert (got_u, got_v) == (expected_u, expected_v)
        assert repr(got_u) + repr(got_v) == repr(w)
        assert oracle_is_lyndon(got_v)

        # v is the longest proper Lyndon suffix: no longer proper suffix is Lyndon
        split = len(w) - len(expected_v)
        for i in range(1, split):
            assert not oracle_is_lyndon(Word(w.letters[i:]))


def test_standard_bracketing_exhaustive_len_le_4_alphabet_4():
    """Bracketing is defined for every nonempty word, not only Lyndon words."""
    for w in all_words_upto_length(4, 4):
        assert w.standard_bracketing() == oracle_standard_bracketing(w)
