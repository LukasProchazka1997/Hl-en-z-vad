# manager.py
import streamlit as st
import csv
import os
from streamlit_sortable import sortable_list  # pip install streamlit-sortable

# --- Nastavení ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}
PASSWORD = "tajneheslo"  # změň na svoje

# --- Pomocné funkce ---
def nacti_csv(soubor):
    if not os.path.exists(soubor):
        with open(soubor, "w", newline="", encoding="utf-8") as f:
            pass
        return []
    with open(soubor, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_csv(soubor, data):
    data = sorted(data)  # abecední řazení
    with open(soubor, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow([item])

# --- Hlavní aplikace ---
def manager_app():
    st.subheader("Manager – Správa položek")
    
    # --- Heslo ---
    if "authorized" not in st.session_state:
        st.session_state.authorized = False
    
    if not st.session_state.authorized:
        pw = st.text_input("Zadejte heslo", type="password")
        if st.button("Potvrdit"):
            if pw == PASSWORD:
                st.session_state.authorized = True
                st.experimental_rerun()
            else:
                st.error("Špatné heslo")
        return

    # --- Výběr služby ---
    service = st.selectbox("Vyber službu", list(CSV_FILES.keys()))
    file_path = CSV_FILES[service]
    data = nacti_csv(file_path)

    # --- Drag & drop seznam ---
    st.write("Přetáhněte položky pro změnu pořadí (automaticky abecedně při uložení)")
    new_order = sortable_list(data, key=f"{service}_sortable")

    # --- Přidání nové položky ---
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")

    if st.button("Uložit změny"):
        upravene = new_order.copy()
        if nova.strip():
            upravene.append(nova.strip())
        uloz_csv(file_path, upravene)
        st.success(f"Položky pro {service} byly uloženy a seřazeny abecedně.")
        st.experimental_rerun()
