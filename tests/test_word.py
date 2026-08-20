import pytest
from word import Word
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    standard_factorization as oracle_standard_factorization,
    standard_bracketing as oracle_standard_bracketing,
    all_words_upto_length,
)
from fixtures.word_examples import (
    EXAMPLES,
    as_word,
    bracketing_as_words,
    examples_with_bracketing,
    examples_with_factorization,
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


@pytest.mark.parametrize("ex", EXAMPLES, ids=lambda ex: ex.word or "ε")
def test_is_lyndon_basic(ex):
    assert as_word(ex).is_lyndon() == ex.is_lyndon


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


@pytest.mark.parametrize(
    "ex", examples_with_factorization(), ids=lambda ex: ex.word
)
def test_standard_factorization_from_catalog(ex):
    w = as_word(ex)
    factorization = w.standard_factorization()
    assert isinstance(factorization[0], Word)
    assert isinstance(factorization[1], Word)
    assert factorization[1].is_lyndon()
    assert tuple(map(repr, factorization)) == ex.factorization


@pytest.mark.parametrize(
    "ex", examples_with_bracketing(), ids=lambda ex: ex.word
)
def test_standard_bracketing_from_catalog(ex):
    w = as_word(ex)
    expected = bracketing_as_words(ex.bracketing)
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
