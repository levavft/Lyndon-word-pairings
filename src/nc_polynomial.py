from collections import defaultdict
from itertools import product
from word import Word
from config import Config

class NCPolynomial:
    """Sparse noncommutative polynomial over Z, in variables a,b,c,..."""
    __slots__ = ('terms', 'alphabet')

    def __init__(self, terms=None):
        self.terms = {tuple(w): int(c) for w, c in (terms or {}).items() if c != 0}
        self.alphabet = Config.alphabet

    @staticmethod
    def monomial(word, coeff=1):
        return NCPolynomial({tuple(word): int(coeff)})

    @staticmethod
    def vars(names_or_n=1):
        """Create a tuple of generator polynomials with indices 0..n-1.

        Generators always use letter indices ``0, 1, ...`` (printed via
        ``Config.alphabet`` as ``a, b, c, ...``). A string argument only
        sets the arity (number of whitespace-separated tokens); the token
        names themselves are ignored.

        Examples:
            NCPolynomial.vars(3)          -> (a, b, c)
            NCPolynomial.vars('x y z')    -> (a, b, c)  # arity 3; names ignored
        """
        alphabet = Config.alphabet
        if isinstance(names_or_n, int):
            names = [alphabet[i] for i in range(names_or_n)]
        else:
            names = names_or_n.split()

        vars_list = []
        for i, _ in enumerate(names):
            vars_list.append(NCPolynomial({(i,): 1}))
        return tuple(vars_list)

    # ---------- Representation ----------
    def __repr__(self):
        if not self.terms:
            return "0"

        parts = []
        for w, c in sorted(self.terms.items()):
            word_str = ''.join(self.alphabet[i] for i in w) or ''

            # Handle coefficient formatting
            if c == 1 and word_str:
                coeff_str = ""
            elif c == -1 and word_str:
                coeff_str = "-"
            else:
                coeff_str = str(c)

            parts.append(coeff_str + word_str if word_str else coeff_str)

        # Combine with proper signs
        s = parts[0]
        for part in parts[1:]:
            if part.startswith('-'):
                s += " - " + part[1:]
            else:
                s += " + " + part
        return s

    # ---------- Arithmetic ----------
    def __add__(self, other):
        if isinstance(other, int):
            other = NCPolynomial({(): other})
        out = defaultdict(int, self.terms)
        for w, c in other.terms.items():
            newc = out[w] + c
            if newc:
                out[w] = newc
            elif w in out:
                del out[w]
        return NCPolynomial(dict(out))

    def __radd__(self, other):
        """Right-hand addition (for int + poly)."""
        if isinstance(other, int):
            return self + other
        raise TypeError(f"Unsupported operand types for +: {type(other)} and NCPolynomial")

    def __neg__(self):
        return NCPolynomial({w: -c for w, c in self.terms.items()})

    def __eq__(self, other):
        if not isinstance(other, NCPolynomial):
            return NotImplemented
        return self.terms == other.terms

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        """Right-hand subtraction (for int - poly)."""
        if isinstance(other, int):
            return (-self) + other
        raise TypeError(f"Unsupported operand types for -: {type(other)} and NCPolynomial")

    def __mul__(self, other):
        if isinstance(other, int):
            return NCPolynomial({w: c * other for w, c in self.terms.items()})
        out = defaultdict(int)
        for (w1, c1), (w2, c2) in product(self.terms.items(), other.terms.items()):
            w = w1 + w2
            out[w] += c1 * c2
            if out[w] == 0:
                del out[w]
        return NCPolynomial(dict(out))

    def __rmul__(self, other):
        """Right-hand multiplication (for int * poly)."""
        if isinstance(other, int):
            return NCPolynomial({w: other * c for w, c in self.terms.items()})
        raise TypeError(f"Unsupported operand types for *: {type(other)} and NCPolynomial")

    # ---------- Utilities ----------
    def degree(self):
        return max(len(w) for w in self.terms) if self.terms else -float("inf")

    def copy(self):
        return NCPolynomial(dict(self.terms))

    def get_coefficient(self, word):
        return self.terms.get(word.to_tuple(), 0)

    @staticmethod
    def from_word(word, coeff=1):
        """Create a monomial polynomial from a Word instance."""
        if not isinstance(word, Word):
            raise TypeError("Expected a Word instance")
        return NCPolynomial({word.to_tuple(): int(coeff)})

    @staticmethod
    def P(word):
        """Lie polynomial of a nonempty word via nested commutators.

        Recursively uses standard factorization: for |w|=1 return the
        monomial; otherwise if w = uv then P(w) = [P(u), P(v)] =
        P(u)P(v) - P(v)P(u). Works for any nonempty word that admits
        factorization; pairing applications typically use Lyndon words.
        """
        if not isinstance(word, Word):
            raise TypeError("Expected a Word instance")

        if len(word) == 1:
            return NCPolynomial.from_word(word)

        u, v = word.standard_factorization()
        pu = NCPolynomial.P(u)
        pv = NCPolynomial.P(v)
        return pu * pv - pv * pu