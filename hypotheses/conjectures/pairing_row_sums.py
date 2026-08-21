"""Falsified conjecture: pairing-matrix row sums lie in {-1, 0, 1}."""

from __future__ import annotations

from dataclasses import dataclass

from pairing_helpers import PairingMatrix
from word import Word

from hypotheses.core import Hypothesis, HypothesisResult, MathStatement, Status


@dataclass(frozen=True)
class RowSumCounterexample:
    """Failure locus for the row-sum conjecture."""

    n: int
    group_signature: str
    row_word: str
    row_index: int
    row_sum: int


STATEMENT = MathStatement(
    latex=(
        r"\forall\text{ packed Lyndon signature blocks }B,\ "
        r"\forall\text{ rows }v\text{ of }B:\ "
        r"\sum_w \langle v,w\rangle \in \{-1,0,1\}"
    ),
    prose=(
        "In every signature-block pairing matrix of packed Lyndon words of length "
        "<= n, each row sums to -1, 0, or 1. This conjecture is false."
    ),
)


def check(n: int = 4) -> HypothesisResult:
    """Find rows whose sum is outside {-1, 0, 1}."""
    counterexamples: list[RowSumCounterexample] = []
    for sig, words in Word.grouped_lyndon_words(n, packed=True).items():
        pm = PairingMatrix(words)
        for i, row in enumerate(pm.matrix):
            s = sum(row)
            if s not in (-1, 0, 1):
                counterexamples.append(
                    RowSumCounterexample(
                        n=n,
                        group_signature=sig,
                        row_word=repr(pm.words[i]),
                        row_index=i,
                        row_sum=s,
                    )
                )

    if counterexamples:
        return HypothesisResult(
            status=Status.REFUTED,
            checked_up_to={"n": n},
            counterexamples=tuple(counterexamples),
            notes="At least one row sum outside {-1, 0, 1}.",
        )

    return HypothesisResult(
        status=Status.HOLDS_UP_TO,
        checked_up_to={"n": n},
        notes=f"All row sums in {{-1,0,1}} for packed Lyndon groups with length <= {n}.",
    )


RESULT = HypothesisResult(
    status=Status.REFUTED,
    checked_up_to={"n": 5},
    counterexamples=(
        RowSumCounterexample(
            n=5,
            group_signature="aabbb",
            row_word="aabbb",
            row_index=0,
            row_sum=-2,
        ),
        RowSumCounterexample(
            n=5,
            group_signature="aabcc",
            row_word="abcac",
            row_index=4,
            row_sum=2,
        ),
        RowSumCounterexample(
            n=5,
            group_signature="aabcd",
            row_word="abdac",
            row_index=9,
            row_sum=2,
        ),
    ),
    notes="Refuted at n=5; first failure is group aabbb, row aabbb, sum=-2.",
)

ITEM = Hypothesis(
    id="pairing_row_sums_in_pm1",
    name="Pairing-matrix row sums in {-1, 0, 1}",
    statement=STATEMENT,
    check=check,
    result=RESULT,
)
