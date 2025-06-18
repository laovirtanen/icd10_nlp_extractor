import pandas as pd
import re

# Anna sarakeotsikot suoraan:
columns = [
    'Category Code',       # 0
    'Minor Code',          # 1
    'Diagnosis Code',      # 2
    'Abbreviated Description',  # 3
    'Full Description',         # 4
    'Category Title'            # 5
]

# Lue CSV ilman headeria, lisää sarakenimet
icd10 = pd.read_csv('data/icd10_codes.csv', header=None, names=columns)

# Lue sample
with open('data/sample_texts.txt', encoding='utf-8') as f:
    texts = f.readlines()

def normalize_code(code):
    """Muuntaa koodin pisteettömään muotoon (E11.9 -> E119)"""
    return code.replace('.', '')

for text in texts:
    found_codes = re.findall(r'\b[A-Z]\d{2}(?:\.\d+)?\b', text)
    print(f"Teksti: {text.strip()}")
    for code in found_codes:
        code_nopoint = normalize_code(code)
        # Yritä ensin pisteellistä, sitten pisteetöntä muotoa
        match = icd10[icd10['Diagnosis Code'] == code]
        if match.empty:
            match = icd10[icd10['Diagnosis Code'] == code_nopoint]
        if not match.empty:
            print(f"  → {code}: {match['Abbreviated Description'].iloc[0]}")
        else:
            print(f"  → {code}: (ei löytynyt selitettä)")
    print()
