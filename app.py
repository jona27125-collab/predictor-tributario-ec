import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Predictor Tributario y Flujo de Caja - SRI Ecuador",
    page_icon="📊",
    layout="wide",
)

# --- CRÉDITO OBLIGATORIO ---
DEVELOPER_NAME = "Jonathan Daniel Toasa Quinga"

# Estilo visual personalizado (CSS limpio)
st.markdown(
    """
    <style>
    .main-header { font-size: 2.2rem; color: #1f77b4; font-weight: 700; }
    .sub-header { font-size: 1.2rem; color: #555555; margin-bottom: 25px; }
    .credit-tag { background-color: #f0f2f6; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #333; border-left: 5px solid #1f77b4; }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado principal
st.markdown(
    '<p class="main-header">ecuadorFin-IA: Predictor Tributario & Flujo de Caja 🇪🇨</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="credit-tag">Desarrollado por {DEVELOPER_NAME}</div>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.markdown(
    f"### ⚙️ Panel de Configuración\n**Desarrollado por {DEVELOPER_NAME}**"
)
st.sidebar.markdown("---")

regimen_fiscal = st.sidebar.selectbox(
    "Seleccione su Régimen Tributario (SRI):",
    [
        "RIMPE Emprendedor",
        "Régimen General",
        "RIMPE Negocio Popular (Cuota Fija)",
    ],
)

st.sidebar.markdown("### 🎛️ Simulación de Factores Macroeconómicos")
factor_crecimiento = (
    st.sidebar.slider("Crecimiento Esperado de Ventas (%)", -20.0, 50.0, 5.0)
    / 100.0
)
inflacion_gastos = (
    st.sidebar.slider("Ajuste en Costos Operativos (%)", -10.0, 30.0, 2.0) / 100.0
)

# --- GENERACIÓN DE DATOS HISTÓRICOS REALISTAS (SRI / ECUADOR) ---
@st.cache_data
def generar_datos_historicos():
    np.random.seed(42)
    meses = pd.date_range(start="2023-01-01", end="2026-02-01", freq="MS")
    n = len(meses)

    # Tendencia estacional con crecimiento base
    tendencia = np.linspace(10000, 22000, n)
    ruido = np.random.normal(0, 1500, n)
    estacionalidad = 2000 * np.sin(np.linspace(0, 3 * np.pi, n))

    ventas = np.clip(tendencia + ruido + estacionalidad, 5000, None)
    costos = ventas * np.random.uniform(0.55, 0.70, n)

    # IVA (Tarifa general 15% vigente)
    iva_cobrado = ventas * 0.15
    iva_pagado = costos * 0.15

    df = pd.DataFrame(
        {
            "Fecha": meses,
            "Mes_Num": np.arange(1, n + 1),
            "Ventas_Brutas": ventas,
            "Costos_Gastos": costos,
            "IVA_Cobrado": iva_cobrado,
            "IVA_Pagado": iva_pagado,
        }
    )
    df["Flujo_Neto"] = df["Ventas_Brutas"] - df["Costos_Gastos"]
    return df


df_historico = generar_datos_historicos()

# --- ENTRENAMIENTO DE LA RED NEURONAL (Scikit-Learn MLPRegressor) ---
@st.cache_resource
def entrenar_modelo(df):
    X = df[["Mes_Num", "Ventas_Brutas", "Costos_Gastos"]]
    y = df[["Flujo_Neto", "IVA_Cobrado", "IVA_Pagado"]]

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # Red Neuronal Multicapa (MLP)
    mlp = MLPRegressor(
        hidden_layer_sizes=(32, 16),
        activation="relu",
        solver="adam",
        max_iter=1000,
        random_state=42,
    )
    mlp.fit(X_scaled, y_scaled)

    return mlp, scaler_X, scaler_y


modelo, scaler_X, scaler_y = entrenar_modelo(df_historico)

# --- PREDICCIÓN PARA LOS PRÓXIMOS 6 MESES ---
ult_mes_num = df_historico["Mes_Num"].max()
ult_ventas = df_historico["Ventas_Brutas"].iloc[-1]
ult_costos = df_historico["Costos_Gastos"].iloc[-1]

futuras_fechas = pd.date_range(
    start=df_historico["Fecha"].iloc[-1] + pd.DateOffset(months=1),
    periods=6,
    freq="MS",
)
proyecciones = []

curr_ventas = ult_ventas
curr_costos = ult_costos

for i, fecha in enumerate(futuras_fechas):
    m_num = ult_mes_num + i + 1
    # Aplicar factores simulados
    curr_ventas *= 1 + (factor_crecimiento / 6)
    curr_costos *= 1 + (inflacion_gastos / 6)

    # Predicción con la Red Neuronal
    X_pred = scaler_X.transform([[m_num, curr_ventas, curr_costos]])
    y_pred_scaled = modelo.predict(X_pred)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)[0]

    flujo_neto_pred = y_pred[0]
    iva_cob_pred = y_pred[1]
    iva_pag_pred = y_pred[2]

    # Lógica Tributaria SRI Ecuador
    iva_por_pagar = max(0, iva_cob_pred - iva_pag_pred)

    # Cálculo Impuesto a la Renta estimado
    utilidad_estimada = curr_ventas - curr_costos
    if regimen_fiscal == "RIMPE Emprendedor":
        # Tasa progresiva estimada sobre ingresos brutos o utilidad simplificada (ej. 1% a 2% sobre ingresos o tabla progresiva)
        impuesto_renta = curr_ventas * 0.02
    elif regimen_fiscal == "RIMPE Negocio Popular (Cuota Fija)":
        impuesto_renta = 60.0 / 12  # Cuota anual fija prorrateada mensual
    else:  # Régimen General
        impuesto_renta = max(0, utilidad_estimada * 0.25)

    proyecciones.append(
        {
            "Fecha": fecha,
            "Ventas Proyectadas": curr_ventas,
            "Costos Proyectados": curr_costos,
            "Flujo Neto Proyectado": flujo_neto_pred,
            "IVA a Pagar (SRI)": iva_por_pagar,
            "Impuesto a la Renta Estimado": impuesto_renta,
        }
    )

df_proyeccion = pd.DataFrame(proyecciones)

# --- DASHBOARD / INTERFAZ PRINCIPAL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Promedio Ingresos Mensuales (Proyectados)",
        value=f"${df_proyeccion['Ventas Proyectadas'].mean():,.2f}",
        delta=f"{factor_crecimiento*100:.1f}% simulación",
    )

with col2:
    st.metric(
        label="IVA Promedio Mensual a Pagar (SRI 15%)",
        value=f"${df_proyeccion['IVA a Pagar (SRI)'].mean():,.2f}",
    )

with col3:
    st.metric(
        label="Renta Estimada Promedio / Mes",
        value=f"${df_proyeccion['Impuesto a la Renta Estimado'].mean():,.2f}",
        delta=regimen_fiscal,
    )

st.markdown("---")

# Gráficos Interactivos con Plotly
st.subheader("📈 Proyección de Flujo de Caja Neto (Histórico vs IA)")

fig_flujo = go.Figure()
fig_flujo.add_trace(
    go.Scatter(
        x=df_historico["Fecha"],
        y=df_historico["Flujo_Neto"],
        name="Histórico Real",
        line=dict(color="#1f77b4", width=2),
    )
)
fig_flujo.add_trace(
    go.Scatter(
        x=df_proyeccion["Fecha"],
        y=df_proyeccion["Flujo Neto Proyectado"],
        name="Proyección Red Neuronal (MLP)",
        line=dict(color="#2ca02c", width=3, dash="dash"),
    )
)
fig_flujo.update_layout(
    xaxis_title="Fecha",
    yaxis_title="USD ($)",
    hovermode="x unified",
    template="plotly_white",
)
st.plotly_chart(fig_flujo, use_container_width=True)

# Sección de Obligaciones Tributarias
st.subheader("🧾 Obligaciones Tributarias Proyectadas (IVA & Impuesto a la Renta)")

col_g1, col_g2 = st.columns(2)

with col_g1:
    fig_iva = px.bar(
        df_proyeccion,
        x="Fecha",
        y="IVA a Pagar (SRI)",
        title="IVA Neto a Declarar por Mes (15%)",
        color_discrete_sequence=["#ff7f0e"],
    )
    fig_iva.update_layout(template="plotly_white")
    st.plotly_chart(fig_iva, use_container_width=True)

with col_g2:
    fig_renta = px.bar(
        df_proyeccion,
        x="Fecha",
        y="Impuesto a la Renta Estimado",
        title=f"Proyección Impuesto a la Renta ({regimen_fiscal})",
        color_discrete_sequence=["#d62728"],
    )
    fig_renta.update_layout(template="plotly_white")
    st.plotly_chart(fig_renta, use_container_width=True)

# Tabla de Datos Detallados
with st.expander("🔍 Ver Detalle Numérico de Proyecciones"):
    df_display = df_proyeccion.copy()
    for col in df_display.columns[1:]:
        df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
    st.dataframe(df_display, use_container_width=True)

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray;'>Plataforma Tributaria Inteligente • Desarrollado por {DEVELOPER_NAME}</p>",
    unsafe_allow_html=True,
)