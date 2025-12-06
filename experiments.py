from word import Word
from pairing_helpers import *


def find_maximal_abs_value_of_coefficient_of_P(words):
    max_coeff, max_word, max_poly = 0, None, None
    for word in words:
        poly = NCPolynomial.P(word)
        if len(poly.terms.values()) == 0:
            continue
        m_coeff = max(map(abs, poly.terms.values()))
        if m_coeff > max_coeff:
            max_coeff, max_word, max_poly = m_coeff, word, poly
            print(f"{max_coeff=}\t{max_word=}\t{max_poly=}")
    return max_coeff, max_word, max_poly



def main():
    n = 5
    words = list(Word.all_words_upto_length(n, True))
    # words = lyndon_words_upto(n, True)  # need to add a Lyndon only option to find_.... for this to make sense...
    print(find_maximal_abs_value_of_coefficient_of_P(words))


if __name__ == "__main__":
    main()
