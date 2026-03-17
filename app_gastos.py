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

# ---------------- LOGIN ----------------
st.subheader("🔐 Iniciar sesión")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if "login" not in st.session_state:
    st.session_state.login = False

if st.button("Ingresar", key="login_btn"):
    if usuario == "admin" and password == "1234":
        st.session_state.login = True
    else:
        st.error("Usuario o contraseña incorrectos")

if not st.session_state.login:
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

# ---------------- FILTRO MENSUAL ----------------
if not df.empty:
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    mes_actual = pd.Timestamp.now().month
    anio_actual = pd.Timestamp.now().year

    df_mes = df[
        (df["Fecha"].dt.month == mes_actual) &
        (df["Fecha"].dt.year == anio_actual)
    ]
else:
    df_mes = df

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
st.subheader("📊 Tus movimientos (Mes actual)")

if not df_mes.empty:
    st.dataframe(df_mes)

    total_gastos = df_mes[df_mes["Tipo"] == "Gasto"]["Monto"].sum()
    total_ingresos = df_mes[df_mes["Tipo"] == "Ingreso"]["Monto"].sum()

    st.metric("💸 Gastos", total_gastos)
    st.metric("💰 Ingresos", total_ingresos)

    # ---------------- GRÁFICO ----------------
    st.subheader("📈 Análisis")

    try:
        resumen = df_mes.groupby("Categoría")["Monto"].sum()
        st.bar_chart(resumen)
    except:
        st.info("Agrega datos para ver gráficos")

else:
    st.info("No hay datos este mes")
    total_gastos = 0
    total_ingresos = 0

# ---------------- IA SIMPLE ----------------
st.subheader("🤖 Asesor financiero")

if total_gastos > total_ingresos:
    st.error("Estás gastando más de lo que ganas ⚠️")
else:
    st.success("Vas bien, tus finanzas están equilibradas ✅")

# ---------------- PLAN DE AHORRO (DESPLEGABLE) ----------------
with st.expander("🎯 Ver Plan de Ahorro"):

    meta = st.number_input("¿Cuánto quieres ahorrar?", min_value=0, key="meta_ahorro")

    ahorro_actual = total_ingresos - total_gastos

    st.write(f"💰 Ahorro actual: {ahorro_actual}")
    st.write(f"🎯 Meta: {meta}")

    if meta > 0:
        progreso = ahorro_actual / meta if meta != 0 else 0

        if progreso >= 1:
            st.success("🎉 ¡Meta alcanzada!")
        else:
            st.progress(min(progreso, 1.0))
            restante = meta - ahorro_actual
            st.info(f"Te faltan {restante} para cumplir tu meta")
    else:
        st.info("Define una meta para comenzar")
