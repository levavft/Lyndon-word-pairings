# pairing_helpers.py
import os
import csv
from nc_polynomial import NCPolynomial

# ------------------------------
# Output utilities
# ------------------------------

class PairingMatrix:
    def __init__(self, words):
        self.words = words
        self.matrix = self._compute_matrix()

    def _compute_matrix(self):
        rows = []
        for v in self.words:
            row = []
            pv = NCPolynomial.P(v)
            for w in self.words:
                row.append(pv.get_coefficient(w))
            rows.append(row)
        return rows

    def write_csv(self, filename, cutify = False):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            string = "<v, w>" if cutify else ""
            writer.writerow([string] + [repr(w) for w in self.words])
            for v, row in zip(self.words, self.matrix):
                writer.writerow([repr(v)] + row)
        print(f"✅ CSV written to {filename}")


def write_pairing_latex(filename, words, caption=None):
    """Write a LaTeX table mirroring the pairing matrix."""
    caption = caption or "Pairing matrix for Lyndon words"
    with open(filename, "w") as f:
        f.write("\\begin{table}[h!]\n\\centering\n")
        f.write("\\begin{tabular}{l" + "r" * len(words) + "}\n")
        f.write("\\toprule\n")
        header = " & " + " & ".join(f"${repr(w)}$" for w in words) + " \\\\\n"
        f.write(header)
        f.write("\\midrule\n")
        for v in words:
            row = [f"${repr(v)}$"]
            pv = NCPolynomial.P(v)
            for w in words:
                row.append(str(pv.get_coefficient(w)))
            f.write(" & ".join(row) + " \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n")
        f.write(f"\\caption{{{{{caption}}}}}\n\\end{{table}}\n")
    print(f"✅ LaTeX table written to {filename}")


def ensure_dir(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)
