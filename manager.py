# manager.py — Streamlit Manager
import streamlit as st
import csv
import os

# --- konfigurace ---
CSV_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}

MANAGER_PASSWORD = "1234"

# --- pomocné funkce ---
def load_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def save_csv(file_path, data):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in sorted(data):  # vždy ukládáme seřazeně
            writer.writerow([item])

# --- hlavní aplikace ---
def manager_app():
    
    # vyber služby
    service = st.selectbox("Vyber službu", list(CSV_FILES.keys()))
    file_path = CSV_FILES[service]

    # načteme data do session_state
    if f"data_{service}" not in st.session_state:
        st.session_state[f"data_{service}"] = load_csv(file_path)
    
    data = st.session_state[f"data_{service}"]
    data.sort()  # vždy abecedně

    # heslo pro úpravy
    if "auth_pass" not in st.session_state:
        st.session_state.auth_pass = ""

    st.text("Pro úpravy zadejte heslo")
    password = st.text_input("Heslo", type="password")

    # --- seznam položek ---
    st.write("### Položky")
    st.write("\n".join(data) if data else "*Žádné položky*")

    # pokud je heslo správné, umožníme CRUD
    if password == MANAGER_PASSWORD:
        st.session_state.auth_pass = password

        # --- přidat položku ---
        new_item = st.text_input("Nová položka", "")
        if st.button("Přidat"):
            if new_item.strip():
                if new_item.strip() not in data:
                    data.append(new_item.strip())
                    save_csv(file_path, data)
                    st.success(f"Položka '{new_item.strip()}' přidána")
                else:
                    st.warning("Tato položka již existuje")
            st.experimental_rerun()

        # --- upravit položku ---
        if data:
            edit_item = st.selectbox("Vyber položku k úpravě", data)
            new_value = st.text_input("Nová hodnota", "")
            if st.button("Upravit"):
                if new_value.strip():
                    idx = data.index(edit_item)
                    data[idx] = new_value.strip()
                    save_csv(file_path, data)
                    st.success(f"Položka '{edit_item}' byla upravena na '{new_value.strip()}'")
                st.experimental_rerun()

        # --- smazat položku ---
        if data:
            del_item = st.selectbox("Vyber položku k odstranění", data, key="del_select")
            if st.button("Smazat"):
                data.remove(del_item)
                save_csv(file_path, data)
                st.success(f"Položka '{del_item}' byla smazána")
                st.experimental_rerun()
    else:
        if password:
            st.warning("Špatné heslo")
