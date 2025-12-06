# pairing_helpers.py
import os
import csv
from collections import defaultdict
from word import Word
from nc_polynomial import NCPolynomial

# ------------------------------

def lyndon_words_upto(n, packed=True):
    return _lyndon_words_upto_duval(n, packed)


def _lyndon_words_upto(n, packed=True):
    """Return all Lyndon words of length ≤ n (optionally only packed ones)."""
    # TODO - use duval's algorithm instead...
    return [w for w in all_words_upto_length(n, packed) if w.is_lyndon()]


def _lyndon_words_upto_duval(n, packed=True):
    """Return all Lyndon words of length ≤ n in the alphabet of size n (optionally only packed ones)."""
    words = []
    w = [-1]  # set up for first increment
    while w:
        w[-1] += 1  # increment the last non-z symbol
        candidate = Word(tuple(w))
        if not packed or candidate == candidate.packed():
            words.append(candidate)
        m = len(w)
        while len(w) < n:  # repeat word to fill exactly n syms
            w.append(w[-m])
        while w and w[-1] == n - 1:  # delete trailing z's
            w.pop()
    return words


def word_signature(w: Word) -> str:
    """Signature for grouping by multiset of letters."""
    return "".join(sorted(repr(w)))


def grouped_lyndon_words(n, packed=True):
    """Group Lyndon words by permutation equivalence."""
    groups = defaultdict(list)
    for w in lyndon_words_upto(n, packed):
        groups[word_signature(w)].append(w)
    return dict(groups)


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
