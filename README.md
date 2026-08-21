# Lyndon word pairings

Tools for Lyndon words, pairing matrices, and noncommutative polynomials.

## Install

From the repository root, create and activate a virtual environment, then install the project in editable mode (with test dependencies):

```bash
python -m venv .venv
```

Activate the venv:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

```bash
pip install -e ".[dev]"
```

In PyCharm, set the project interpreter to this same `.venv` so imports resolve after the editable install.

## Demo: grouped pairing matrices

[`demo.py`](demo.py) writes a pairing matrix for each packed Lyndon-word signature
group (words with the same multiset of letters). Entry `(v, w)` is the coefficient
of `w` in `P(v)`.

From the repository root, with the venv activated:

```bash
python demo.py
```

Defaults: `--n 4`, packed words, output directory `pairings_n=4/`, and all three
formats (`csv`, `typst`, `latex`). Console output looks like:

```text
Wrote 36 file(s) for 12 group(s) (n=4, packed=True) to pairings_n=4/
```

Useful flags:

```bash
# Smaller run: CSV only, n=3
python demo.py --n 3 --formats csv --outdir pairings_n=3

# Only groups whose shortest word has length exactly n
python demo.py --n 4 --only-length-n --formats csv,latex

# Unpacked Lyndon words
python demo.py --n 3 --no-packed --formats csv
```

Each group becomes `group_<signature>.{csv,typ,tex}`. Examples for `--n 3 --formats csv`:

`group_abc.csv` (2×2 block for `{abc, acb}`):

```csv
,abc,acb
abc,1,-1
acb,0,1
```

`group_abb.csv`:

```csv
,abb
abb,1
```

Typst fragment for the same `ab` group (`--n 2 --formats typst`):

```typst
#table(
    columns: 2,
    table.header([$chevron.l v, w chevron.r$], $(a b)$),
	$(a b)$, $1$,
)
```

LaTeX for that group (needs `\usepackage{booktabs}` in the document):

```latex
\begin{table}[h!]
\centering
\begin{tabular}{lr}
\toprule
 & $ab$ \\
\midrule
$ab$ & 1 \\
\bottomrule
\end{tabular}
\caption{Pairing matrix for Lyndon words with signature ab}
\end{table}
```

## Exploring hypotheses

Research conjectures and exploratory probes live under [`hypotheses/`](hypotheses/)
(not part of the test suite). Each item stores a mathematical statement (or goal)
and a checked-in Python `RESULT`. The thin CLI is [`explore_hypotheses.py`](explore_hypotheses.py):

```bash
python explore_hypotheses.py --list
python explore_hypotheses.py --check fundamental_m_central_binomial --n 6
python explore_hypotheses.py --check-all --n 5
python explore_hypotheses.py --explore max_abs_p_coefficient --n 5
```

## Tests

From the repository root, with the venv activated:

```bash
pytest
```

Or:

```bash
python -m pytest
```
