import os
import csv
import pytest
from pairing_helpers import grouped_lyndon_words, write_pairing_csv

REFERENCE_DIR = "reference_pairings"   # hand-computed CSVs
OUT_DIR = "pairings"


# @pytest.fixture(scope="module")
# def setup_generated_packed_groups(tmp_path_factory):
#     """Generate packed grouped CSVs for testing structure and content."""
#     outdir = tmp_path_factory.mktemp("groups")
#     groups = grouped_lyndon_words(n=N, packed=True)
#     for sig, words in groups.items():
#         csvfile = os.path.join(outdir, f"packed_group_{sig}.csv")
#         write_pairing_csv(csvfile, words)
#     return outdir


# --------------------------
# Utility functions
# --------------------------

def load_csv(path):
    """Load CSV as list of lists, stripped of whitespace."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return [[cell.strip() for cell in row] for row in reader if any(cell.strip() for cell in row)]


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


def compare_csv_content(file_a, file_b):
    """Compare two CSV matrices structurally and numerically."""
    mat_a = normalize_matrix(load_csv(file_a))
    mat_b = normalize_matrix(load_csv(file_b))

    # Basic shape check
    assert len(mat_a) == len(mat_b), f"Row count differs: {file_a} vs {file_b}"
    for i, (ra, rb) in enumerate(zip(mat_a, mat_b)):
        assert len(ra) == len(rb), f"Column count mismatch at row {i} in {file_a}"

    # Full content equality
    for i, (ra, rb) in enumerate(zip(mat_a, mat_b)):
        for j, (ca, cb) in enumerate(zip(ra, rb)):
            if ca != cb:
                pytest.fail(f"Value mismatch at {file_a} row {i}, col {j}: {ca} ≠ {cb}")


# --------------------------
# Content comparison tests
# --------------------------

def test_reference_dir_exists():
    """Ensure the hand-computed reference directory exists."""
    if not os.path.isdir(REFERENCE_DIR):
        pytest.skip(f"Reference directory '{REFERENCE_DIR}' not found; skipping content comparison.")
    assert any(f.endswith(".csv") for f in os.listdir(REFERENCE_DIR)), \
        f"No CSV files found in '{REFERENCE_DIR}'"


def test_generated_files_match_reference_structure():
    """Check that generated packed CSVs match the reference file list."""
    outdir = OUT_DIR
    generated = {f for f in os.listdir(outdir) if f.endswith(".csv")}

    if not os.path.exists(REFERENCE_DIR):
        pytest.skip(f"Reference directory '{REFERENCE_DIR}' not found.")
    reference = {f for f in os.listdir(REFERENCE_DIR) if f.endswith(".csv")}

    missing = reference - generated
    extra = generated - reference

    if missing:
        pytest.fail(f"Missing generated CSVs: {missing}")
    if extra:
        pytest.fail(f"Unexpected extra generated CSVs: {extra}")

    print(f"✅ File list matches: {len(reference)} CSV files.")


def test_generated_csv_content_matches_reference():
    """Compare each generated CSV against its reference counterpart."""
    outdir = OUT_DIR

    if not os.path.exists(REFERENCE_DIR):
        pytest.skip(f"Reference directory '{REFERENCE_DIR}' not found; skipping content comparison.")

    for filename in os.listdir(REFERENCE_DIR):
        if not filename.endswith(".csv"):
            continue
        ref_path = os.path.join(REFERENCE_DIR, filename)
        gen_path = os.path.join(outdir, filename)
        assert os.path.exists(gen_path), f"Missing generated file {filename}"
        compare_csv_content(ref_path, gen_path)
        print(f"✅ {filename}: content matches reference.")


def get_maximal_value_of_dir(path):
    M = 0
    for filename in os.listdir(path):
        lst = normalize_matrix(load_csv(path + "\\" + filename), False)
        m = max(max(abs(t) for t in l) for l in lst if len(l) > 0)
        if m > M:
            M = m
    return M