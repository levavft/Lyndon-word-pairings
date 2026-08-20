"""Catalog self-check: handmade WordExample fields agree with the oracle."""

import pytest
from word import Word
from fixtures.word_examples import (
    EXAMPLES,
    as_word,
    bracketing_as_words,
)
from oracles.word_oracle import (
    is_lyndon as oracle_is_lyndon,
    packed as oracle_packed,
    standard_factorization as oracle_standard_factorization,
    standard_bracketing as oracle_standard_bracketing,
)


@pytest.mark.parametrize("ex", EXAMPLES, ids=lambda ex: ex.word or "ε")
def test_word_example_agrees_with_oracle(ex):
    w = as_word(ex)
    assert oracle_is_lyndon(w) == ex.is_lyndon

    packed_repr = repr(oracle_packed(w))
    if packed_repr == "ε":
        packed_repr = ""
    assert packed_repr == ex.packed

    if ex.factorization is None:
        assert len(w) <= 1
    else:
        u, v = oracle_standard_factorization(w)
        assert (repr(u), repr(v)) == ex.factorization

    if ex.bracketing is None:
        assert len(w) == 0
    else:
        expected = bracketing_as_words(ex.bracketing)
        assert oracle_standard_bracketing(w) == expected
