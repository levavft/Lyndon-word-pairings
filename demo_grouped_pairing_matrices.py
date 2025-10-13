# demo_grouped_pairing_matrices.py
import os
from pairing_helpers import grouped_lyndon_words, write_pairing_csv, write_pairing_latex, ensure_dir
from datetime import datetime

def main(n=4, outdir="pairings"):
    now = datetime.now()
    ensure_dir(outdir)
    groups = grouped_lyndon_words(n)

    for sig, words in groups.items():
        base = f"group_{sig}"
        csvfile = os.path.join(outdir, base + ".csv")
        # texfile = os.path.join(outdir, base + ".tex")

        # caption = f"Pairing matrix for Lyndon words with signature {sig} (alphabet {alphabet})"
        write_pairing_csv(csvfile, words)
        # write_pairing_latex(texfile, words, caption)

    print(f"✅ Generated {len(groups)} groups in '{outdir}/'")
    print(datetime.now() - now)

if __name__ == "__main__":
    main()
