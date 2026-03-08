import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Control de gastos", page_icon="💰", layout="wide")

st.title("💳 Control de gastos de Daniela Pantoja")

archivo_gastos = "gastos.csv"
archivo_config = "config.csv"

# ---------- CARGAR GASTOS ----------
if os.path.exists(archivo_gastos):
    df = pd.read_csv(archivo_gastos)
else:
    df = pd.DataFrame(columns=["Fecha","Categoria","Descripcion","Valor"])

# ---------- CARGAR CONFIGURACION ----------
if os.path.exists(archivo_config):
    config = pd.read_csv(archivo_config)
    ingreso = int(config.loc[0,"Ingreso"])
    ahorro = int(config.loc[0,"Ahorro"])
else:
    ingreso = 0
    ahorro = 0

# ---------- CONFIGURACION ----------
st.sidebar.header("⚙️ Configuración financiera")

nuevo_ingreso = st.sidebar.number_input(
    "Ingreso mensual",
    value=ingreso,
    min_value=0
)

meta_ahorro = st.sidebar.number_input(
    "Meta de ahorro",
    value=ahorro,
    min_value=0
)

if st.sidebar.button("Guardar configuración"):
    config = pd.DataFrame([[nuevo_ingreso,meta_ahorro]],
    columns=["Ingreso","Ahorro"])
    config.to_csv(archivo_config,index=False)
    st.sidebar.success("Configuración guardada")

ingreso = nuevo_ingreso
ahorro = meta_ahorro

# ---------- LIMITE DE GASTO ----------
limite_gasto = ingreso - ahorro

st.subheader("📊 Resumen financiero")

total_gastos = df["Valor"].sum()
restante = limite_gasto - total_gastos

c1,c2,c3,c4 = st.columns(4)

c1.metric("Ingreso mensual", ingreso)
c2.metric("Meta de ahorro", ahorro)
c3.metric("Límite para gastar", limite_gasto)
c4.metric("Dinero restante", restante)

# ---------- ALERTAS ----------
if total_gastos >= limite_gasto:
    st.error("⚠️ Has alcanzado el límite de gasto del mes")
elif total_gastos >= limite_gasto * 0.8:
    st.warning("⚠️ Estás cerca del límite de gasto")

# ---------- REGISTRAR GASTO ----------
st.subheader("Registrar gasto")

col1,col2 = st.columns(2)

with col1:
    fecha = st.date_input("Fecha")
    categoria = st.selectbox("Categoría",[
        "Gastos fijos",
        "Comida",
        "Transporte",
        "Gastos personales",
        "Entretenimiento",
        "Inversión",
        "Otros"
    ])

with col2:
    descripcion = st.text_input("Descripción")
    valor = st.number_input("Valor del gasto",min_value=0)

if st.button("Guardar gasto"):

    if total_gastos + valor > limite_gasto:
        st.error("❌ Este gasto supera el límite permitido")
    else:
        nuevo = pd.DataFrame([[fecha,categoria,descripcion,valor]],
        columns=df.columns)

        df = pd.concat([df,nuevo],ignore_index=True)
        df.to_csv(archivo_gastos,index=False)

        st.success("Gasto guardado")

# ---------- GRAFICA ----------
st.subheader("📊 Distribución de gastos")

if not df.empty:
    grafica = df.groupby("Categoria")["Valor"].sum()
    st.bar_chart(grafica)

# ---------- HISTORIAL ----------
st.subheader("📋 Historial de gastos")

if not df.empty:

    fila = st.selectbox(
        "Selecciona un gasto para eliminar",
        df.index
    )

    if st.button("Eliminar gasto seleccionado"):
        df = df.drop(fila)
        df.to_csv(archivo_gastos,index=False)
        st.success("Gasto eliminado")

    st.dataframe(df)

# ---------- BORRAR TODO ----------
if st.button("🗑️ Borrar todo el historial"):
    df = pd.DataFrame(columns=df.columns)
    df.to_csv(archivo_gastos,index=False)
    st.warning("Historial eliminado")
