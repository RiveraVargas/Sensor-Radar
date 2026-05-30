import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(
    page_title="Dashboard de Modelos",
    layout="wide"
)

st.title("📊 Dashboard de Modelos y Versiones")

# Cargar archivo Excel desde GitHub local
archivo = "muestra 300.csv"

try:
    df = pd.read_excel(archivo)

    st.success("Archivo cargado correctamente")

    # Mostrar columnas
    st.subheader("Vista General de Datos")
    st.dataframe(df, use_container_width=True)

    # Seleccionar columna de versión
    columnas = df.columns.tolist()

    col_filtro = st.sidebar.selectbox(
        "Seleccionar columna para filtrar",
        columnas
    )

    opciones = sorted(df[col_filtro].dropna().unique())

    seleccion = st.sidebar.multiselect(
        f"Filtrar por {col_filtro}",
        opciones,
        default=opciones
    )

    df_filtrado = df[df[col_filtro].isin(seleccion)]

    st.subheader("Datos Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

    # KPIs
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Registros", len(df_filtrado))
    c2.metric("Columnas", len(df_filtrado.columns))
    c3.metric("Valores Únicos", df_filtrado[col_filtro].nunique())

    # Selección de gráfico
    st.subheader("Gráficos")

    col_x = st.selectbox(
        "Eje X",
        columnas,
        index=0
    )

    conteo = (
        df_filtrado[col_x]
        .value_counts()
        .reset_index()
    )

    conteo.columns = [col_x, "Cantidad"]

    fig_bar = px.bar(
        conteo,
        x=col_x,
        y="Cantidad",
        title=f"Distribución por {col_x}"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        conteo,
        names=col_x,
        values="Cantidad",
        title=f"Participación por {col_x}"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # Histograma para columnas numéricas
    numericas = df_filtrado.select_dtypes(
        include=["int64", "float64"]
    ).columns

    if len(numericas) > 0:

        variable = st.selectbox(
            "Variable Numérica",
            numericas
        )

        fig_hist = px.histogram(
            df_filtrado,
            x=variable,
            nbins=30,
            title=f"Distribución de {variable}"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

except Exception as e:
    st.error(f"Error al cargar archivo: {e}")
