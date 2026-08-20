import pytest
from word import Word


@pytest.mark.parametrize(
    "input_word,expected",
    [
        ("abc", "abc"),     # already packed
        ("acb", "acb"),     # distinct letters, preserves order pattern
        ("bca", "bca"),     # shift in alphabet, still pattern 'abc'
        ("cba", "cba"),     # descending order
        ("bac", "bac"),     # permutation pattern preserved
        ("bdb", "aba"),     # letters b<d → a<b → pattern aba
        ("abac", "abac"),
        ("abad", "abac"),
    ],
)
def test_pack_word_expected_output(input_word, expected):
    """Check that pack_word produces correct packed (tassé) words."""
    w = Word(input_word)
    packed = w.packed()
    assert repr(packed) == expected, f"{input_word} → {repr(packed)} (expected {expected})"


@pytest.mark.parametrize("word_str", ["abc", "acb", "bca", "bac", "cab", "cba"])
def test_packing_preserves_lyndon(word_str):
    """Packing should not alter Lyndon status for canonical pattern words."""
    w = Word(word_str)
    pw = w.packed()
    assert w.is_lyndon() == pw.is_lyndon(), f"Lyndon status changed for {word_str} → {repr(pw)}"

