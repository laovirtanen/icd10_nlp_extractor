import streamlit as st
import pandas as pd
import re

# Anna sarakeotsikot suoraan:
columns = [
    'Category Code',
    'Minor Code',
    'Diagnosis Code',
    'Abbreviated Description',
    'Full Description',
    'Category Title'
]

# Lue ICD-10-koodit
icd10 = pd.read_csv('data/icd10_codes.csv', header=None, names=columns)

def normalize_code(code):
    return code.replace('.', '')

def extract_icd10(text):
    results = []
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
            'Koodi': code,
            'Selite': description
        })
    return results

# --- STREAMLIT UI ---
st.title("ICD-10 tekstinlouhinta-demo")

text_input = st.text_area(
    "Syötä vapaateksti (esim. potilaskertomus, diagnoosilistaus tms.):",
    height=150
)

if st.button("Etsi ICD-10-koodit"):
    results = extract_icd10(text_input)
    if results:
        st.success(f"Löytyi {len(results)} koodia!")
        st.table(results)
    else:
        st.warning("Ei löytynyt yhtään ICD-10-koodia.")

st.markdown("---")
st.markdown("Demo by Lauri Virtanen | Sisältää noin 70 000 koodia, mutta ei ole kokonaan kattava listaus!")
