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

MANAGER_PASSWORD = "tajneheslo"  # ← sem dej svoje heslo

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

# --- Hlavní aplikace ---
def manager_app():
    st.title("📋 Manager")
    
    # --- Autentizace ---
    if "manager_auth" not in st.session_state:
        st.session_state.manager_auth = False

    if not st.session_state.manager_auth:
        st.info("Pro přístup do managera zadej heslo.")
        with st.form("login_form", clear_on_submit=True):
            heslo = st.text_input("Zadejte heslo", type="password")
            odeslat = st.form_submit_button("Přihlásit se")

            if odeslat:
                if heslo == MANAGER_PASSWORD:
                    st.session_state.manager_auth = True
                    st.success("✅ Přihlášení úspěšné!")
                    st.rerun()  # bezpečné přenačtení rozhraní
                else:
                    st.error("❌ Špatné heslo")
        return

    # --- Po přihlášení ---
    st.success("Přihlášen jako správce")
    if st.button("Odhlásit se"):
        st.session_state.manager_auth = False
        st.rerun()

    st.write("---")

    # --- Správa CSV ---
    for service, file_path in CSV_FILES.items():
        st.subheader(service)
        data = nacti_csv(file_path)
        upravene = data.copy()

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

        nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
        if st.button("💾 Uložit změny", key=f"{service}_save"):
            if nova.strip():
                upravene.append(nova.strip())
            uloz_csv(file_path, upravene)
            st.success(f"Položky pro {service} byly uloženy.")
            st.rerun()
