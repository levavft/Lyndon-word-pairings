"""Ordered catalog of hypotheses and explorations."""

from __future__ import annotations

from hypotheses.conjectures import fundamental_m_central_binomial, pairing_row_sums
from hypotheses.core import Exploration, Hypothesis
from hypotheses.explorations import max_abs_p_coefficient

ITEMS: list[Hypothesis | Exploration] = [
    max_abs_p_coefficient.ITEM,
    fundamental_m_central_binomial.ITEM,
    pairing_row_sums.ITEM,
]

_BY_ID = {item.id: item for item in ITEMS}


def get(item_id: str) -> Hypothesis | Exploration:
    try:
        return _BY_ID[item_id]
    except KeyError as exc:
        known = ", ".join(sorted(_BY_ID))
        raise KeyError(f"unknown id {item_id!r}; known: {known}") from exc


def hypotheses() -> list[Hypothesis]:
    return [item for item in ITEMS if isinstance(item, Hypothesis)]


def explorations() -> list[Exploration]:
    return [item for item in ITEMS if isinstance(item, Exploration)]
