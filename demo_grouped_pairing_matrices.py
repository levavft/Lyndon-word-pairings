# demo_grouped_pairing_matrices.py
import os
from pairing_helpers import PairingMatrix, write_pairing_latex, ensure_dir
from datetime import datetime
from word import Word

def main(n=5, outdir="pairings_n=5", repeat_lower=False):
    now = datetime.now()
    ensure_dir(outdir)
    groups = Word.grouped_lyndon_words(n)

    typst_output = ""

    for sig, words in groups.items():
        if not repeat_lower and len(min(words)) < n:
            continue
        base = f"group_{sig}"
        csvfile = os.path.join(outdir, base + ".csv")
        # texfile = os.path.join(outdir, base + ".tex")

        # caption = f"Pairing matrix for Lyndon words with signature {sig} (alphabet {alphabet})"
        matrix = PairingMatrix(words)
        matrix.write_csv(csvfile)
        # typst_output += f"=== The block of the permutation class ${{{min(words).to_typst()[1:-1]}}}$ \n {matrix.to_typst()}\n"
        # write_pairing_latex(texfile, words, caption)

    print(f"✅ Generated {len(groups)} groups in '{outdir}/'")
    print(datetime.now() - now)
    print(typst_output)

if __name__ == "__main__":
    main(repeat_lower=True)
