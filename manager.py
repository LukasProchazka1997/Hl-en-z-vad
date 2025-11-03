# manager.py
import streamlit as st
import csv
import json
import os

CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}

def nacti_csv(soubor):
    if not os.path.exists(soubor):
        return []
    with open(soubor, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_csv(soubor, data):
    with open(soubor, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in sorted(data, key=lambda x: x.lower()):  # abecední řazení
            writer.writerow([item])

def manager_app():
    st.subheader("Manager CSV položek (jen úprava, řazeno abecedně)")
    
    # výběr souboru
    service = st.selectbox("Vyber službu", list(CSV_FILES.keys()))
    file_path = CSV_FILES[service]

    data = nacti_csv(file_path)

    # zobrazení všech položek v textových polích
    upravene = []
    for i, item in enumerate(data):
        upravene.append(st.text_input(f"Položka {i+1}", value=item, key=f"{service}_{i}"))

    # přidání nové položky
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
    
    if st.button("Uložit změny"):
        if nova.strip():
            upravene.append(nova.strip())
        uloz_csv(file_path, upravene)
        st.success(f"Položky pro {service} byly uloženy.")
        st.experimental_rerun()  # spustí znovu stránku a načte nové hodnoty
