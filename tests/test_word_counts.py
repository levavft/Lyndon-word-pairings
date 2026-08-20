import pytest
from word import Word
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    is_packed as oracle_is_packed,
    lyndon_count,
    all_words_of_length,
    all_words_upto_length,
)


@pytest.mark.parametrize(
    "n,k",
    [
        (1, 1),
        (1, 2),
        (1, 4),
        (2, 2),
        (2, 3),
        (3, 3),
        (3, 2),
        (3, 4),
        (4, 4),
        (4, 2),
        (4, 3),
    ],
)
def test_witt_formula_exact_length(n, k):
    """Oracle Lyndon count of exact length n over alphabet k matches Witt formula."""
    count = sum(1 for w in all_words_of_length(n, k) if oracle_is_lyndon(w))
    assert count == lyndon_count(n, k)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_duval_unpacked_matches_oracle_lyndon(n):
    """Duval packed=False equals all oracle-Lyndon words of length ≤ n over alphabet n."""
    duval = {w.letters for w in Word.lyndon_words_upto(n, packed=False)}
    oracle = {
        w.letters
        for w in all_words_upto_length(n, n)
        if oracle_is_lyndon(w)
    }
    assert duval == oracle


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_duval_packed_subset_and_cover(n):
    """
    Duval packed=True words are oracle-packed and oracle-Lyndon;
    every packed oracle-Lyndon word of length ≤ n over alphabet n appears.
    """
    duval = list(Word.lyndon_words_upto(n, packed=True))
    duval_letters = {w.letters for w in duval}

    for w in duval:
        assert oracle_is_packed(w)
        assert oracle_is_lyndon(w)

    packed_oracle_lyndon = {
        w.letters
        for w in all_words_upto_length(n, n)
        if oracle_is_lyndon(w) and oracle_is_packed(w)
    }
    assert packed_oracle_lyndon == duval_letters
