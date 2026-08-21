"""Conjecture: M(n+2) equals the central binomial coefficient."""

from __future__ import annotations

import math
from dataclasses import dataclass

from pairing_helpers import PairingMatrix
from word import Word

from hypotheses.core import Hypothesis, HypothesisResult, MathStatement, Status


@dataclass(frozen=True)
class MMismatch:
    """Witness when observed M(depth) disagrees with the conjectured value."""

    depth: int
    observed_M: int
    expected: int
    witness_group: str
    witness_row: str
    witness_col: str
    value: int


STATEMENT = MathStatement(
    latex=(
        r"M(n)=\max\lvert\text{entries of the fundamental matrix of depth }n\rvert"
        r";\quad "
        r"M(n+2)=\left\lvert\binom{n}{\lfloor n/2\rfloor}\right\rvert"
    ),
    prose=(
        "The fundamental matrix of depth n is the pairing matrix of all packed "
        "Lyndon words of length <= n. It is block-diagonal with blocks indexed by "
        "signature (permutation class ∩ Lyndon ∩ packed). M(n) is the max absolute "
        "entry over those blocks. Conjecture: M(n+2) = |C(n, floor(n/2))|."
    ),
)


def fundamental_M(n: int) -> tuple[int, str | None, str | None, str | None, int | None]:
    """Return (M(n), group, row, col, value) for the max-abs entry witness."""
    best = 0
    wit_group = wit_row = wit_col = None
    wit_val = None
    for sig, words in Word.grouped_lyndon_words(n, packed=True).items():
        pm = PairingMatrix(words)
        for i, row in enumerate(pm.matrix):
            for j, c in enumerate(row):
                if abs(c) > best:
                    best = abs(c)
                    wit_group = sig
                    wit_row = repr(pm.words[i])
                    wit_col = repr(pm.words[j])
                    wit_val = c
    return best, wit_group, wit_row, wit_col, wit_val


def expected_M(depth: int) -> int:
    """Conjectured M(depth) = C(depth-2, floor((depth-2)/2)) for depth ≥ 2."""
    k = depth - 2
    return math.comb(k, k // 2)


def check(n_max: int = 5) -> HypothesisResult:
    """Check M(d) == expected_M(d) for each depth d in 2..n_max."""
    if n_max < 2:
        return HypothesisResult(
            status=Status.UNCHECKED,
            checked_up_to={"n_max": n_max},
            notes="Need n_max ≥ 2 to check any depth.",
        )

    mismatches: list[MMismatch] = []
    for depth in range(2, n_max + 1):
        observed, g, r, c, v = fundamental_M(depth)
        expected = expected_M(depth)
        if observed != expected:
            mismatches.append(
                MMismatch(
                    depth=depth,
                    observed_M=observed,
                    expected=expected,
                    witness_group=g or "",
                    witness_row=r or "",
                    witness_col=c or "",
                    value=v if v is not None else 0,
                )
            )

    if mismatches:
        return HypothesisResult(
            status=Status.REFUTED,
            checked_up_to={"n_max": n_max},
            counterexamples=tuple(mismatches),
            notes="Observed M(depth) disagreed with central-binomial prediction.",
        )

    return HypothesisResult(
        status=Status.HOLDS_UP_TO,
        checked_up_to={"n_max": n_max},
        notes=f"M(d) matched C(d-2, floor((d-2)/2)) for all d in 2..{n_max}.",
    )


RESULT = HypothesisResult(
    status=Status.HOLDS_UP_TO,
    checked_up_to={"n_max": 6},
    notes="M(d) matched C(d-2, floor((d-2)/2)) for all d in 2..6.",
)

ITEM = Hypothesis(
    id="fundamental_m_central_binomial",
    name="Fundamental matrix max vs central binomial",
    statement=STATEMENT,
    check=check,
    result=RESULT,
)
