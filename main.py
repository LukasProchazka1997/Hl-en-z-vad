import streamlit as st
from spojova import Aplikace as SpojovaApp
from technicka import Aplikace as TechnickaApp
from strojni import Aplikace as StrojniApp
from manager import Manager


# Hlavní nadpis
st.set_page_config(page_title="Hlášení závad", layout="wide")
st.title("Hlášení závad")

# Záložky místo Tkinter notebooku
tabs = st.tabs(["Spojová služba", "Technická služba", "Strojní služba", "Manager"])

# --- SPOJOVÁ SLUŽBA ---
with tabs[0]:
    st.subheader("Spojová služba")
    SpojovaApp(st)

# --- TECHNICKÁ SLUŽBA ---
with tabs[1]:
    st.subheader("Technická služba")
    TechnickaApp(st)

# --- STROJNÍ SLUŽBA ---
with tabs[2]:
    st.subheader("Strojní služba")
    StrojniApp(st)

# --- MANAGER ---
with tabs[3]:
    st.subheader("Manager")
    Manager(st)
