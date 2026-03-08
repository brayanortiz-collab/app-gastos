import streamlit as st
import pandas as pd
import os

# configuración de la página
st.set_page_config(page_title="Control de gastos", page_icon="💰", layout="wide")

st.title("💳 Control de gastos de Daniela Pantoja")

archivo = "gastos.csv"

# cargar datos
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["Fecha","Categoria","Descripcion","Valor"])

# ingreso mensual
st.sidebar.header("💰 Configuración")
ingreso = st.sidebar.number_input("Ingreso mensual", min_value=0)

st.sidebar.write("Este valor permite calcular el dinero restante del mes.")

# formulario para registrar gasto
st.subheader("Registrar gasto")

col1, col2 = st.columns(2)

with col1:
    fecha = st.date_input("Fecha")
    categoria = st.selectbox(
        "Categoría",
        [
            "Gastos fijos",
            "Comida",
            "Transporte",
            "Gastos personales",
            "Entretenimiento",
            "Inversión",
            "Otros"
        ]
    )

with col2:
    descripcion = st.text_input("Descripción")
    valor = st.number_input("Valor del gasto", min_value=0)

if st.button("Guardar gasto"):
    nuevo = pd.DataFrame([[fecha, categoria, descripcion, valor]],
    columns=df.columns)
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(archivo, index=False)
    st.success("Gasto guardado correctamente")

# resumen financiero
st.subheader("📊 Resumen financiero")

total_gastos = df["Valor"].sum()
restante = ingreso - total_gastos

c1, c2, c3 = st.columns(3)

c1.metric("Ingreso mensual", ingreso)
c2.metric("Total gastado", total_gastos)
c3.metric("Dinero restante", restante)

# gráfico de gastos
st.subheader("📊 Distribución de gastos por categoría")

if not df.empty:
    grafica = df.groupby("Categoria")["Valor"].sum()
    st.bar_chart(grafica)

# historial de gastos
st.subheader("📋 Historial de gastos")
st.dataframe(df)
