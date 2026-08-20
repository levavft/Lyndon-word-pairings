"""Coverage for Word.all_words_upto_length and grouped_lyndon_words."""

import pytest
from word import Word
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    is_packed as oracle_is_packed,
    all_words_upto_length as oracle_all_words_upto_length,
)


@pytest.mark.parametrize("n", [1, 2, 3])
def test_all_words_upto_length_unpacked_default_k_equals_n(n):
    words = list(Word.all_words_upto_length(n, packed=False))
    expected_count = sum(n**L for L in range(1, n + 1))
    assert len(words) == expected_count
    for w in words:
        assert 1 <= len(w) <= n
        assert all(0 <= letter < n for letter in w.letters)


@pytest.mark.parametrize("n,k", [(3, 2), (4, 2), (2, 3)])
def test_all_words_upto_length_unpacked_general_k(n, k):
    words = list(Word.all_words_upto_length(n, packed=False, k=k))
    expected = {w.letters for w in oracle_all_words_upto_length(n, k)}
    assert {w.letters for w in words} == expected
    assert len(words) == sum(k**L for L in range(1, n + 1))


def test_all_words_upto_length_include_empty():
    words = list(Word.all_words_upto_length(1, packed=False, include_empty=True))
    assert Word(()) in words
    assert len(words) == 1 + 1  # ε and "a"


def test_all_words_upto_length_rejects_negative():
    with pytest.raises(ValueError, match="n must"):
        list(Word.all_words_upto_length(-1, packed=False))
    with pytest.raises(ValueError, match="alphabet size"):
        list(Word.all_words_upto_length(2, packed=False, k=-1))


@pytest.mark.parametrize("n", [1, 2, 3])
def test_all_words_upto_length_packed(n):
    words = list(Word.all_words_upto_length(n, packed=True))
    seen = set()
    for w in words:
        assert oracle_is_packed(w)
        assert w.is_packed()
        assert w.packed() == w
        t = w.letters
        assert t not in seen
        seen.add(t)


@pytest.mark.parametrize("n", [1, 2, 3])
@pytest.mark.parametrize("packed", [False, True])
def test_grouped_lyndon_words(n, packed):
    groups = Word.grouped_lyndon_words(n, packed=packed)
    duval = {w.letters for w in Word.lyndon_words_upto(n, packed=packed)}

    union = set()
    for key, members in groups.items():
        assert members
        for w in members:
            assert oracle_is_lyndon(w)
            assert w.signature() == key
            union.add(w.letters)

    assert union == duval
