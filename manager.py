# manager.py (Streamlit verze)
import streamlit as st
import csv
import os

DEFAULT_CSV = "manager.csv"

def load_csv(file=None):
    data = []
    if file:
        content = file.getvalue().decode("utf-8")
        reader = csv.reader(content.splitlines())
        data = [row[0] for row in reader if row]
    elif os.path.exists(DEFAULT_CSV):
        with open(DEFAULT_CSV, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = [row[0] for row in reader if row]
    return data

def save_csv(data, filename=DEFAULT_CSV):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow([item])
    st.success(f"CSV uložen: {filename}")

def manager_app(key_prefix="manager"):
    st.subheader("Manager")

    uploaded_file = st.file_uploader("Načíst CSV", type=["csv"], key=f"{key_prefix}_uploader")
    data = load_csv(uploaded_file)

    # Session state pro data
    if f"{key_prefix}_data" not in st.session_state:
        st.session_state[f"{key_prefix}_data"] = data

    items = st.session_state[f"{key_prefix}_data"]

    # Zobrazení položek s možností editace
    st.write("### Položky")
    for i, item in enumerate(items):
        col1, col2, col3, col4 = st.columns([4,2,2,2])
        col1.text_input(f"Položka {i}", value=item, key=f"{key_prefix}_item_{i}", on_change=lambda idx=i: items.__setitem__(idx, st.session_state[f"{key_prefix}_item_{idx}"]))
        if col2.button("Nahoru", key=f"{key_prefix}_up_{i}") and i>0:
            items[i-1], items[i] = items[i], items[i-1]
        if col3.button("Dolů", key=f"{key_prefix}_down_{i}") and i < len(items)-1:
            items[i+1], items[i] = items[i], items[i+1]
        if col4.button("Smazat", key=f"{key_prefix}_del_{i}"):
            items.pop(i)
            st.experimental_rerun()

    # Přidání nové položky
    new_item = st.text_input("Nová položka", key=f"{key_prefix}_new")
    if st.button("Přidat položku", key=f"{key_prefix}_add") and new_item.strip():
        items.append(new_item.strip())
        st.session_state[f"{key_prefix}_new"] = ""
        st.experimental_rerun()

    # Uložit CSV
    if st.button("Uložit CSV", key=f"{key_prefix}_save"):
        save_csv(items)
