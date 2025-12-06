# demo_pairing_matrix.py
from pairing_helpers import write_pairing_csv, write_pairing_latex
from word import Word

def main(n=3):
    lyndons = Word.lyndon_words_upto(n)
    write_pairing_csv(f"pairing_matrix_{n=}.csv", lyndons)
    # write_pairing_latex(f"pairing_matrix_{n=}.tex", lyndons,
    #                     caption=f"Pairing matrix for Lyndon words up to length {n}")

if __name__ == "__main__":
    main()
