# ==================================
# RESUMEN POR ADSB_VERSION
# ==================================

if "adsb_version" in df_filtrado.columns:

    st.subheader("📡 Resumen de Modelos por ADS-B Version")

    resumen_adsb = (
        df_filtrado["adsb_version"]
        .value_counts()
        .reset_index()
    )

    resumen_adsb.columns = [
        "adsb_version",
        "Cantidad"
    ]

    st.dataframe(
        resumen_adsb,
        use_container_width=True
    )

    colA, colB = st.columns(2)

    with colA:
        fig_adsb_bar = px.bar(
            resumen_adsb,
            x="adsb_version",
            y="Cantidad",
            text="Cantidad",
            title="Cantidad por ADS-B Version"
        )

        st.plotly_chart(
            fig_adsb_bar,
            use_container_width=True
        )

    with colB:
        fig_adsb_pie = px.pie(
            resumen_adsb,
            names="adsb_version",
            values="Cantidad",
            title="Distribución de ADS-B Version"
        )

        st.plotly_chart(
            fig_adsb_pie,
            use_container_width=True
        )
