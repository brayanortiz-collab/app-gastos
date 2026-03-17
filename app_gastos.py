import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
st.set_page_config(page_title="D’ela 💜", layout="centered")

# ---------------- LOGO ----------------
st.image("logo.png", width=120)

st.title("D’ela 💜")
st.subheader("Tu app financiera inteligente")

# ---------------- LOGIN SIMPLE ----------------
usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if usuario != "admin" or password != "1234":
    st.warning("Ingresa usuario y contraseña")
    st.stop()

# ---------------- GOOGLE SHEETS ----------------
scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds_dict = st.secrets["GOOGLE_CREDENTIALS"]

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1ZYKTKT5E5GIBLa9FceWt3PgSx0eg04_EAwF2mUWiuMI/edit?gid=0#gid=0"
).sheet1

# ---------------- CARGAR DATOS ----------------
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])

# ---------------- FORMULARIO ----------------
st.subheader("➕ Agregar movimiento")

fecha = st.date_input("Fecha")
tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])
categoria = st.text_input("Categoría")
monto = st.number_input("Monto", min_value=0)
descripcion = st.text_input("Descripción")

# ---------------- BOTONES ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Guardar", key="guardar_gasto"):
        nueva_fila = [str(fecha), tipo, categoria, monto, descripcion]
        sheet.append_row(nueva_fila)
        st.success("Guardado correctamente")
        st.rerun()

with col2:
    if st.button("🗑️ Reset", key="reset_gastos"):
        st.warning("Formulario limpiado")
        st.rerun()

# ---------------- MOSTRAR DATOS ----------------
st.subheader("📊 Tus movimientos")

if not df.empty:
    st.dataframe(df)

    total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
    total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()

    st.metric("💸 Gastos", total_gastos)
    st.metric("💰 Ingresos", total_ingresos)

    # ---------------- GRÁFICO ----------------
    st.subheader("📈 Análisis")

    try:
        resumen = df.groupby("Categoría")["Monto"].sum()
        st.bar_chart(resumen)
    except:
        st.info("Agrega datos para ver gráficos")

else:
    st.info("Aún no hay datos registrados")

# ---------------- IA SIMPLE ----------------
st.subheader("🤖 Asesor financiero")

if not df.empty:
    if total_gastos > total_ingresos:
        st.error("Estás gastando más de lo que ganas ⚠️")
    else:
        st.success("Vas bien, tus finanzas están equilibradas ✅")
# ---------- RESET ----------
if st.button("🗑️ Reset"):
    sheet.clear()
    sheet.append_row(["Fecha","Categoria","Descripcion","Valor"])
    st.rerun()
