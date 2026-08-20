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

## Tests

From the repository root, with the venv activated:

```bash
pytest
```

Or:

```bash
python -m pytest
```
