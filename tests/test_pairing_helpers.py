"""Unit tests for PairingMatrix CSV / Typst / LaTeX serializers."""

from pathlib import Path

from word import Word
from pairing_helpers import PairingMatrix


def _small_matrix():
    # Length-1 and length-2 Lyndon words: P(a)=a, P(ab)=ab-ba
    return PairingMatrix([Word("a"), Word("ab")])


def test_to_csv_rows_shape_and_label():
    pm = _small_matrix()
    rows = pm.to_csv_rows()
    assert rows[0] == ["", "a", "ab"]
    assert rows[1][0] == "a"
    assert rows[2][0] == "ab"
    assert len(rows) == 3
    assert all(len(r) == 3 for r in rows)

    labeled = pm.to_csv_rows(label=True)
    assert labeled[0][0] == "<v, w>"
    assert labeled[1:] == rows[1:]


def test_to_csv_matches_rows():
    pm = _small_matrix()
    text = pm.to_csv()
    assert text.startswith(",a,ab\n")
    assert "a," in text
    # csv.writer quotes the corner label (contains comma / spaces)
    assert pm.to_csv(label=True).startswith('"<v, w>",a,ab\n')


def test_to_typst_contains_table_and_words():
    pm = _small_matrix()
    typ = pm.to_typst()
    assert "#table(" in typ
    assert "columns: 3" in typ
    assert Word("a").to_typst() in typ
    assert Word("ab").to_typst() in typ
    assert "$chevron.l v, w chevron.r$" in typ
    for row in pm.matrix:
        for c in row:
            assert f"${c}$" in typ


def test_to_latex_contains_booktabs_and_coeffs():
    pm = _small_matrix()
    tex = pm.to_latex(caption="Test pairing")
    assert "\\begin{tabular}{lrr}" in tex
    assert "\\toprule" in tex
    assert "\\midrule" in tex
    assert "\\bottomrule" in tex
    assert "\\caption{Test pairing}" in tex
    assert "$a$" in tex and "$ab$" in tex
    for row in pm.matrix:
        for c in row:
            assert str(c) in tex


def test_write_roundtrips(tmp_path: Path):
    pm = _small_matrix()

    csv_path = tmp_path / "m.csv"
    pm.write_csv(csv_path)
    assert csv_path.read_text(encoding="utf-8") == pm.to_csv()

    csv_labeled = tmp_path / "m_label.csv"
    pm.write_csv(csv_labeled, label=True)
    assert csv_labeled.read_text(encoding="utf-8") == pm.to_csv(label=True)

    typ_path = tmp_path / "m.typ"
    pm.write_typst(typ_path)
    assert typ_path.read_text(encoding="utf-8") == pm.to_typst()

    tex_path = tmp_path / "m.tex"
    pm.write_latex(tex_path, caption="Round trip")
    assert tex_path.read_text(encoding="utf-8") == pm.to_latex(caption="Round trip")
