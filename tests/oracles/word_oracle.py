"""
Slow definitional oracles for Word / Lyndon properties.

Circularity: does not call Word.is_lyndon, Word.packed, Word.is_packed,
Word.standard_factorization, Word.standard_bracketing, or Duval generators.
Uses Word only for construction, .letters, and lex comparison via tuples / __lt__.
"""

from __future__ import annotations

from itertools import product
from typing import Iterator

from sympy import divisors, mobius
from word import Word


def is_lyndon(w: Word) -> bool:
    """Nonempty and strictly lexicographically smaller than every nontrivial rotation."""
    letters = w.letters
    n = len(letters)
    if n == 0:
        return False
    for i in range(1, n):
        rot = letters[i:] + letters[:i]
        if not (letters < rot):
            return False
    return True


def packed(w: Word) -> Word:
    """
    Packed (tassé) form: relabel distinct letters by 0,1,2,... according to
    their order in the base alphabet (not order of first appearance).

    Example (alphabet a<b<c<d): bda packs to bca.
    """
    letters = w.letters
    if not letters:
        return Word(())
    distinct_sorted = sorted(set(letters))
    rank_map = {letter: i for i, letter in enumerate(distinct_sorted)}
    return Word(tuple(rank_map[i] for i in letters))


def is_packed(w: Word) -> bool:
    """
    True iff letters form {0..m-1} for m = number of distinct letters.
    The empty word is considered packed.
    """
    letters = w.letters
    if not letters:
        return True
    s = set(letters)
    return max(s) == len(s) - 1


def standard_factorization(w: Word) -> tuple[Word, Word]:
    """
    Return (u, v) such that w = uv and v is the longest proper Lyndon suffix
    (Lyndon status via oracle is_lyndon).

    Defined for every word of length > 1 (not only Lyndon words). Raises
    ValueError for length ≤ 1, or if no proper Lyndon suffix exists (impossible).
    """
    letters = w.letters
    n = len(letters)
    if n <= 1:
        raise ValueError(
            "standard_factorization requires a word of length > 1"
        )
    # i=1 → longest proper suffix; then shorter
    for i in range(1, n):
        v = Word(letters[i:])
        if is_lyndon(v):
            u = Word(letters[:i])
            return u, v
    raise ValueError(
        f"standard_factorization: no proper Lyndon suffix (word={w!r}). "
        "This is mathematically impossible; investigate."
    )


def standard_bracketing(w: Word):
    """
    Standard bracketing as nested tuples of Words (same shape as production).

    Defined for every nonempty word via recursive longest-proper-Lyndon-suffix
    factorization (not only for Lyndon words). Length-1 words are leaves.
    """
    if len(w.letters) == 0:
        raise ValueError("standard_bracketing requires a nonempty word")
    if len(w.letters) == 1:
        return w
    u, v = standard_factorization(w)
    return standard_bracketing(u), standard_bracketing(v)


def lyndon_count(n: int, k: int) -> int:
    """
    Number of Lyndon words of length n over an alphabet of size k (Witt formula):

        (1/n) * sum_{d|n} μ(d) * k^{n/d}
    """
    if n < 1:
        raise ValueError("lyndon_count requires n >= 1")
    if k < 0:
        raise ValueError("lyndon_count requires k >= 0")
    return sum(int(mobius(d)) * (k ** (n // d)) for d in divisors(n)) // n


def all_words_of_length(L: int, k: int) -> Iterator[Word]:
    """All words of exact length L over letter indices 0...k-1."""
    if L < 0:
        raise ValueError("length must be non-negative")
    if k < 0:
        raise ValueError("alphabet size must be non-negative")
    if L == 0:
        yield Word(())
        return
    for letters in product(range(k), repeat=L):
        yield Word(letters)


def all_words_upto_length(
    n: int, k: int | None = None, *, include_empty: bool = False
) -> Iterator[Word]:
    """
    All words of length ≤ n over letter indices 0..k-1 (as Word objects).

    If k is omitted, it defaults to n (same convention as Word.all_words_upto_length).
    """
    if k is None:
        k = n
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0:
        raise ValueError("alphabet size must be non-negative")
    if include_empty:
        yield Word(())
    for L in range(1, n + 1):
        yield from all_words_of_length(L, k)
