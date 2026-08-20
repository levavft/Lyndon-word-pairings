import pytest
from word import Word
from oracles.word_oracle import (
    packed as oracle_packed,
    is_packed as oracle_is_packed,
    is_lyndon as oracle_is_lyndon,
    all_words_upto_length,
)


@pytest.mark.parametrize(
    "input_word,expected",
    [
        ("abc", "abc"),  # already packed
        ("acb", "acb"),  # distinct letters, preserves order pattern
        ("bca", "bca"),  # shift in alphabet, still pattern 'abc'
        ("cba", "cba"),  # descending order
        ("bac", "bac"),  # permutation pattern preserved
        ("bdb", "aba"),  # letters b<d → a<b → pattern aba
        ("abac", "abac"),
        ("abad", "abac"),
    ],
)
def test_pack_word_expected_output(input_word, expected):
    """Golden packed forms, also matching the oracle."""
    w = Word(input_word)
    packed = w.packed()
    assert repr(packed) == expected, f"{input_word} → {repr(packed)} (expected {expected})"
    assert packed == oracle_packed(w)


@pytest.mark.parametrize("word_str", ["abc", "acb", "bca", "bac", "cab", "cba"])
def test_packing_preserves_lyndon(word_str):
    """Packing should not alter Lyndon status for canonical pattern words."""
    w = Word(word_str)
    pw = w.packed()
    assert w.is_lyndon() == pw.is_lyndon(), f"Lyndon status changed for {word_str} → {repr(pw)}"
    assert oracle_is_lyndon(w) == oracle_is_lyndon(oracle_packed(w))


@pytest.mark.parametrize("w", list(all_words_upto_length(4, 4)))
def test_packed_matches_oracle(w):
    assert w.packed() == oracle_packed(w)


@pytest.mark.parametrize("w", list(all_words_upto_length(4, 4)))
def test_is_packed_matches_oracle(w):
    assert w.is_packed() == oracle_is_packed(w)


@pytest.mark.parametrize("w", list(all_words_upto_length(4, 4)))
def test_packing_idempotence(w):
    prod_once = w.packed()
    oracle_once = oracle_packed(w)
    assert prod_once.packed() == prod_once
    assert oracle_packed(oracle_once) == oracle_once
    assert prod_once == oracle_once


@pytest.mark.parametrize("w", list(all_words_upto_length(4, 4)))
def test_packing_preserves_oracle_lyndon(w):
    assert oracle_is_lyndon(w) == oracle_is_lyndon(oracle_packed(w))
    # Production packed form agrees with oracle on Lyndon status
    assert oracle_is_lyndon(w.packed()) == oracle_is_lyndon(oracle_packed(w))
