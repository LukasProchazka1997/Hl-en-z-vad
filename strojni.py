import streamlit as st
import csv
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CSV_FILE = "strojni.csv"
JMENA_FILE = "jmena.csv"
XLSX_FILE = "vystupsts.xlsx"

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

def nacti_poslednich_20():
    if not os.path.exists(XLSX_FILE):
        return []
    wb = load_workbook(XLSX_FILE)
    ws = wb.active
    zaznamy = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        radek, odpoved, cas = row[:3]
        if radek and odpoved and cas:
            zaznamy.append(f"[{cas}] {radek} → {odpoved}")
    return list(reversed(zaznamy[-20:]))

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
def strojní_app(key_prefix="strojni"):
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
                # uložíme do XLSX
                cas = uloz_do_xlsx(vybrany_radek, odpoved)
                
                # pošleme email s volitelnou fotkou
                odesli_email(vybrany_radek, odpoved, cas, fotka=fotka)
                
                st.success(f"Hlášení bylo uloženo a odesláno ({cas})")
            except Exception as e:
                st.error(f"Nastala chyba: {e}")

    st.subheader("Posledních 20 hlášení")
    historie = nacti_poslednich_20()
    for z in historie:
        st.text(z)
