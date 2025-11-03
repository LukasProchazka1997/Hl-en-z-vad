import streamlit as st
import csv
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

CSV_FILE = "spojova.csv"
JMENA_FILE = "jmena.csv"
XLSX_FILE = "vystupss.xlsx"

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

def spojova_app():
    st.write("### Hlášení pro Spojovou službu")

    radky = nacti_csv(CSV_FILE)
    jmena = nacti_csv(JMENA_FILE)

    if not radky:
        st.warning("Soubor spojova.csv je prázdný nebo neexistuje")
        return

    vybrany_radek = st.selectbox("Vyber položku", radky)
    vybrane_jmeno = st.selectbox("Vyber jméno", jmena)
    popis = st.text_area("Popis / poznámka")

    if st.button("Odeslat"):
        if not vybrane_jmeno or not popis:
            st.error("Je potřeba vybrat jméno a napsat popis.")
            return
        odpoved = f"{vybrane_jmeno} → {popis}"
        cas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Uložit do XLSX
        from openpyxl import Workbook, load_workbook
        if os.path.exists(XLSX_FILE):
            wb = load_workbook(XLSX_FILE)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.append(["Původní text", "Odpověď", "Čas"])
        ws.append([vybrany_radek, odpoved, cas])
        wb.save(XLSX_FILE)

        # Odeslat e-mail
        try:
            msg = MIMEText(f"Původní text: {vybrany_radek}\nOdpověď: {odpoved}\nČas: {cas}", "plain", "utf-8")
            msg["Subject"] = f"Hlášení k: {vybrany_radek}"
            msg["From"] = EMAIL_USER
            msg["To"] = EMAIL_TO
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.send_message(msg)
            st.success("Hlášení bylo uloženo a odesláno.")
        except Exception as e:
            st.error(f"Nastala chyba při odesílání: {e}")
