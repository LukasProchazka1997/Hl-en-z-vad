import streamlit as st
from datetime import datetime
import csv
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CSV_FILE = "spojova.csv"
JMENA_FILE = "jmena.csv"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "vyjezdhhmh@gmail.com"
EMAIL_PASS = "lzjh kbtc xdkk jaiy"
EMAIL_TO = "lupc@post.cz"

# --------------------
# Pomocné funkce
# --------------------
def nacti_csv(soubor):
    try:
        with open(soubor, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        st.warning(f"{soubor} nenalezen, seznam bude prázdný.")
        return []

def uloz_do_session(radek, odpoved):
    cas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zaznam = {"radek": radek, "odpoved": odpoved, "cas": cas}
    if "hlaseni" not in st.session_state:
        st.session_state.hlaseni = []
    st.session_state.hlaseni.append(zaznam)
    return cas

def nacti_poslednich_20():
    if "hlaseni" not in st.session_state:
        return []
    return list(reversed([f"[{z['cas']}] {z['radek']} → {z['odpoved']}" for z in st.session_state.hlaseni[-20:]]))

def odesli_email(radek, odpoved, cas, fotka=None):
    msg = MIMEMultipart()
    msg["Subject"] = f"Hlášení k: {radek}"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    text = f"Původní text: {radek}\nOdpověď: {odpoved}\nČas: {cas}"
    msg.attach(MIMEText(text, "plain", "utf-8"))

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

def export_xlsx():
    import openpyxl
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append(["Původní text", "Odpověď", "Čas"])
    for z in st.session_state.hlaseni:
        ws.append([z["radek"], z["odpoved"], z["cas"]])
    
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    return file_stream

# --------------------
# Streamlit aplikace
# --------------------
def spojova_app():
    radky = nacti_csv(CSV_FILE)
    jmena = nacti_csv(JMENA_FILE)

    vybrany_radek = st.selectbox("Vyber položku", radky)
    vybrane_jmeno = st.selectbox("Vyber jméno", jmena)
    popis = st.text_area("Popis / poznámka")

    fotka = st.file_uploader("Přiložit fotku (volitelné)", type=["png", "jpg", "jpeg"])

    if st.button("Odeslat hlášení"):
        st.write("Tlačítko stisknuto")  # debug
        st.write(f"Vybraný řádek: {vybrany_radek}")
        st.write(f"Vybrané jméno: {vybrane_jmeno}")
        st.write(f"Popis: {popis.strip()}")

        if not vybrany_radek or not vybrane_jmeno or not popis.strip():
            st.error("Vyplňte všechny položky.")
        else:
            odpoved = f"{vybrane_jmeno} → {popis.strip()}"
            try:
                # uložíme do session
                cas = uloz_do_session(vybrany_radek, odpoved)

                # pošleme email
                odesli_email(vybrany_radek, odpoved, cas, fotka=fotka)

                st.success(f"Hlášení bylo uloženo a odesláno ({cas})")
            except Exception as e:
                st.error(f"Nastala chyba: {e}")

    st.subheader("Posledních 20 hlášení")
    historie = nacti_poslednich_20()
    for z in historie:
        st.text(z)

    # Export do XLSX
    if st.button("Exportovat všechna hlášení do XLSX"):
        xlsx_data = export_xlsx()
        st.download_button("Stáhnout XLSX", xlsx_data, file_name="vystupss.xlsx")

# Spuštění aplikace
spojova_app()
