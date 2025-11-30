import pytest
from word import Word
from nc_polynomial import NCPolynomial
from itertools import product


@pytest.fixture
def setup_letters():
    return [Word(l) for l in "abc"]


@pytest.fixture
def word_list():
    letters = "abcd"
    word_list = list(map("".join, product(letters, repeat=4)))
    lyndon_word_list = {"a", "b", "c", "d",
                        "ab", "ac", "ad", "bc", "bd", "cd",
                        "aab", "aac", "aad", "abb", "abc", "abd", "acb", "acc", "acd", "adb", "adc", "add",
                        "bbc", "bbd", "bcc", "bcd", "bdc", "bdd",
                        "ccd", "cdd",
                        "aaab", "aaac", "aaad", "aabb", "aabc", "aabd", "aacb", "aacc", "aacd", "aadb", "aadc", "aadd",
                        "abac", "abad", "abbb", "abbc", "abbd", "abcb", "abcc", "abcd", "abdb", "abdc", "abdd",
                        "acad", "acbb", "acbc", "acbd", "accb", "accc", "accd", "acdb", "acdc", "acdd",
                        "adbb", "adbc", "adbd", "adcb", "adcc", "adcd", "addb", "addc", "addd",
                        "bbbc", "bbbd", "bbcc", "bbcd", "bbdc", "bbdd",
                        "bcbd", "bccc", "bccd", "bcdc", "bcdd", "bdcc", "bdcd", "bddc", "bddd", "cccd", "ccdd", "cddd"
                        }
    # lyndon_word_factorizations = {"a": ("", "a"),
    #                               "b": ("", "b"),
    #                               "c": ("", "c"),
    #                               "d": ("", "d"),
    #                               "ab": ("a", "b"),
    #                               "ac",
    #                               "ad",
    #                               "bc",
    #                               "bd",
    #                               "cd",
    #                               "aab",
    #                               "aac",
    #                               "aad",
    #                               "abb",
    #                               "abc",
    #                               "abd",
    #                               "acb",
    #                               "acc",
    #                               "acd",
    #                               "adb",
    #                               "adc",
    #                               "add",
    #                               "bbc",
    #                               "bbd",
    #                               "bcc",
    #                               "bcd",
    #                               "bdc",
    #                               "bdd",
    #                               "ccd",
    #                               "cdd",
    #                               "aaab",
    #                               "aaac",
    #                               "aaad",
    #                               "aabb",
    #                               "aabc",
    #                               "aabd",
    #                               "aacb",
    #                               "aacc",
    #                               "aacd",
    #                               "aadb",
    #                               "aadc",
    #                               "aadd",
    #                               "abac",
    #                               "abad",
    #                               "abbb",
    #                               "abbc",
    #                               "abbd",
    #                               "abcb",
    #                               "abcc",
    #                               "abcd",
    #                               "abdb",
    #                               "abdc",
    #                               "abdd",
    #                               "acad",
    #                               "acbb",
    #                               "acbc",
    #                               "acbd",
    #                               "accb",
    #                               "accc",
    #                               "accd",
    #                               "acdb",
    #                               "acdc",
    #                               "acdd",
    #                               "adbb",
    #                               "adbc",
    #                               "adbd",
    #                               "adcb",
    #                               "adcc",
    #                               "adcd",
    #                               "addb",
    #                               "addc",
    #                               "addd",
    #                               "bbbc",
    #                               "bbbd",
    #                               "bbcc",
    #                               "bbcd",
    #                               "bbdc",
    #                               "bbdd",
    #                               "bcbd",
    #                               "bccc",
    #                               "bccd",
    #                               "bcdc",
    #                               "bcdd",
    #                               "bdcc",
    #                               "bdcd",
    #                               "bddc",
    #                               "bddd",
    #                               "cccd",
    #                               "ccdd",
    #                               "cddd"
    #                     }
    return word_list, lyndon_word_list


def test_word_basic_repr(setup_letters):
    a, b, _ = setup_letters
    assert repr(a) == "a"
    assert repr(b) == "b"
    assert repr(a + b) == "ab"
    assert repr(b + a) == "ba"
    assert repr(b + b + a + b) == "bbab"
    assert repr(Word(())) == "ε"


def test_word_comparisons(setup_letters):
    a, b, c = setup_letters
    assert a < b < c
    assert Word("ab") < Word("ac")
    assert not (Word("b") < Word("a"))


def test_is_lyndon_basic(setup_letters):
    a, b, c = setup_letters
    assert a.is_lyndon()
    assert b.is_lyndon()
    assert Word("ab").is_lyndon()
    assert not Word("ba").is_lyndon()
    assert Word("abc").is_lyndon()
    assert not Word("aba").is_lyndon()


def test_is_lyndon(word_list):
    word_list, lyndon_word_list = word_list
    for word in word_list:
        w = Word(word)
        assert w.is_lyndon() == (word in lyndon_word_list)


def test_standard_factorization_for_lyndon():
    factorizations = {
        "ab": ("a", "b"),
        "ac": ("a", "c"),
        "ad": ("a", "d"),
        "abb": ("ab", "b"),
        "acb": ("ac", "b"),
        "abcd": ("a", "bcd"),
        "accd": ("a", "ccd"),
        "acbc": ("ac", "bc")
    }

    for word, fac in factorizations.items():
        print(word, fac)
        w = Word(word)
        factorization = w.standard_factorization()
        assert isinstance(factorization[0], Word)
        assert isinstance(factorization[1], Word)
        assert factorization[1].is_lyndon()
        assert tuple(map(repr, factorization)) == fac


def test_lyndon_factorization_general():
    # TODO - DO I CARE ABOUT THIS TEST/ THIS FUNCTIONALITY?
    w = Word("aba")
    factors = w.lyndon_factorization()
    assert [repr(f) for f in factors] == ["ab", "a"]

    w2 = Word("baba")
    factors = w2.lyndon_factorization()
    assert [repr(f) for f in factors] == ["b", "ab", "a"]


def test_standard_bracketing():
    def wordify(tup):
        for obj in tup:
            if isinstance(obj, str):
                yield Word(obj)
            else:
                yield tuple(wordify(obj))


    bracketings = {
        "ab": ("a", "b"),
        "ac": ("a", "c"),
        "ad": ("a", "d"),
        "cd": ("c", "d"),
        "abb": (("a", "b"), "b"),
        "acb": (("a", "c"), "b"),
        "bcd": ("b", ("c", "d")),
        "abcd": ("a", ("b", ("c", "d"))),
        "accd": ("a", ("c", ("c", "d"))),
        "acbc": (("a", "c"), ("b", "c"))
    }

    for word, br in bracketings.items():
        w = Word(word)
        bracketing = w.standard_bracketing()
        assert bracketing == tuple(wordify(br))
