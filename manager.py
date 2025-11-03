import streamlit as st
import os
import json

# --- Nastavení ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv",
    "Jména": "jmena.csv"
}
PASSWORD = "1234"

def nacti_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def uloz_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def manager_app():
    st.subheader("Manager – přístup vyžaduje heslo")
    heslo = st.text_input("Zadejte heslo", type="password")
    if heslo != PASSWORD:
        st.warning("Špatné heslo nebo nezadáno.")
        return

    st.success("Přístup povolen!")

    # --- Vyber služby ---
    service = st.selectbox("Vyber službu", list(CSV_FILES.keys()))

    file_path = CSV_FILES[service]

    # --- Načtení dat ---
    data = nacti_json(file_path)

    st.markdown("### Položky (abecedně seřazeno)")
    data.sort()
    
    # --- Zobrazení a editace položek ---
    upravene = data.copy()
    for i, item in enumerate(data):
        cols = st.columns([0.7, 0.1, 0.1])
        with cols[0]:
            upravene[i] = st.text_input(f"Položka {i+1}", value=item, key=f"{service}_{i}")
        with cols[1]:
            if st.button("↑", key=f"{service}_up_{i}") and i > 0:
                upravene[i-1], upravene[i] = upravene[i], upravene[i-1]
        with cols[2]:
            if st.button("↓", key=f"{service}_down_{i}") and i < len(upravene)-1:
                upravene[i+1], upravene[i] = upravene[i], upravene[i+1]

    st.markdown("---")
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
    if st.button("Uložit změny"):
        if nova.strip():
            upravene.append(nova.strip())
        upravene = sorted(upravene)  # abecední řazení
        uloz_json(file_path, upravene)
        st.success(f"Položky pro {service} byly uloženy.")
        st.experimental_rerun()  # refresh stránky
