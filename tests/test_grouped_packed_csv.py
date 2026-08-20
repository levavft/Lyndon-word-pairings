"""Live PairingMatrix output vs thesis-verified reference CSVs (n=4, packed)."""

import os
import csv
import pytest

from word import Word
from pairing_helpers import PairingMatrix

REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "reference_pairings")
N = 4


def load_csv(path):
    """Load CSV as list of lists, stripped of whitespace."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return [
            [cell.strip() for cell in row]
            for row in reader
            if any(cell.strip() for cell in row)
        ]


def normalize_matrix(matrix, inc_non_int=True):
    """Convert all numeric-looking strings to ints for reliable comparison."""
    norm = []
    for row in matrix:
        norm_row = []
        for val in row:
            try:
                norm_row.append(int(val))
            except ValueError:
                if inc_non_int:
                    norm_row.append(val)
        norm.append(norm_row)
    return norm


def matrix_as_csv_rows(words, matrix):
    """Same layout as PairingMatrix.write_csv (cutify=False)."""
    header = [""] + [repr(w) for w in words]
    body = [[repr(v)] + list(row) for v, row in zip(words, matrix)]
    return [header] + body


@pytest.fixture(scope="module")
def live_packed_groups():
    """Generate packed grouped pairing matrices from current production code."""
    groups = Word.grouped_lyndon_words(n=N, packed=True)
    out = {}
    for sig, words in groups.items():
        pm = PairingMatrix(words)
        out[sig] = (words, pm.matrix)
    return out


def test_reference_dir_exists():
    """Ensure the thesis-verified reference directory exists and has CSVs."""
    assert os.path.isdir(REFERENCE_DIR), (
        f"Reference directory '{REFERENCE_DIR}' not found"
    )
    assert any(f.endswith(".csv") for f in os.listdir(REFERENCE_DIR)), (
        f"No CSV files found in '{REFERENCE_DIR}'"
    )


def test_live_files_match_reference_structure(live_packed_groups):
    """Live group signatures must match the reference CSV file list."""
    generated = {f"group_{sig}.csv" for sig in live_packed_groups}
    reference = {f for f in os.listdir(REFERENCE_DIR) if f.endswith(".csv")}

    missing = reference - generated
    extra = generated - reference
    if missing:
        pytest.fail(f"Missing live groups for reference CSVs: {missing}")
    if extra:
        pytest.fail(f"Unexpected extra live groups: {extra}")


def test_live_csv_content_matches_reference(live_packed_groups):
    """Compare each live PairingMatrix against its thesis-verified reference."""
    for filename in os.listdir(REFERENCE_DIR):
        if not filename.endswith(".csv"):
            continue
        assert filename.startswith("group_") and filename.endswith(".csv")
        sig = filename[len("group_") : -len(".csv")]
        assert sig in live_packed_groups, f"No live group for {filename}"

        words, matrix = live_packed_groups[sig]
        live_rows = normalize_matrix(matrix_as_csv_rows(words, matrix))
        ref_rows = normalize_matrix(
            load_csv(os.path.join(REFERENCE_DIR, filename))
        )

        assert len(live_rows) == len(ref_rows), (
            f"Row count differs for {filename}: live {len(live_rows)} vs "
            f"ref {len(ref_rows)}"
        )
        for i, (live_row, ref_row) in enumerate(zip(live_rows, ref_rows)):
            assert len(live_row) == len(ref_row), (
                f"Column count mismatch at row {i} in {filename}"
            )
            for j, (live_val, ref_val) in enumerate(zip(live_row, ref_row)):
                if live_val != ref_val:
                    pytest.fail(
                        f"Value mismatch at {filename} row {i}, col {j}: "
                        f"live {live_val} ≠ ref {ref_val}"
                    )
