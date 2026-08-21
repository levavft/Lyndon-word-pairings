"""Exploration: maximal absolute coefficient appearing in P(w)."""

from __future__ import annotations

from nc_polynomial import NCPolynomial
from word import Word

from hypotheses.core import Exploration, ExplorationResult

# Checked-in snapshot from a previous run (update deliberately after re-running).
RESULT = ExplorationResult(
    observations={
        "max_abs": 6,
        "word": "aaaab",
        "poly_repr": "aaaab - 4aaaba + 6aabaa - 4abaaa + baaaa",
    },
    params={"n": 5, "packed": True},
    notes="Snapshot from packed words of length <= 5.",
)


def run(n: int = 5) -> ExplorationResult:
    """Find max |coeff| of P(w) over packed words of length ≤ n."""
    max_coeff = 0
    max_word = None
    max_poly = None
    for word in Word.all_words_upto_length(n, True):
        poly = NCPolynomial.P(word)
        if not poly.terms:
            continue
        m_coeff = max(map(abs, poly.terms.values()))
        if m_coeff > max_coeff:
            max_coeff, max_word, max_poly = m_coeff, word, poly

    return ExplorationResult(
        observations={
            "max_abs": max_coeff,
            "word": None if max_word is None else repr(max_word),
            "poly_repr": None if max_poly is None else repr(max_poly),
        },
        params={"n": n, "packed": True},
        notes="Max absolute coefficient among all terms of P(w) for packed words <= n.",
    )


ITEM = Exploration(
    id="max_abs_p_coefficient",
    name="Max absolute coefficient in P(w)",
    description=(
        "Among packed words of length <= n, find the largest absolute coefficient "
        "appearing in any P(w), with a witness word and polynomial."
    ),
    goal_latex=r"\max_w \max_c \lvert [w^c] P(w) \rvert",
    run=run,
    result=RESULT,
)
