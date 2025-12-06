# pairing_helpers.py
import os
import csv
from nc_polynomial import NCPolynomial

# ------------------------------
# Output utilities
# ------------------------------

def write_pairing_csv(filename, words):
    """Write a CSV pairing matrix for the given list of Word objects."""
    header = [""] + [repr(w) for w in words]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for v in words:
            row = [repr(v)]
            pv = NCPolynomial.P(v)
            for w in words:
                row.append(pv.get_coefficient(w))
            writer.writerow(row)
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
