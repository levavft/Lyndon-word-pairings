"""Generate grouped pairing matrices (CSV / Typst / LaTeX) for packed Lyndon words."""

from __future__ import annotations

import argparse
import os

from pairing_helpers import PairingMatrix, ensure_dir
from word import Word

FORMAT_EXT = {
    "csv": ".csv",
    "typst": ".typ",
    "latex": ".tex",
}


def parse_formats(s: str) -> list[str]:
    formats = [part.strip().lower() for part in s.split(",") if part.strip()]
    unknown = [f for f in formats if f not in FORMAT_EXT]
    if unknown:
        raise argparse.ArgumentTypeError(
            f"unknown format(s) {unknown}; choose from {sorted(FORMAT_EXT)}"
        )
    if not formats:
        raise argparse.ArgumentTypeError("at least one format is required")
    return formats


def main(
    n: int = 4,
    outdir: str | None = None,
    packed: bool = True,
    only_length_n: bool = False,
    formats: list[str] | None = None,
) -> None:
    if outdir is None:
        outdir = f"pairings_n={n}"
    if formats is None:
        formats = ["csv", "typst", "latex"]

    ensure_dir(outdir)
    groups = Word.grouped_lyndon_words(n, packed=packed)
    written = 0
    used_groups = 0

    for sig, words in groups.items():
        if only_length_n and len(min(words)) < n:
            continue
        used_groups += 1
        base = os.path.join(outdir, f"group_{sig}")
        pm = PairingMatrix(words)
        caption = f"Pairing matrix for Lyndon words with signature {sig}"

        if "csv" in formats:
            pm.write_csv(base + FORMAT_EXT["csv"])
            written += 1
        if "typst" in formats:
            pm.write_typst(base + FORMAT_EXT["typst"])
            written += 1
        if "latex" in formats:
            pm.write_latex(base + FORMAT_EXT["latex"], caption=caption)
            written += 1

    print(
        f"Wrote {written} file(s) for {used_groups} group(s) "
        f"(n={n}, packed={packed}) to {outdir}/"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Write grouped Lyndon pairing matrices as CSV, Typst, and/or LaTeX."
    )
    p.add_argument("--n", type=int, default=4, help="alphabet/length bound (default: 4)")
    p.add_argument(
        "--outdir",
        default=None,
        help="output directory (default: pairings_n=<n>)",
    )
    p.add_argument(
        "--packed",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="use packed Lyndon words (default: true)",
    )
    p.add_argument(
        "--only-length-n",
        action="store_true",
        help="skip groups whose shortest word has length < n",
    )
    p.add_argument(
        "--formats",
        type=parse_formats,
        default=["csv", "typst", "latex"],
        help="comma-separated: csv, typst, latex (default: all)",
    )
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    main(
        n=args.n,
        outdir=args.outdir,
        packed=args.packed,
        only_length_n=args.only_length_n,
        formats=args.formats,
    )
