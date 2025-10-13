import random
import pytest
from word import Word
from nc_polynomial import NCPolynomial




# -------------------------------
# Benchmark helpers
# -------------------------------

def random_word(max_len=10):
    n = random.randint(1, max_len)
    return Word(tuple(random.randint(0, len(alphabet) - 1) for _ in range(n)))


def random_polynomial(nterms=20, max_len=6, alphabet=ALPHABET, coeff_range=(-5, 5)):
    terms = {}
    for _ in range(nterms):
        w = tuple(random.randint(0, len(alphabet) - 1) for _ in range(random.randint(0, max_len)))
        c = 0
        while c == 0:
            c = random.randint(*coeff_range)
        terms[w] = c
    return NCPolynomial(terms)


# -------------------------------
# Word benchmarks
# -------------------------------

@pytest.mark.benchmark(group="word-lyndon")
def test_lyndon_check_benchmark(benchmark):
    """Benchmark is_lyndon() on random words."""
    words = [random_word(max_len=20) for _ in range(200)]

    def run():
        for w in words:
            _ = w.is_lyndon()

    benchmark(run)


@pytest.mark.benchmark(group="word-bracketing")
def test_standard_bracketing_benchmark(benchmark):
    """Benchmark standard_bracketing() on random Lyndon and non-Lyndon words."""
    words = [random_word(max_len=10) for _ in range(100)]

    def run():
        for w in words:
            _ = w.standard_bracketing()

    benchmark(run)


# -------------------------------
# NCPolynomial benchmarks
# -------------------------------

@pytest.mark.benchmark(group="poly-addition")
@pytest.mark.parametrize("size", [50, 100, 200, 400])
def test_polynomial_addition_scaling(benchmark, size):
    """Measure time for adding two sparse polynomials of increasing size."""
    p = random_polynomial(nterms=size)
    q = random_polynomial(nterms=size)

    benchmark(lambda: p + q)


@pytest.mark.benchmark(group="poly-multiplication")
@pytest.mark.parametrize("size", [5, 10, 20, 40])
def test_polynomial_multiplication_scaling(benchmark, size):
    """Measure polynomial multiplication scaling."""
    p = random_polynomial(nterms=size, max_len=3)
    q = random_polynomial(nterms=size, max_len=3)

    benchmark(lambda: p * q)


@pytest.mark.benchmark(group="poly-degree")
@pytest.mark.parametrize("size", [50, 100, 500])
def test_degree_computation_scaling(benchmark, size):
    """Measure degree() performance with varying number of terms."""
    p = random_polynomial(nterms=size, max_len=6)

    benchmark(p.degree)
