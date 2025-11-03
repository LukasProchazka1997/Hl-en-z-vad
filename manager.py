import streamlit as st
import pandas as pd
import os

CSV_FILE = "manager.csv"

def manager_app():
    st.write("### Správa položek CSV")

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Položka"])

    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Uložit změny"):
        edited_df.to_csv(CSV_FILE, index=False)
        st.success(f"Soubor {CSV_FILE} byl uložen.")
