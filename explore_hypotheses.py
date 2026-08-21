"""CLI runner for the hypotheses / explorations catalog.

Not part of the test suite. Definitions and checked-in results live under
``hypotheses/``.
"""

from __future__ import annotations

import argparse
import inspect
import pprint
import sys

from hypotheses.core import Exploration, Hypothesis
from hypotheses.registry import explorations, get, hypotheses


def _print_hypothesis(item: Hypothesis, *, live) -> None:
    print(f"[{item.id}] {item.name}")
    print(f"  latex: {item.statement.latex}")
    if item.statement.prose:
        print(f"  prose: {item.statement.prose}")
    print("  stored result:")
    pprint.pprint(item.result, indent=2)
    if live is not None:
        print("  live check:")
        pprint.pprint(live, indent=2)


def _print_exploration(item: Exploration, *, live) -> None:
    print(f"[{item.id}] {item.name}")
    print(f"  description: {item.description}")
    if item.goal_latex:
        print(f"  goal_latex: {item.goal_latex}")
    print("  stored result:")
    pprint.pprint(item.result, indent=2)
    if live is not None:
        print("  live run:")
        pprint.pprint(live, indent=2)


def _call_with_n(fn, n: int):
    """Invoke check/run, mapping --n to the function's length-bound parameter."""
    params = inspect.signature(fn).parameters
    if "n_max" in params:
        return fn(n_max=n)
    if "n" in params:
        return fn(n=n)
    return fn()


def cmd_list() -> None:
    print("Hypotheses:")
    for h in hypotheses():
        print(f"  {h.id:40} {h.result.status.value:12} {h.name}")
    print("Explorations:")
    for e in explorations():
        print(f"  {e.id:40} {'explore':12} {e.name}")


def cmd_check(item_id: str | None, n: int, check_all: bool) -> None:
    targets: list[Hypothesis]
    if check_all:
        targets = hypotheses()
    else:
        assert item_id is not None
        item = get(item_id)
        if not isinstance(item, Hypothesis):
            raise SystemExit(f"{item_id!r} is an exploration; use --explore")
        targets = [item]

    for h in targets:
        live = _call_with_n(h.check, n)
        _print_hypothesis(h, live=live)
        print()


def cmd_explore(item_id: str, n: int) -> None:
    item = get(item_id)
    if not isinstance(item, Exploration):
        raise SystemExit(f"{item_id!r} is a hypothesis; use --check")
    live = _call_with_n(item.run, n)
    _print_exploration(item, live=live)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="List and run research hypotheses / explorations."
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true", help="list catalog entries")
    g.add_argument("--check", metavar="ID", help="run one hypothesis checker")
    g.add_argument("--check-all", action="store_true", help="run all hypothesis checkers")
    g.add_argument("--explore", metavar="ID", help="run one exploration")
    p.add_argument(
        "--n",
        type=int,
        default=5,
        help="length / depth bound passed to check/run (default: 5)",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.list:
        cmd_list()
    elif args.check_all or args.check:
        cmd_check(args.check, args.n, args.check_all)
    elif args.explore:
        cmd_explore(args.explore, args.n)
    else:  # pragma: no cover
        build_parser().print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
