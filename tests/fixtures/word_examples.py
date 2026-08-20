"""Handmade golden examples for Word — single source of truth for manual tests.

Edit EXAMPLES to add or change curated words. Run tests to check consistency
with the definitional oracle.
"""

from __future__ import annotations

from dataclasses import dataclass

from word import Word


@dataclass(frozen=True)
class WordExample:
    word: str
    is_lyndon: bool
    packed: str  # expected packed form as alphabet string ("" for empty)
    factorization: tuple[str, str] | None  # None if len <= 1
    bracketing: object | None  # nested str tuples / letter str; None if empty
    notes: str = ""


EXAMPLES: tuple[WordExample, ...] = (
    WordExample("", False, "", None, None, notes="empty → ε"),
    WordExample("a", True, "a", None, "a"),
    WordExample("b", True, "a", None, "b"),
    WordExample("c", True, "a", None, "c"),
    WordExample("d", True, "a", None, "d"),
    WordExample("ab", True, "ab", ("a", "b"), ("a", "b")),
    WordExample("ac", True, "ab", ("a", "c"), ("a", "c")),
    WordExample("ad", True, "ab", ("a", "d"), ("a", "d")),
    WordExample("cd", True, "ab", ("c", "d"), ("c", "d")),
    WordExample("ba", False, "ba", ("b", "a"), ("b", "a"), notes="non-Lyndon"),
    WordExample("aba", False, "aba", ("ab", "a"), (("a", "b"), "a"), notes="non-Lyndon"),
    WordExample("abb", True, "abb", ("ab", "b"), (("a", "b"), "b")),
    WordExample("abc", True, "abc", ("a", "bc"), ("a", ("b", "c"))),
    WordExample("acb", True, "acb", ("ac", "b"), (("a", "c"), "b")),
    WordExample("bcd", True, "abc", ("b", "cd"), ("b", ("c", "d"))),
    WordExample("abcd", True, "abcd", ("a", "bcd"), ("a", ("b", ("c", "d")))),
    WordExample("accd", True, "abbc", ("a", "ccd"), ("a", ("c", ("c", "d")))),
    WordExample("acbc", True, "acbc", ("ac", "bc"), (("a", "c"), ("b", "c"))),
    WordExample("abac", True, "abac", ("ab", "ac"), (("a", "b"), ("a", "c"))),
    WordExample(
        "abad", True, "abac", ("ab", "ad"), (("a", "b"), ("a", "d")), notes="packs to abac"
    ),
    WordExample(
        "adab", False, "acab", ("ad", "ab"), (("a", "d"), ("a", "b")), notes="packs to acab"
    ),
    WordExample(
        "bdb", False, "aba", ("bd", "b"), (("b", "d"), "b"), notes="packing nontrivial"
    ),
    WordExample("bac", False, "bac", ("b", "ac"), ("b", ("a", "c"))),
    WordExample("bca", False, "bca", ("bc", "a"), (("b", "c"), "a")),
    WordExample("cab", False, "cab", ("c", "ab"), ("c", ("a", "b"))),
    WordExample("cba", False, "cba", ("cb", "a"), (("c", "b"), "a")),
)


def examples() -> tuple[WordExample, ...]:
    return EXAMPLES


def examples_with_factorization() -> tuple[WordExample, ...]:
    return tuple(ex for ex in EXAMPLES if ex.factorization is not None)


def examples_with_bracketing() -> tuple[WordExample, ...]:
    return tuple(ex for ex in EXAMPLES if ex.bracketing is not None)


def as_word(ex: WordExample) -> Word:
    return Word(()) if ex.word == "" else Word(ex.word)


def bracketing_as_words(tree: object) -> object:
    """Convert nested str bracketing to nested Word leaves (same shape as production)."""
    if isinstance(tree, str):
        return Word(tree)
    if isinstance(tree, tuple):
        return tuple(bracketing_as_words(x) for x in tree)
    raise TypeError(f"unexpected bracketing node: {tree!r}")
