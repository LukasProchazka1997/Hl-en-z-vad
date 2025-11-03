# manager.py
import streamlit as st
import csv
import os

# --- Nastavení CSV ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv",
    "Jména": "jmena.csv"
}

# --- Heslo pro vstup ---
MANAGER_PASSWORD = "1234"

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

# --- Funkce Manager ---
def manager_app():
    st.subheader("Manager CSV položek")

    # --- Heslo ---
    if "authorized" not in st.session_state:
        st.session_state.authorized = False

    if not st.session_state.authorized:
        heslo = st.text_input("Zadejte heslo pro vstup do managera", type="password")
        if st.button("Přihlásit"):
            if heslo == MANAGER_PASSWORD:
                st.session_state.authorized = True
                st.experimental_rerun()
            else:
                st.error("Špatné heslo")
        return  # neukazuje obsah, dokud není heslo

    # --- Výběr CSV ---
    service = st.selectbox("Vyber soubor", list(CSV_FILES.keys()))
    file_path = CSV_FILES[service]

    data = nacti_csv(file_path)

    # --- Zobrazení položek a úpravy ---
    st.markdown("### Položky")
    upravene = data.copy()
    vybrany_index = st.selectbox("Vyber položku pro úpravu / posun", range(len(data)), format_func=lambda x: data[x] if x < len(data) else "")

    nova = st.text_input("Přidat novou položku")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Nahoru") and vybrany_index > 0:
            upravene[vybrany_index-1], upravene[vybrany_index] = upravene[vybrany_index], upravene[vybrany_index-1]
            uloz_csv(file_path, upravene)
            st.experimental_rerun()
    with col2:
        if st.button("Dolů") and vybrany_index < len(upravene)-1:
            upravene[vybrany_index+1], upravene[vybrany_index] = upravene[vybrany_index], upravene[vybrany_index+1]
            uloz_csv(file_path, upravene)
            st.experimental_rerun()
    with col3:
        if st.button("Smazat"):
            upravene.pop(vybrany_index)
            uloz_csv(file_path, upravene)
            st.experimental_rerun()

    if st.button("Uložit změny"):
        if nova.strip():
            upravene.append(nova.strip())
        uloz_csv(file_path, upravene)
        st.success("Změny uloženy")
        st.experimental_rerun()

    st.markdown("### Aktuální seznam položek")
    for i, item in enumerate(upravene):
        st.text(f"{i+1}. {item}")
