from config import Config


class Word:
    """Immutable word over a finite alphabet, represented as a tuple of ints."""

    __slots__ = ('letters', 'alphabet')

    def __init__(self, letters=()):
        self.alphabet = Config.alphabet
        
        if isinstance(letters, str):
            # Convert string to integer indices (a→0, b→1, etc.)
            self.letters = tuple(self.alphabet.index(ch) for ch in letters)
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
        """Check if the word is Lyndon (strictly smaller than all its rotations)."""
        if not self.letters:
            return False
        return all(self.letters < rot for rot in self._rotations())

    def to_tuple(self):
        return self.letters



    # ---------- Lyndon factorization ----------

    def standard_factorization(self):
        """
        Return (u, v) such that w = uv, v is the longest proper Lyndon suffix.
        """
        for i in range(1, len(self.letters)):
            v = Word(self.letters[i:])
            if v.is_lyndon():
                u = Word(self.letters[:i])
                return u, v

        raise Exception("Unexpected path in code reached")

    # ---------- Standard bracketing ----------

    def standard_bracketing(self):
        """
        Return the standard bracketing [w] as an NCPolynomial.
        """

        if not self.is_lyndon():
            return None

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
        # Generate a consistent alphabet of the right size
        return Word(packed_indices)
