# strojni.py
import streamlit as st
import csv
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

CSV_FILE = "strojni.csv"
JMENA_FILE = "jmena.csv"
JSON_FILE = "strojni.json"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "vyjezdhhmh@gmail.com"
EMAIL_PASS = "lzjh kbtc xdkk jaiy"
EMAIL_TO = "lupc@post.cz"

# --------------------
# Pomocné funkce
# --------------------
def nacti_csv(soubor):
    if not os.path.exists(soubor):
        return []
    with open(soubor, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def uloz_do_json(radek, odpoved):
    cas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append({"radek": radek, "odpoved": odpoved, "cas": cas})
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return cas

def nacti_poslednich_20():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    historie = [f"[{z['cas']}] {z['radek']} → {z['odpoved']}" for z in data]
    return historie[-20:]

def odesli_email(radek, odpoved, cas, fotka=None):
    msg = MIMEMultipart()
    msg["Subject"] = f"Hlášení k: {radek}"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    # Text emailu
    text = f"Původní text: {radek}\nOdpověď: {odpoved}\nČas: {cas}"
    msg.attach(MIMEText(text, "plain", "utf-8"))

    # Připojení fotky
    if fotka is not None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(fotka.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{fotka.name}"')
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# --------------------
# Hlavní Streamlit aplikace
# --------------------
def strojni_app(key_prefix="strojni"):
    radky = nacti_csv(CSV_FILE)
    jmena = nacti_csv(JMENA_FILE)

    vybrany_radek = st.selectbox("Vyber položku", radky, key=f"{key_prefix}_radek")
    vybrane_jmeno = st.selectbox("Vyber jméno", jmena, key=f"{key_prefix}_jmeno")
    popis = st.text_area("Popis / poznámka", key=f"{key_prefix}_popis")
    fotka = st.file_uploader("Přiložit fotku (volitelné)", type=["png", "jpg", "jpeg"], key=f"{key_prefix}_fotka")

    if st.button("Odeslat hlášení", key=f"{key_prefix}_odeslat"):
        if not vybrany_radek or not vybrane_jmeno or not popis.strip():
            st.error("Vyplňte všechny položky.")
        else:
            odpoved = f"{vybrane_jmeno} → {popis.strip()}"
            try:
                cas = uloz_do_json(vybrany_radek, odpoved)
                odesli_email(vybrany_radek, odpoved, cas, fotka=fotka)
                st.success(f"Hlášení bylo uloženo a odesláno ({cas})")
            except Exception as e:
                st.error(f"Nastala chyba: {e}")

    historie = nacti_poslednich_20()
    for z in historie:
        st.text(z)
