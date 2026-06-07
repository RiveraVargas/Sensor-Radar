import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# CONFIGURACIÓN DE PÁGINA
# =====================================
st.set_page_config(
    page_title="(GRUPO 04): ANALISIS DE LA MADUREZ TECNOLOGICA ADS-B DE LAS AERONAVES QUE OPERAN EN LA FIR LIMA",
    page_icon="📡",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================
st.title("📡 DATA SENSOR RADAR - GRUPO 04")
st.markdown(
    "### Dashboard interactivo para análisis y visualización de datos de sensores radar"
)

# =====================================
# CARGA DE DATOS
# =====================================
df = pd.read_csv("muestra 300.csv")

# =====================================
# TABLA GENERAL
# =====================================
st.subheader("📋 Datos Cargados")
st.dataframe(df, use_container_width=True)

# =====================================
# COLUMNAS DETECTADAS
# =====================================
st.subheader("📑 Columnas Detectadas")
st.write(df.columns.tolist())

# =====================================
# FILTRO LATERAL
# =====================================
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

# =====================================
# DATOS FILTRADOS
# =====================================
st.subheader("📋 Datos Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# =====================================
# INDICADORES GENERALES
# =====================================
st.subheader("📊 Indicadores Generales")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Registros",
    len(df_filtrado)
)

col2.metric(
    "Total Columnas",
    len(df_filtrado.columns)
)

col3.metric(
    "Valores Únicos",
    df_filtrado[columna_filtro].nunique()
)

# =====================================
# RESUMEN ADSB VERSION
# =====================================
if "adsb_version" in df_filtrado.columns:

    st.subheader("📡 Resumen Estadístico de ADS-B Version")

    total_registros = len(df_filtrado)

    resumen_adsb = (
        df_filtrado["adsb_version"]
        .value_counts()
        .reset_index()
    )

    resumen_adsb.columns = [
        "ADS-B Version",
        "Cantidad"
    ]

    resumen_adsb["Porcentaje (%)"] = (
        resumen_adsb["Cantidad"] /
        total_registros * 100
    ).round(2)

    st.markdown("#### Tabla de Cuantización")

    st.dataframe(
        resumen_adsb,
        use_container_width=True
    )

    colA, colB, colC = st.columns(3)

    colA.metric(
        "Versiones ADS-B",
        resumen_adsb.shape[0]
    )

    colB.metric(
        "Total Registros",
        total_registros
    )

    colC.metric(
        "Versión Más Frecuente",
        str(resumen_adsb.iloc[0]["ADS-B Version"])
    )

    # Gráfico de barras ADS-B
    fig_adsb = px.bar(
        resumen_adsb,
        x="ADS-B Version",
        y="Cantidad",
        text="Cantidad",
        title="Cantidad de Registros por ADS-B Version"
    )

    st.plotly_chart(
        fig_adsb,
        use_container_width=True
    )

    # Gráfico circular ADS-B
    fig_adsb_pie = px.pie(
        resumen_adsb,
        names="ADS-B Version",
        values="Cantidad",
        title="Participación Porcentual por ADS-B Version"
    )

    st.plotly_chart(
        fig_adsb_pie,
        use_container_width=True
    )

# =====================================
# DISTRIBUCIÓN SEGÚN FILTRO
# =====================================
st.subheader("📈 Distribución según Filtro Seleccionado")

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

# =====================================
# PARTICIPACIÓN SEGÚN FILTRO
# =====================================
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
