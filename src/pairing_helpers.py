"""Pairing matrices for lists of words, with CSV / Typst / LaTeX export.

The entry at row ``v`` and column ``w`` is the pairing
``⟨v, w⟩ =`` coefficient of ``w`` in ``P(v)``, where ``P`` is
``NCPolynomial.P``.

LaTeX output uses ``booktabs`` (``\\toprule`` / ``\\midrule`` /
``\\bottomrule``); include ``\\usepackage{booktabs}`` in the document.
"""

from __future__ import annotations

import csv
import io
import os

from nc_polynomial import NCPolynomial


class PairingMatrix:
    """Square pairing matrix over an ordered list of words."""

    def __init__(self, words):
        self.words = list(words)
        self.matrix = self._compute_matrix()

    def _compute_matrix(self):
        rows = []
        for v in self.words:
            pv = NCPolynomial.P(v)
            rows.append([pv.get_coefficient(w) for w in self.words])
        return rows

    # ---------- String / structured forms ----------

    def to_csv_rows(self, *, label: bool = False) -> list[list]:
        """Return ``[[corner, w...], [v, coeffs...], ...]``.

        If ``label`` is true, the corner cell is ``"<v, w>"``; otherwise empty.
        """
        corner = "<v, w>" if label else ""
        header = [corner] + [repr(w) for w in self.words]
        body = [[repr(v)] + list(row) for v, row in zip(self.words, self.matrix)]
        return [header] + body

    def to_csv(self, *, label: bool = False) -> str:
        """CSV text matching ``write_csv`` (including trailing newline)."""
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        for row in self.to_csv_rows(label=label):
            writer.writerow(row)
        return buf.getvalue()

    def to_typst(self) -> str:
        """Typst ``#table(...)`` fragment for this pairing matrix."""
        tabs = "\t"
        internal = ""
        for v, row in zip(self.words, self.matrix):
            coeffs = ", ".join(f"${el}$" for el in row)
            internal += f"{tabs}{v.to_typst()}, {coeffs},\n"
        header_words = ", ".join(w.to_typst() for w in self.words)
        return (
            f"\n#table(\n"
            f"    columns: {len(self.words) + 1}, \n"
            f"    table.header([$chevron.l v, w chevron.r$], {header_words}),\n"
            f"{internal})    \n"
        )

    def to_latex(self, *, caption: str | None = None) -> str:
        """LaTeX ``table``+``tabular`` (needs ``booktabs`` in the preamble)."""
        caption = caption or "Pairing matrix for Lyndon words"
        n = len(self.words)
        lines = [
            "\\begin{table}[h!]",
            "\\centering",
            "\\begin{tabular}{l" + "r" * n + "}",
            "\\toprule",
            " & " + " & ".join(f"${repr(w)}$" for w in self.words) + " \\\\",
            "\\midrule",
        ]
        for v, row in zip(self.words, self.matrix):
            cells = [f"${repr(v)}$"] + [str(c) for c in row]
            lines.append(" & ".join(cells) + " \\\\")
        lines.extend(
            [
                "\\bottomrule",
                "\\end{tabular}",
                f"\\caption{{{caption}}}",
                "\\end{table}",
                "",
            ]
        )
        return "\n".join(lines)

    # ---------- Writers (no print side effects) ----------

    def write_csv(self, path, *, label: bool = False) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(self.to_csv(label=label))

    def write_typst(self, path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_typst())

    def write_latex(self, path, *, caption: str | None = None) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_latex(caption=caption))


def ensure_dir(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)
