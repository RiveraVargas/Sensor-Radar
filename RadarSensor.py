import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================
st.set_page_config(
    page_title="Sensores Radar",
    page_icon="📡",
    layout="wide"
)

# ==========================
# TÍTULO
# ==========================
st.title("📡 Dashboard de Sensores Radar")
st.markdown(
    "Monitoreo y análisis estadístico de equipos y versiones detectadas."
)

# ==========================
# CARGA DE DATOS
# ==========================
df = pd.read_csv("muestra 300.csv")

# ==========================
# KPIs GENERALES
# ==========================
st.subheader("📊 Indicadores Generales")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Registros",
    len(df)
)

col2.metric(
    "Versiones ADB",
    df["adb_version"].nunique()
)

col3.metric(
    "Columnas",
    len(df.columns)
)

# ==========================
# TABLA GENERAL
# ==========================
st.subheader("📋 Datos Cargados")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================
# FILTRO LATERAL
# ==========================
st.sidebar.header("Filtros")

columna_filtro = st.sidebar.selectbox(
    "Seleccionar columna",
    df.columns
)

opciones = sorted(
    df[columna_filtro].dropna().unique()
)

seleccion = st.sidebar.multiselect(
    "Seleccionar valores",
    opciones,
    default=opciones
)

df_filtrado = df[
    df[columna_filtro].isin(seleccion)
]

# ==========================
# DATOS FILTRADOS
# ==========================
st.subheader("🔎 Datos Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# ==========================
# REPORTE ADB_VERSION
# ==========================
if "adb_version" in df.columns:

    st.subheader("📈 Resumen por Versión ADB")

    resumen_version = (
        df_filtrado["adb_version"]
        .value_counts()
        .reset_index()
    )

    resumen_version.columns = [
        "adb_version",
        "Cantidad"
    ]

    st.dataframe(
        resumen_version,
        use_container_width=True
    )

    colA, colB = st.columns(2)

    with colA:

        fig_bar = px.bar(
            resumen_version,
            x="adb_version",
            y="Cantidad",
            text_auto=True,
            title="Cantidad por Versión ADB"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with colB:

        fig_pie = px.pie(
            resumen_version,
            names="adb_version",
            values="Cantidad",
            title="Distribución de Versiones ADB"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

# ==========================
# GRÁFICO ADICIONAL
# ==========================
st.subheader("📊 Distribución por Categoría")

columna_grafico = st.selectbox(
    "Seleccionar columna para análisis",
    df.columns
)

conteo = (
    df_filtrado[columna_grafico]
    .value_counts()
    .reset_index()
)

conteo.columns = [
    columna_grafico,
    "Cantidad"
]

fig = px.bar(
    conteo,
    x=columna_grafico,
    y="Cantidad",
    text_auto=True,
    title=f"Distribución de {columna_grafico}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
