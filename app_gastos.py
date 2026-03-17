import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------- CONFIG ----------
st.set_page_config(page_title="D'ela", page_icon="logo.png", layout="wide")

# ---------- LOGIN SIMPLE ----------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.image("logo.png", width=120)
    st.title("D’ela 💜")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == "daniela" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Datos incorrectos")

    st.stop()

# ---------- GOOGLE SHEETS ----------
scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds_dict = st.secrets["GOOGLE_CREDENTIALS"]

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)

sheet = client.open("https://docs.google.com/spreadsheets/d/1ZYKTKT5E5GIBLa9FceWt3PgSx0eg04_EAwF2mUWiuMI/edit?gid=0#gid=0").sheet1

data = sheet.get_all_records()

if data:
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(columns=["Fecha","Categoria","Descripcion","Valor"])

# ---------- CATEGORIAS DINÁMICAS ----------
if "categorias" not in st.session_state:
    st.session_state.categorias = [
        "Comida","Transporte","Entretenimiento","Otros"
    ]

st.sidebar.header("⚙️ Configuración")

nueva_cat = st.sidebar.text_input("Nueva categoría")

if st.sidebar.button("Agregar categoría"):
    if nueva_cat:
        st.session_state.categorias.append(nueva_cat)
        st.sidebar.success("Agregada")

# ---------- FINANZAS ----------
ingreso = st.sidebar.number_input("Ingreso mensual", min_value=0)
ahorro = st.sidebar.number_input("Meta ahorro", min_value=0)

limite = ingreso - ahorro
total = df["Valor"].sum() if not df.empty else 0
restante = limite - total

# ---------- RESUMEN ----------
st.title("💜 D’ela")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Ingreso", ingreso)
c2.metric("Ahorro", ahorro)
c3.metric("Disponible", limite)
c4.metric("Restante", restante)

# ---------- NOTIFICACIONES ----------
if total > limite:
    st.error("🚨 Te pasaste del presupuesto")
elif total > limite * 0.8:
    st.warning("⚠️ Estás cerca del límite")
elif total < limite * 0.3:
    st.success("🔥 Vas excelente en tus gastos")

# ---------- REGISTRAR ----------
st.subheader("➕ Registrar gasto")

col1,col2 = st.columns(2)

with col1:
    fecha = st.date_input("Fecha")
    categoria = st.selectbox("Categoría", st.session_state.categorias)

with col2:
    descripcion = st.text_input("Descripción")
    valor = st.number_input("Valor", min_value=0)

if st.button("Guardar"):
    sheet.append_row([str(fecha), categoria, descripcion, valor])
    st.success("Guardado 💜")
    st.rerun()

# ---------- GRAFICAS ----------
if not df.empty:
    st.subheader("📊 Análisis")

    df["Valor"] = pd.to_numeric(df["Valor"])

    st.bar_chart(df.groupby("Categoria")["Valor"].sum())
    st.line_chart(df["Valor"])

# ---------- HISTORIAL ----------
if not df.empty:
    st.subheader("📋 Historial")

    fila = st.selectbox("Eliminar", df.index)

    if st.button("Eliminar gasto"):
        sheet.delete_rows(fila + 2)
        st.rerun()

    st.dataframe(df)

# ---------- IA SIMPLE ----------
st.subheader("🤖 Asesor financiero")

if ingreso > 0:
    porcentaje = (ahorro / ingreso) * 100

    if porcentaje < 10:
        st.write("👉 Estás ahorrando muy poco, intenta subir al 20%")
    elif porcentaje < 20:
        st.write("👉 Buen inicio, puedes mejorar tu ahorro")
    else:
        st.write("🔥 Excelente manejo financiero")

# ---------- RESET ----------
if st.button("🗑️ Reset"):
    sheet.clear()
    sheet.append_row(["Fecha","Categoria","Descripcion","Valor"])
    st.rerun()
# ---------- RESET ----------
if st.button("🗑️ Reset"):
    sheet.clear()
    sheet.append_row(["Fecha","Categoria","Descripcion","Valor"])
    st.rerun()
