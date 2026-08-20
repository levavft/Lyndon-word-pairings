from config import Config
from itertools import product
from collections import defaultdict


class Word:
    """Immutable word over a finite alphabet, represented as a tuple of ints."""

    __slots__ = ('letters', 'alphabet')

    def __init__(self, letters=()):
        self.alphabet = Config.alphabet
        
        if isinstance(letters, str):
            # Convert string to integer indices (a→0, b→1, etc.)
            self.letters = tuple(self.alphabet.index(ch) for ch in letters)
        elif isinstance(letters, int):
            # Convert an integer to indices. (1->0, 2->1, etc. For each digit)
            self.letters = tuple(int(d)-1 for d in str(letters))
        else:
            self.letters = tuple(letters)

    def __repr__(self):
        if not self.letters:
            return "ε"  # epsilon for empty word
        return ''.join(self.alphabet[i] for i in self.letters)

    def __len__(self):
        return len(self.letters)

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.letters == other.letters

    def __lt__(self, other):
        return self.letters < other.letters

    def __add__(self, other):
        """Concatenate two words."""
        if isinstance(other, Word):
            return Word(self.letters + other.letters)
        raise TypeError("Word can only be concatenated with Word")

    def __radd__(self, other):
        """Concatenate two words."""
        if isinstance(other, Word):
            return Word(other.letters + self.letters)
        raise TypeError("Word can only be concatenated with Word")

    def _rotations(self, include_trivial=False):
        """All nontrivial rotations of the word."""
        if include_trivial:
            yield self.letters
        for i in range(1, len(self.letters)):
            yield self.letters[i:] + self.letters[:i]

    def is_lyndon(self):
        """
        True iff the word is Lyndon: nonempty and strictly lexicographically
        smaller than all of its nontrivial rotations.

        TODO: consider the equivalent "smaller than all nontrivial suffixes"
        characterization, which is probably faster.
        """
        if not self.letters:
            return False
        return all(self.letters < rot for rot in self._rotations())

    def to_tuple(self):
        return self.letters

    def signature(self):
        """Signature for grouping by multiset of letters."""
        return "".join(sorted(self.__repr__()))

    def to_typst(self):
        internal = " ".join(self.__repr__())
        return f"$({internal})$"

    # ---------- Lyndon factorization ----------

    def standard_factorization(self):
        """
        Return (u, v) such that w = uv and v is the longest proper Lyndon suffix.

        Defined for every word of length greater than 1 (not only Lyndon words).
        Every such word has at least one proper Lyndon suffix (its last letter).
        """
        n = len(self.letters)
        if n <= 1:
            raise ValueError("standard_factorization requires a word of length > 1")
        for i in range(1, n):
            v = Word(self.letters[i:])
            if v.is_lyndon():
                u = Word(self.letters[:i])
                return u, v
        raise ValueError(  # pragma: no cover — every len>1 word has a Lyndon last letter
            f"standard_factorization: no proper Lyndon suffix (word={self!r}). "
            "This is mathematically impossible; investigate."
        )

    # ---------- Standard bracketing ----------

    def standard_bracketing(self):
        """
        Return the standard bracketing of this word as a nested tuple of Words
        (letters are leaves). Defined for every nonempty word via recursive
        longest-proper-Lyndon-suffix factorization, not only for Lyndon words.
        """
        if len(self.letters) == 0:
            raise ValueError("standard_bracketing requires a nonempty word")
        if len(self.letters) == 1:
            return self

        u, v = self.standard_factorization()
        return u.standard_bracketing(), v.standard_bracketing()

    # ---------- Packing -------------------

    def packed(self):
        """
        Compute the packed (tassé) form of a word, preserving its relative order pattern.
        That is, relabel distinct letters of the word by 0,1,2,... according to their
        order in the base alphabet, not the order of first appearance.

        Example (alphabet = a<b<c<d):
            abc -> abc
            acb -> acb
            bda -> bcb -> abc (same structure)
        """
        if not self.letters:
            return Word(())

        # Extract the set of letters that appear, sorted by the base alphabet order
        distinct_sorted = sorted(set(self.letters))
        # Map each letter to its rank in that sorted set
        rank_map = {letter: i for i, letter in enumerate(distinct_sorted)}
        # Apply mapping to get packed indices
        packed_indices = tuple(rank_map[i] for i in self.letters)
        return Word(packed_indices)

    def is_packed(self):
        """
        True iff the letters form {0, 1, ..., m-1} for m = number of distinct
        letters. The empty word is considered packed.
        """
        if not self.letters:
            return True
        s = set(self.letters)
        return max(s) == len(s) - 1
    # ---------- Static methods --------------

    @staticmethod
    def all_words_upto_length(n, packed=True, k=None, *, include_empty=False):
        """
        Generate all words of length ≤ n over an alphabet of size k.

        If k is omitted, it defaults to n (the usual thesis case). Optionally
        restrict to packed (tassé) words, deduplicated by letter tuple.
        """
        if k is None:
            k = n
        if n < 0:
            raise ValueError("n must be non-negative")
        if k < 0:
            raise ValueError("alphabet size k must be non-negative")

        # TODO - there is clearly a more efficient algorithm
        seen = set()
        if include_empty:
            yield Word(())
        for length in range(1, n + 1):
            for letters in product(Config.alphabet[:k], repeat=length):
                w = Word("".join(letters))
                if packed:
                    w = w.packed()
                    t = w.to_tuple()
                    if t in seen:
                        continue
                    seen.add(t)
                yield w

    @staticmethod
    def lyndon_words_upto(n, packed=True):
        return Word._lyndon_words_upto_duval(n, packed)

    @staticmethod
    def _lyndon_words_upto_duval(n, packed=True):
        """Return all Lyndon words of length ≤ n in the alphabet of size n (optionally only packed ones)."""
        words = []
        w = [-1]  # set up for first increment
        while w:
            w[-1] += 1  # increment the last non-z symbol
            candidate = Word(tuple(w))
            if not packed or candidate == candidate.packed():
                words.append(candidate)
            m = len(w)
            while len(w) < n:  # repeat word to fill exactly n syms
                w.append(w[-m])
            while w and w[-1] == n - 1:  # delete trailing z's
                w.pop()
        return words

    @staticmethod
    def grouped_lyndon_words(n, packed=True):
        """Group Lyndon words by permutation equivalence."""
        groups = defaultdict(list)
        for w in Word.lyndon_words_upto(n, packed):
            groups[w.signature()].append(w)
        return dict(groups)


if __name__ == "__main__":  # pragma: no cover
    word = Word(341)
    print(word.standard_factorization())
    print(word.standard_bracketing())