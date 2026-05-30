import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================
st.set_page_config(
    page_title="DATA SENSOR RADAR - GRUPO 04",
    page_icon="📡",
    layout="wide"
)

# ==========================
# TÍTULO DEL DASHBOARD
# ==========================
st.title("📡 DATA SENSOR RADAR - GRUPO 04")
st.markdown(
    "### Dashboard interactivo para análisis y visualización de datos de sensores radar"
)

# ==========================
# CARGA DE DATOS
# ==========================
df = pd.read_csv("muestra 300.csv")

# ==========================
# TABLA GENERAL
# ==========================
st.subheader("📋 Datos Cargados")
st.dataframe(df, use_container_width=True)

# ==========================
# COLUMNAS DETECTADAS
# ==========================
st.subheader("📑 Columnas Detectadas")
st.write(df.columns.tolist())

# ==========================
# FILTRO LATERAL
# ==========================
st.sidebar.header("🔎 Filtros")

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

# ==========================
# DATOS FILTRADOS
# ==========================
st.subheader("📋 Datos Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# ==========================
# INDICADORES
# ==========================
st.subheader("📊 Indicadores")

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

# ==========================
# GRÁFICO DE BARRAS
# ==========================
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
    text="Cantidad",
    title=f"Distribución por {columna_filtro}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# GRÁFICO CIRCULAR
# ==========================
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
