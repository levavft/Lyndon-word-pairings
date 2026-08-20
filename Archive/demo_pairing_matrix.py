# demo_pairing_matrix.py
from pairing_helpers import PairingMatrix, write_pairing_latex
from word import Word

def main(n=3):
    lyndons = Word.lyndon_words_upto(n)
    PairingMatrix(lyndons).write_csv(f"pairing_matrix_{n=}.csv")
    # write_pairing_latex(f"pairing_matrix_{n=}.tex", lyndons,
    #                     caption=f"Pairing matrix for Lyndon words up to length {n}")

if __name__ == "__main__":
    main()
