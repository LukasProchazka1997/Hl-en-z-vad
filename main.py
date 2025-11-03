import streamlit as st

# Import Streamlit verze jednotlivých aplikací
from spojova import spojova_app
from technicka import technicka_app
from strojni import strojni_app
from manager import manager_app  # pokud máš Streamlit Manager verzi

# Hlavní nadpis
st.set_page_config(page_title="Hlášení závad", layout="wide")
st.title("Hlášení závad")

# Záložky
tabs = st.tabs(["Spojová služba", "Technická služba", "Strojní služba", "Manager"])

# --- SPOJOVÁ SLUŽBA ---
with tabs[0]:
    st.subheader("Spojová služba")
    spojova_app()

# --- TECHNICKÁ SLUŽBA ---
with tabs[1]:
    st.subheader("Technická služba")
    technicka_app()

# --- STROJNÍ SLUŽBA ---
with tabs[2]:
    st.subheader("Strojní služba")
    strojni_app()

# --- MANAGER ---
with tabs[3]:
    st.subheader("Manager")
    manager_app()
