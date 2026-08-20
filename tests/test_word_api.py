"""API / edge-case coverage for Word (ctors, ops, helpers)."""

import pytest
from word import Word


def test_int_constructor():
    # Digits map as d -> d-1 (1->a, 3->c, 4->d)
    w = Word(341)
    assert w.to_tuple() == (2, 3, 0)
    assert repr(w) == "cda"


def test_equality():
    assert Word("ab") == Word((0, 1))
    assert Word("a") != "a"
    assert Word("a") != (0,)
    assert Word("a") != Word("b")


def test_add_type_error():
    with pytest.raises(TypeError, match="Word"):
        Word("a") + "b"


def test_radd():
    # Normal + uses __add__; exercise __radd__ explicitly (same Word+Word path)
    assert Word("b").__radd__(Word("a")) == Word("ab")
    assert Word(()) + Word("a") == Word("a")
    with pytest.raises(TypeError, match="Word"):
        "x" + Word("a")


def test_rotations_include_trivial():
    w = Word("abc")
    rots = list(w._rotations(include_trivial=True))
    assert rots[0] == w.letters
    assert rots[1:] == [(1, 2, 0), (2, 0, 1)]


def test_to_tuple_signature_typst():
    w = Word("bac")
    assert w.to_tuple() == (1, 0, 2)
    assert w.signature() == "abc"
    typst = w.to_typst()
    assert typst.startswith("$(") and typst.endswith(")$")
    assert "b" in typst and "a" in typst and "c" in typst
