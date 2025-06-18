import pandas as pd
import re
import matplotlib.pyplot as plt

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


# Alustetaan tyhjä lista, joka tallennetaan dataframeen
results = []

for text in texts:
    found_codes = re.findall(r'\b[A-Z]\d{2}(?:\.\d+)?\b', text)
    for code in found_codes:
        code_nopoint = normalize_code(code)
        match = icd10[icd10['Diagnosis Code'] == code]
        if match.empty:
            match = icd10[icd10['Diagnosis Code'] == code_nopoint]
        if not match.empty:
            description = match['Abbreviated Description'].iloc[0]
        else:
            description = '(ei löytynyt selitettä)'
        results.append({
            'Text': text.strip(),
            'Code': code,
            'Description': description
        })

# Muutetaan tulokset DataFrameksi
df = pd.DataFrame(results)
print(df.head(10))


top_codes = df['Code'].value_counts().head(10)
print("Yleisimmät koodit:\n", top_codes)



top_codes.plot(kind='bar')
plt.title("Yleisimmät löydetyt ICD-10-koodit")
plt.xlabel("ICD-10-koodi")
plt.ylabel("Esiintymät")
plt.tight_layout()
plt.savefig('output/top_icd10_codes.png')
plt.show()

