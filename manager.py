import streamlit as st
import csv
import os
from streamlit_sortable import sortable_list

# --- Nastavení ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}
PASSWORD = "1234"

# --- Pomocné funkce ---
def nacti_csv(soubor):
    if not os.path.exists(soubor):
        return []
    with open(soubor, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_csv(soubor, data):
    with open(soubor, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow([item])

# --- Manager aplikace ---
def manager_app():
    st.subheader("Správa položek (Manager)")

    # --- Heslo ---
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        heslo = st.text_input("Zadejte heslo pro přístup", type="password")
        if st.button("Potvrdit"):
            if heslo == PASSWORD:
                st.session_state["authenticated"] = True
                st.experimental_rerun()
            else:
                st.error("Špatné heslo")
        return

    # --- Vyber služby ---
    service = st.selectbox("Vyber službu", list(CSV_FILES.keys()), key="manager_service")
    file_path = CSV_FILES[service]

    # --- Načtení dat ---
    data = st.session_state.get(f"{service}_data", nacti_csv(file_path))

    st.write("**Seznam položek – přetáhni pro změnu pořadí**")
    # Drag & Drop seznam
    data = sortable_list(data, key=f"{service}_sortable")
    st.session_state[f"{service}_data"] = data

    # --- Přidání nové položky ---
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
    if st.button("Přidat položku", key=f"{service}_add"):
        if nova.strip():
            data.append(nova.strip())
            st.session_state[f"{service}_data"] = data
            st.success("Položka přidána")
            st.experimental_rerun()

    # --- Uložení změn ---
    if st.button("Uložit změny", key=f"{service}_save"):
        uloz_csv(file_path, data)
        st.success(f"Položky pro {service} byly uloženy")
