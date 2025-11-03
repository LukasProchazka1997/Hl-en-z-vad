import streamlit as st
import csv
import os

# --- Nastavení ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv",
    "Jména": "jmena.csv"
}

MANAGER_PASSWORD = "tajneheslo"  # změňte podle potřeby

# --- Pomocné funkce ---
def nacti_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_csv(file_path, data):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow([item])

def manager_app():
    if "manager_auth" not in st.session_state:
        st.session_state.manager_auth = False

    # --- Login ---
    if not st.session_state.manager_auth:
        login_container = st.empty()
        with login_container:
            heslo = st.text_input("Zadejte heslo pro Managera", type="password")
            if st.button("Potvrdit"):
                if heslo == MANAGER_PASSWORD:
                    st.session_state.manager_auth = True
                    st.success("Přihlášení úspěšné!")
                    login_container.empty()  # skryje login form
                else:
                    st.error("Špatné heslo")
        return  # dokud není přihlášeno, nepokračujeme

    # --- Zobrazení pro správu CSV ---
    st.write("### Správa položek")

    for service, file_path in CSV_FILES.items():
        st.write(f"#### {service}")

        data = nacti_csv(file_path)
        upravene = data.copy()

        # Posouvání položek
        for i, item in enumerate(data):
            cols = st.columns([0.7, 0.15, 0.15])
            with cols[0]:
                st.text(item)
            with cols[1]:
                if st.button("↑", key=f"{service}_up_{i}") and i > 0:
                    upravene[i], upravene[i-1] = upravene[i-1], upravene[i]
            with cols[2]:
                if st.button("↓", key=f"{service}_down_{i}") and i < len(upravene) - 1:
                    upravene[i], upravene[i+1] = upravene[i+1], upravene[i]

        # Přidání nové položky
        nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
        if st.button("Uložit změny", key=f"{service}_save"):
            if nova.strip():
                upravene.append(nova.strip())
            uloz_csv(file_path, upravene)
            st.success(f"Položky pro {service} byly uloženy.")
            st.experimental_rerun = lambda: None  # dummy, aby kód fungoval v starších verzích
