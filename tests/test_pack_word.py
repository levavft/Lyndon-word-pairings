import pytest
from word import Word
from oracles.word_oracle import (
    packed as oracle_packed,
    is_packed as oracle_is_packed,
    is_lyndon as oracle_is_lyndon,
    all_words_upto_length,
)
from fixtures.word_examples import EXAMPLES, as_word


@pytest.mark.parametrize("ex", EXAMPLES, ids=lambda ex: ex.word or "ε")
def test_pack_word_expected_output(ex):
    """Golden packed forms from the catalog."""
    w = as_word(ex)
    packed = w.packed()
    got = "" if repr(packed) == "ε" else repr(packed)
    assert got == ex.packed, f"{ex.word!r} → {got!r} (expected {ex.packed!r})"
    assert packed == oracle_packed(w)


@pytest.mark.parametrize("ex", EXAMPLES, ids=lambda ex: ex.word or "ε")
def test_packing_preserves_lyndon(ex):
    """Packing should not alter Lyndon status (catalog + oracle)."""
    w = as_word(ex)
    pw = w.packed()
    assert w.is_lyndon() == pw.is_lyndon(), f"Lyndon status changed for {ex.word!r}"
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
    assert oracle_is_lyndon(w.packed()) == oracle_is_lyndon(oracle_packed(w))
