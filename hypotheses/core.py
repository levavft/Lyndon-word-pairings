"""Shared types for hypotheses and explorations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Status(Enum):
    """Status of a checked conjecture."""

    UNCHECKED = "unchecked"
    HOLDS_UP_TO = "holds_up_to"
    REFUTED = "refuted"


@dataclass(frozen=True)
class MathStatement:
    """Mathematical description of a conjecture."""

    latex: str
    prose: str = ""


@dataclass(frozen=True)
class HypothesisResult:
    """Checked-in or live result of a hypothesis check."""

    status: Status
    checked_up_to: dict[str, Any] = field(default_factory=dict)
    counterexamples: tuple[Any, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class ExplorationResult:
    """Checked-in or live result of an exploration run."""

    observations: dict[str, Any] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass(frozen=True)
class Hypothesis:
    """A conjecture with a mathematical statement, checker, and stored result."""

    id: str
    name: str
    statement: MathStatement
    check: Callable[..., HypothesisResult]
    result: HypothesisResult


@dataclass(frozen=True)
class Exploration:
    """An open-ended probe with a goal description, runner, and stored result."""

    id: str
    name: str
    description: str
    run: Callable[..., ExplorationResult]
    result: ExplorationResult
    goal_latex: str = ""
