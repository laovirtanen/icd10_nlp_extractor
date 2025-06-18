import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import re

columns = [
    'Category Code',
    'Minor Code',
    'Diagnosis Code',
    'Abbreviated Description',
    'Full Description',
    'Category Title'
]
icd10 = pd.read_csv('data/icd10_codes.csv', header=None, names=columns)

def normalize_code(code):
    return code.replace('.', '')

def extract_icd10_codes(text):
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

def fuzzy_icd10_mapping(term, icd10_df, limit=3):
    choices = icd10_df['Abbreviated Description'].astype(str).tolist()
    matches = process.extract(
        term, choices, scorer=fuzz.token_set_ratio, limit=limit
    )
    results = []
    for match, score, idx in matches:
        if score > 70:
            row = icd10_df.iloc[idx]
            results.append({
                'Koodi': row['Diagnosis Code'],
                'Selite': match,
                'Osuma (%)': score
            })
    return results

st.title("ICD-10 tekstinlouhinta-demo")

text_input = st.text_area("Syötä teksti:")
if st.button("Etsi suorat ICD-10-koodit"):
    results = extract_icd10_codes(text_input)
    if results:
        st.success(f"Löytyi {len(results)} koodia!")
        st.table(results)
    else:
        st.warning("Ei löytynyt yhtään ICD-10-koodia.")

st.markdown("---")

free_term = st.text_input("Syötä vapaa hakutermi (englanniksi):")
if st.button("Fuzzy-haku ICD-10-sanastoon"):
    if free_term.strip():
        results = fuzzy_icd10_mapping(free_term, icd10)
        if results:
            st.success("Parhaat osumat:")
            st.table(results)
        else:
            st.warning("Ei löytynyt hyviä osumia.")
    else:
        st.info("Anna hakutermi!")
