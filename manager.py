# manager.py — Streamlit verze s tlačítky nahoru/dolů a správou jmen
import streamlit as st
import csv
import os

# --- Nastavení ---
CSV_FILES = {
    "spojova": "spojova.csv",
    "technicka": "technicka.csv",
    "strojni": "strojni.csv",
    "jmena": "jmena.csv"
}

MANAGER_PASSWORD = "tajneheslo123"

# --- Pomocné funkce ---
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

# --- Hlavní aplikace managera ---
def manager_app():
    st.subheader("Správa položek a jmen – přístup chráněn heslem")
    heslo = st.text_input("Zadejte heslo", type="password")
    if heslo != MANAGER_PASSWORD:
        st.warning("Zadejte správné heslo")
        return

    # --- Výběr služby ---
    service = st.selectbox("Vyber službu k úpravě", ["spojova", "technicka", "strojni", "jmena"])
    file_path = CSV_FILES[service]

    data = nacti_csv(file_path)

    st.write("**Aktuální položky:**")
    # Zobrazíme seznam s tlačítky nahoru/dolů a možností smazání
    upravene = data.copy()
    for i, item in enumerate(data):
        col1, col2, col3, col4 = st.columns([4,1,1,1])
        col1.text(item)
        if col2.button("↑", key=f"{service}_up_{i}") and i > 0:
            upravene[i], upravene[i-1] = upravene[i-1], upravene[i]
        if col3.button("↓", key=f"{service}_down_{i}") and i < len(upravene)-1:
            upravene[i], upravene[i+1] = upravene[i+1], upravene[i]
        if col4.button("❌", key=f"{service}_del_{i}"):
            upravene[i] = None

    # Odstraníme smazané položky
    upravene = [x for x in upravene if x]

    # Přidání nové položky
    nova = st.text_input("Přidat novou položku", key=f"{service}_nova")
    if st.button("Uložit změny"):
        if nova.strip():
            upravene.append(nova.strip())
        # Uložíme zpět do CSV
        uloz_csv(file_path, upravene)
        st.success(f"Položky pro {service} byly uloženy.")
        # Rerun aplikace pro okamžité zobrazení
        st.experimental_rerun()
