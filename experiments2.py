from word import Word
# from math import log10


def lyndon_words_upto_duval(n, packed=True):
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


def packed_lyndon_words_upto(n):
    """Return all packed Lyndon words of length ≤ n in the alphabet of size n."""
    """
    It is a simple modification of Duval's algorithm.
    1. Since Duval's algorithm generates words in lexicographical order, and since all letters in a Lyndon word must be
        greater or equal than the first letter of the word, we stop generating words once the first letter is increased.
    2. We only add the packed words to our list.
    
    """
    words = []
    w = [-1]
    while w:
        w[-1] += 1
        if w[0] > 0:
            break
        candidate = Word(tuple(w))
        if candidate == candidate.packed():
            words.append(candidate)
        m = len(w)
        while len(w) < n:  # repeat word to fill exactly n syms
            w.append(w[-m])
        while w and w[-1] == n - 1:  # delete trailing z's
            w.pop()
    return words


def packed_lyndon_words_upto_v2(n):
    """Return all packed Lyndon words of length ≤ n in the alphabet of size n."""
    """
    It is a simple modification of Duval's algorithm.
    1. Since Duval's algorithm generates words in lexicographical order, and since all letters in a Lyndon word must be
        greater or equal than the first letter of the word, we stop generating words once the first letter is increased.
    2. We only add the packed words to our list.

    """
    words = []
    w = [-1]
    while w:
        w[-1] += 1
        if w[0] > 0:
            break
        candidate = Word(tuple(w))
        if candidate.is_packed():
            words.append(candidate)
        w = w * (n // len(w) + 1)
        w = w[:n]
        while w and w[-1] == n - 1:  # delete trailing z's
            w.pop()
    return words


def packed_lyndon_words_upto_v3(n):
    """Return all packed Lyndon words of length ≤ n in the alphabet of size n."""
    """
    It is a simple modification of Duval's algorithm.
    1. Since Duval's algorithm generates words in lexicographical order, and since all letters in a Lyndon word must be
        greater or equal than the first letter of the word, we stop generating words once the first letter is increased.
    2. We only add the packed words to our list.

    """
    words = []
    w = [-1]
    while w:
        w[-1] += 1
        if w[0] > 0:
            break
        candidate = Word(tuple(w))
        if candidate.is_packed():
            words.append(candidate)
        w = w * (n // len(w) + 1)
        w = w[:n]
        while w and w[-1] == n - 1:  # delete trailing z's
            w.pop()
    return words


def packed_lyndon_words_upto_numerical(n):
    """Return all packed Lyndon words of length ≤ n in the alphabet of size n."""
    """
    It is a simple modification of Duval's algorithm.
    1. Since Duval's algorithm generates words in lexicographical order, and since all letters in a Lyndon word must be
        greater or equal than the first letter of the word, we stop generating words once the first letter is increased.
    2. We only add the packed words to our list.
    3. We use numerical operations instead of list operations.

    """
    words = []
    w = 0
    powers_of_10 = [10 ** i for i in range(n + 1)]

    while True:
        w += 1
        m = len(str(w))
        # m = int(log10(w)) + 1
        ten_pow = powers_of_10[m-1]
        if w // ten_pow > 1:
            break

        candidate = Word(w)
        if candidate == candidate.packed():
            words.append(candidate)

        ten_pow = powers_of_10[m]
        ww = w
        while ww < powers_of_10[n-1]:
            ww = ww * ten_pow + w
        while ww > powers_of_10[n]:
            ww //= 10
        while ww != 0 and ww % 10 == n:  # delete trailing z's
            ww //= 10
        w = ww
    return words


if __name__ == "__main__":
    # for w in packed_lyndon_words_upto(4):
    #     print(w)
    # packed_lyndon_words_upto(4)
    n = 7
    # x = packed_lyndon_words_upto(n)
    # y = packed_lyndon_words_upto_numerical(n)
    x = packed_lyndon_words_upto_v2(n)
    z = packed_lyndon_words_upto_v3(n)
    # print(x == y)
    print(x == z)