import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Modelos",
    layout="wide"
)

st.title("📊 Dashboard de Modelos y Versiones")

# Cargar CSV
df = pd.read_csv("muestra 300.csv")

# Mostrar tabla
st.subheader("Datos Cargados")
st.dataframe(df, use_container_width=True)

# Mostrar columnas
st.write("Columnas detectadas:")
st.write(df.columns.tolist())

# Seleccionar columna para filtrar
columna_filtro = st.sidebar.selectbox(
    "Filtrar por",
    df.columns
)

opciones = sorted(df[columna_filtro].dropna().unique())

seleccion = st.sidebar.multiselect(
    "Seleccionar valores",
    opciones,
    default=opciones
)

df_filtrado = df[df[columna_filtro].isin(seleccion)]

st.subheader("Datos Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Indicadores
col1, col2, col3 = st.columns(3)

col1.metric(
    "Registros",
    len(df_filtrado)
)

col2.metric(
    "Columnas",
    len(df_filtrado.columns)
)

col3.metric(
    "Valores Únicos",
    df_filtrado[columna_filtro].nunique()
)

# Gráfico de barras
conteo = (
    df_filtrado[columna_filtro]
    .value_counts()
    .reset_index()
)

conteo.columns = [columna_filtro, "Cantidad"]

fig = px.bar(
    conteo,
    x=columna_filtro,
    y="Cantidad",
    title=f"Distribución por {columna_filtro}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Gráfico circular
fig2 = px.pie(
    conteo,
    names=columna_filtro,
    values="Cantidad",
    title=f"Participación por {columna_filtro}"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
