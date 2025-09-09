import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configurar la página
st.set_page_config(page_title="Reporte Expedientes", layout="wide", initial_sidebar_state="expanded")

# Cargar datos
df_expedientes = pd.read_csv("expedientes_generados.csv")
df_pases = pd.read_csv("pases_generados.csv")

# Convertir fechas a datetime
df_expedientes['Fecha inicio'] = pd.to_datetime(df_expedientes['Fecha inicio'], errors='coerce')
df_pases['Fecha ingreso'] = pd.to_datetime(df_pases['Fecha ingreso'], errors='coerce')

# Sidebar: selección rango fechas
with st.sidebar:
    st.header("Filtros")
    fecha_desde = st.date_input("Fecha Desde", value=df_expedientes['Fecha inicio'].min())
    fecha_hasta = st.date_input("Fecha Hasta", value=df_expedientes['Fecha inicio'].max())
    boton_consultar = st.button("Consultar")

if boton_consultar:
    # Filtrar expedientes por fecha inicio
    df_exp_filtrado = df_expedientes[
        (df_expedientes['Fecha inicio'] >= pd.to_datetime(fecha_desde)) &
        (df_expedientes['Fecha inicio'] <= pd.to_datetime(fecha_hasta))
    ]

    # Filtrar pases por fecha ingreso
    df_pases_filtrado = df_pases[
        (df_pases['Fecha ingreso'] >= pd.to_datetime(fecha_desde)) &
        (df_pases['Fecha ingreso'] <= pd.to_datetime(fecha_hasta))
    ]

    st.title(f"Reporte Expedientes del {fecha_desde} al {fecha_hasta}")

    # -- KPIs en columnas --
    col1, col2, col3 = st.columns(3)

    # Promedio días primer pase en legales (preparar datos)
    df_pases_legales = df_pases_filtrado[df_pases_filtrado['Sector'] == 'Legales']
    df_primer_pase = df_pases_legales.groupby('Nro. Expediente')['Fecha ingreso'].min().reset_index()
    df_primer_pase = df_primer_pase.rename(columns={'Fecha ingreso': 'Fecha ingreso_pase'})
    df_promedio = pd.merge(df_exp_filtrado, df_primer_pase, on='Nro. Expediente', how='inner')
    df_promedio['Dias_Resolucion'] = (df_promedio['Fecha ingreso_pase'] - df_promedio['Fecha inicio']).dt.days
    promedio_dias = df_promedio['Dias_Resolucion'].mean() if not df_promedio.empty else 0

    col1.metric("Total Expedientes", len(df_exp_filtrado))
    col2.metric("Total Pases", len(df_pases_filtrado))
    col3.metric("Promedio días primer pase 'Legales'", f"{promedio_dias:.2f}")

    # Botones para descargar datos
    csv_expedientes = df_exp_filtrado.to_csv(index=False).encode('utf-8')
    csv_pases = df_pases_filtrado.to_csv(index=False).encode('utf-8')

    with st.expander("Descargar datos filtrados"):
        st.download_button("Descargar Expedientes Filtrados CSV", data=csv_expedientes, file_name="expedientes_filtrados.csv", mime="text/csv")
        st.download_button("Descargar Pases Filtrados CSV", data=csv_pases, file_name="pases_filtrados.csv", mime="text/csv")

    # 1. Cantidad de expedientes por Sector Actual
    df_sector = df_exp_filtrado.groupby('Sector Actual').size().reset_index(name='Cantidad')
    fig_sector = px.bar(df_sector, x='Sector Actual', y='Cantidad', text='Cantidad', title="Expedientes por Sector")

    st.subheader("Cantidad de Expedientes por Sector Actual")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_sector)
    with col2:
        st.plotly_chart(fig_sector, use_container_width=True)

    # 2. Cantidad de expedientes por Tipo Expediente
    df_tipo = df_exp_filtrado.groupby('Tipo Expediente').size().reset_index(name='Cantidad')
    fig_tipo = px.pie(df_tipo, names='Tipo Expediente', values='Cantidad', hole=0.4, title="Distribución por Tipo")

    st.subheader("Cantidad de Expedientes por Tipo")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_tipo)
    with col2:
        st.plotly_chart(fig_tipo, use_container_width=True)

    # 3. Expedientes sin pase en sector "Legales"
    expedientes_con_pase_legales = df_pases_filtrado[df_pases_filtrado['Sector'] == 'Legales']['Nro. Expediente'].unique()
    df_no_pase_legales = df_exp_filtrado[~df_exp_filtrado['Nro. Expediente'].isin(expedientes_con_pase_legales)]
    df_no_pase_tipo = df_no_pase_legales.groupby('Tipo Expediente').size().reset_index(name='Cantidad')
    fig_no_pase = px.bar(df_no_pase_tipo, x='Tipo Expediente', y='Cantidad', text='Cantidad', title="Expedientes sin pase por 'Legales'")

    st.subheader("Expedientes sin pase por 'Legales'")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_no_pase_tipo)
    with col2:
        st.plotly_chart(fig_no_pase, use_container_width=True)

    # 4. Expedientes iniciados por día (serie temporal)
    df_dia = df_exp_filtrado.groupby('Fecha inicio').size().reset_index(name='Cantidad')
    fig_dia = px.bar(df_dia, x='Fecha inicio', y='Cantidad', title="Expedientes por Día")

    st.subheader("Expedientes iniciados por día")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_dia)
    with col2:
        st.plotly_chart(fig_dia, use_container_width=True)

    # 5. Promedio días entre inicio expediente y primer pase en "Legales"
    df_pases_legales = df_pases_filtrado[df_pases_filtrado['Sector'] == 'Legales']

    df_primer_pase = df_pases_legales.groupby('Nro. Expediente')['Fecha ingreso'].min().reset_index()
    df_primer_pase = df_primer_pase.rename(columns={'Fecha ingreso': 'Fecha ingreso_pase'})

    df_promedio = pd.merge(df_exp_filtrado, df_primer_pase, on='Nro. Expediente', how='inner')
    df_promedio['Dias_Resolucion'] = (df_promedio['Fecha ingreso_pase'] - df_promedio['Fecha inicio']).dt.days
    promedio_dias = df_promedio['Dias_Resolucion'].mean()

    st.subheader("Promedio de días para primer pase en 'Legales'")
    st.write(f"Promedio: {promedio_dias:.2f} días")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_promedio[['Nro. Expediente', 'Tipo Expediente', 'Fecha inicio', 'Fecha ingreso_pase', 'Dias_Resolucion']])
    with col2:
        # Por ejemplo, un histograma de días de resolución
        fig_hist = px.histogram(df_promedio, x='Dias_Resolucion', nbins=30, title="Distribución de Días de Resolución")
        st.plotly_chart(fig_hist, use_container_width=True)

    # 6. Cantidad de pases por mes en "Legales"
    df_pases_legales['Mes'] = df_pases_legales['Fecha ingreso'].dt.to_period('M').astype(str)
    df_pases_mes = df_pases_legales.groupby('Mes').size().reset_index(name='Cantidad')
    fig_pases_mes = px.bar(df_pases_mes, x='Mes', y='Cantidad', text='Cantidad', title="Pases por Mes en 'Legales'")

    st.subheader("Cantidad de pases por mes en 'Legales'")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df_pases_mes)
    with col2:
        st.plotly_chart(fig_pases_mes, use_container_width=True)

    # ---- Expanders para detalles ----
    with st.expander("Mostrar tabla detallada: Expedientes filtrados"):
        st.dataframe(df_exp_filtrado)

    with st.expander("Mostrar tabla detallada: Pases filtrados"):
        st.dataframe(df_pases_filtrado)

    with st.expander("Detalles: Promedio de días para primer pase en 'Legales'"):
        st.dataframe(df_promedio[['Nro. Expediente', 'Tipo Expediente', 'Fecha inicio', 'Fecha ingreso_pase', 'Dias_Resolucion']])

else:
    st.info("Use los filtros en la barra lateral y presione 'Consultar' para mostrar el reporte.")