# manager.py — Streamlit Manager
import streamlit as st
import csv
import os

# Heslo pro vstup do managera
MANAGER_PASSWORD = "1234"

# Mapování služeb a jejich CSV
SERVICES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}

# --------------------
# Pomocné funkce
# --------------------
def nacti_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_csv(file_path, data):
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow([item])

# --------------------
# Hlavní funkce managera
# --------------------
def manager_app():
    st.subheader("Manager – správa položek")

    # --- Heslo ---
    if "authorized" not in st.session_state:
        st.session_state.authorized = False

    if not st.session_state.authorized:
        heslo = st.text_input("Zadejte heslo pro vstup", type="password")
        if st.button("Potvrdit"):
            if heslo == MANAGER_PASSWORD:
                st.session_state.authorized = True
                st.experimental_rerun = None  # jen aby Streamlit překreslil
            else:
                st.error("Špatné heslo.")
        return

    # --- Vyber služby ---
    service = st.selectbox("Vyber službu", list(SERVICES.keys()))
    file_path = SERVICES[service]

    # --- Načtení dat do session_state ---
    if f"{service}_data" not in st.session_state:
        st.session_state[f"{service}_data"] = nacti_csv(file_path)

    upravene = st.session_state[f"{service}_data"]

    # --- Zobrazení a výběr položky ---
    if not upravene:
        st.info("Seznam je prázdný.")
        vybrany_index = None
    else:
        vybrany_index = st.selectbox(
            "Vyber položku k úpravě",
            range(len(upravene)),
            format_func=lambda i: upravene[i]
        )

    # --- Tlačítka pro úpravy ---
    if vybrany_index is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Nahoru"):
                if vybrany_index > 0:
                    upravene[vybrany_index-1], upravene[vybrany_index] = upravene[vybrany_index], upravene[vybrany_index-1]
                    uloz_csv(file_path, upravene)
                    st.session_state[f"{service}_data"] = upravene
        with col2:
            if st.button("Dolů"):
                if vybrany_index < len(upravene)-1:
                    upravene[vybrany_index+1], upravene[vybrany_index] = upravene[vybrany_index], upravene[vybrany_index+1]
                    uloz_csv(file_path, upravene)
                    st.session_state[f"{service}_data"] = upravene
        with col3:
            if st.button("Smazat"):
                upravene.pop(vybrany_index)
                uloz_csv(file_path, upravene)
                st.session_state[f"{service}_data"] = upravene

    # --- Přidání nové položky ---
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
    if st.button("Uložit změny"):
        if nova.strip():
            upravene.append(nova.strip())
        # automatické seřazení abecedně
        upravene.sort()
        uloz_csv(file_path, upravene)
        st.session_state[f"{service}_data"] = upravene
        st.success(f"Položky pro {service} byly uloženy.")

    # --- Zobrazení seznamu ---
    st.text("Aktuální položky:")
    for i, item in enumerate(upravene):
        st.text(f"{i+1}. {item}")
