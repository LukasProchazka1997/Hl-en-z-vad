# manager.py
import streamlit as st
import csv
import os

SERVICE_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}

HESLO = "1234"

def manager_app():
    # --- session state ---
    if 'manager_data' not in st.session_state:
        st.session_state.manager_data = []
    if 'manager_file' not in st.session_state:
        st.session_state.manager_file = None

    service = st.selectbox("Vyber službu", list(SERVICE_FILES.keys()))

    # načtení CSV
    if st.session_state.manager_file != SERVICE_FILES[service]:
        st.session_state.manager_file = SERVICE_FILES[service]
        st.session_state.manager_data.clear()
        if os.path.exists(st.session_state.manager_file):
            with open(st.session_state.manager_file, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        st.session_state.manager_data.append(row[0])

    st.subheader(f"Položky služby: {service}")

    selected_idx = st.selectbox(
        "Vyber položku",
        options=list(range(len(st.session_state.manager_data))),
        format_func=lambda i: st.session_state.manager_data[i] if i < len(st.session_state.manager_data) else ""
    ) if st.session_state.manager_data else None

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        new_item = st.text_input("Nová položka")
        if st.button("Přidat"):
            if new_item.strip():
                st.session_state.manager_data.append(new_item.strip())
                st.experimental_rerun()

    with col2:
        if selected_idx is not None:
            edit_val = st.text_input("Upravit položku", st.session_state.manager_data[selected_idx])
            if st.button("Upravit"):
                if edit_val.strip():
                    st.session_state.manager_data[selected_idx] = edit_val.strip()
                    st.experimental_rerun()

    with col3:
        if selected_idx is not None and st.button("Smazat"):
            st.session_state.manager_data.pop(selected_idx)
            st.experimental_rerun()

    with col4:
        if selected_idx is not None and st.button("Nahoru"):
            if selected_idx > 0:
                st.session_state.manager_data[selected_idx-1], st.session_state.manager_data[selected_idx] = \
                    st.session_state.manager_data[selected_idx], st.session_state.manager_data[selected_idx-1]
                st.experimental_rerun()

    with col5:
        if selected_idx is not None and st.button("Dolů"):
            if selected_idx < len(st.session_state.manager_data) - 1:
                st.session_state.manager_data[selected_idx+1], st.session_state.manager_data[selected_idx] = \
                    st.session_state.manager_data[selected_idx], st.session_state.manager_data[selected_idx+1]
                st.experimental_rerun()

    st.write("---")
    pwd = st.text_input("Heslo pro uložení změn", type="password")
    if st.button("Uložit CSV"):
        if pwd != HESLO:
            st.error("Špatné heslo!")
        else:
            with open(st.session_state.manager_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for item in st.session_state.manager_data:
                    writer.writerow([item])
            st.success(f"Soubor {st.session_state.manager_file} byl uložen!")
