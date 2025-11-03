# technicka.py
import streamlit as st
import csv
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os
import smtplib
from email.mime.text import MIMEText

CSV_FILE = "technicka.csv"
JMENA_FILE = "jmena.csv"
XLSX_FILE = "vystupts.xlsx"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "vyjezdhhmh@gmail.com"
EMAIL_PASS = "lzjh kbtc xdkk jaiy"
EMAIL_TO = "lupc@post.cz"

def nacti_csv(soubor):
    if not os.path.exists(soubor):
        return []
    with open(soubor, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_do_xlsx(radek, odpoved):
    cas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(XLSX_FILE):
        wb = load_workbook(XLSX_FILE)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["Původní text", "Odpověď", "Čas"])
    ws.append([radek, odpoved, cas])
    wb.save(XLSX_FILE)
    return cas

def odesli_email(radek, odpoved, cas):
    predmet = f"Hlášení k: {radek}"
    text = f"Původní text: {radek}\nOdpověď: {odpoved}\nČas: {cas}"
    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = predmet
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def techncka_app(key_prefix="spojova"):
    st.subheader("Technická služba")
    radky = nacti_csv(CSV_FILE)
    jmena = nacti_csv(JMENA_FILE)

    vybrany_radek = st.selectbox("Vyber položku", radky, key=f"{key_prefix}_radek")
    vybrane_jmeno = st.selectbox("Vyber jméno", jmena, key=f"{key_prefix}_jmeno")
    popis = st.text_area("Popis / poznámka", key=f"{key_prefix}_popis")

    if st.button("Odeslat hlášení", key=f"{key_prefix}_odeslat"):
        if not vybrany_radek or not vybrane_jmeno or not popis.strip():
            st.error("Vyplňte všechny položky.")
        else:
            odpoved = f"{vybrane_jmeno} → {popis.strip()}"
            try:
                cas = uloz_do_xlsx(vybrany_radek, odpoved)
                odesli_email(vybrany_radek, odpoved, cas)
                st.success(f"Hlášení bylo uloženo a odesláno ({cas})")
            except Exception as e:
                st.error(f"Nastala chyba: {e}")
