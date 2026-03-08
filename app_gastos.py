import streamlit as st
import pandas as pd
import os

st.title("Control de gastos")

archivo = "gastos.csv"

if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["Fecha","Categoria","Descripcion","Valor"])

st.subheader("Registrar gasto")

fecha = st.date_input("Fecha")
categoria = st.selectbox("Categoria",[
"Gastos fijos","Comida","Transporte",
"Gastos personales","Entretenimiento","Inversion"
])

descripcion = st.text_input("Descripcion")
valor = st.number_input("Valor")

if st.button("Guardar"):
    nuevo = pd.DataFrame([[fecha,categoria,descripcion,valor]],
    columns=df.columns)
    df = pd.concat([df,nuevo],ignore_index=True)
    df.to_csv(archivo,index=False)
    st.success("Gasto guardado")

st.subheader("Gastos registrados")
st.dataframe(df)

if not df.empty:
    st.subheader("Grafica de gastos")
    grafica = df.groupby("Categoria")["Valor"].sum()
    st.bar_chart(grafica)