import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Red Neuronal del IVA y del Impuesto a la Renta",
    page_icon="🧠",
    layout="wide",
)

# --- CRÉDITO OBLIGATORIO ---
DEVELOPER_NAME = "Jonathan Toasa"

# Estilos CSS
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; color: #ffffff; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size: 1rem; color: #b0b0b0; text-align: center; margin-bottom: 25px; }
    .stMetric { background-color: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
    </style>
""",
    unsafe_allow_html=True,
)

# Título Principal
st.markdown(
    '<p class="main-title">🧠 Red Neuronal del IVA y del Impuesto a la Renta</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<p class="sub-title">Práctico-experimental • Modelo Predictivo'
    f' Interactivo (SRI & LORTI) • Desarrollado por'
    f' <b>{DEVELOPER_NAME}</b></p>',
    unsafe_allow_html=True,
)

# --- PANEL DE CONTROL LATERAL ---
st.sidebar.markdown("### ⚙️ Casos de Ejemplo y Controles")
caso = st.sidebar.selectbox(
    "Seleccionar Escenario:",
    [
        "Comercial Los Andes S.A. (Caso Base)",
        "Tienda Tarifa 0% / Crédito a Favor",
        "Persona Natural Servicios Profesionales",
    ],
)

if "Los Andes" in caso:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        10000.0,
        6000.0,
        15.0,
        1290.0,
        200000.0,
        160000.0,
    )
elif "0%" in caso:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        5000.0,
        8000.0,
        0.0,
        200.0,
        80000.0,
        70000.0,
    )
else:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        15000.0,
        2000.0,
        15.0,
        1500.0,
        120000.0,
        40000.0,
    )

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📥 Parámetros de Entrada")
ventas_mes = st.sidebar.number_input(
    "Ventas del Mes (USD sin IVA)", value=v_def, step=500.0
)
compras_mes = st.sidebar.number_input(
    "Compras del Mes (USD sin IVA)", value=c_def, step=500.0
)
tipo_tarifa = st.sidebar.selectbox(
    "Tarifa IVA Aplicable", [15.0, 5.0, 0.0], index=0 if t_def == 15.0 else 2
)
retenciones_recibidas = st.sidebar.number_input(
    "Retenciones Recibidas (Total)", value=ret_def, step=50.0
)
ingresos_anual = st.sidebar.number_input(
    "Ingresos del Año", value=ing_def, step=5000.0
)
costos_anual = st.sidebar.number_input(
    "Costos y Gastos Deducibles", value=cos_def, step=5000.0
)

# --- CÁLCULOS MATEMÁTICOS ---
iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = compras_mes * (tipo_tarifa / 100.0)
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))

base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_a_pagar = max(
    0.0, impuesto_causado_renta - (retenciones_recibidas * 0.9)
)

# --- VISTA PRINCIPAL: 4 CAPAS NEURONALES EN COLUMNAS ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("### 1️⃣ CAPA DE ENTRADA\n*Datos del negocio*")
    st.metric("Ventas del Mes", f"${ventas_mes:,.2f}")
    st.metric("Compras del Mes", f"${compras_mes:,.2f}")
    st.metric("Tarifa Aplicable", f"{tipo_tarifa}%")
    st.metric("Retenciones", f"${retenciones_recibidas:,.2f}")
    st.metric("Ingresos Año", f"${ingresos_anual:,.2f}")

with c2:
    st.warning("### 2️⃣ CLASIFICACIÓN\n*Aplica la ley*")
    st.metric("Hecho Generador", "SÍ (Art. 61)")
    st.metric("Tarifa IVA", f"{tipo_tarifa}% (Art. 65)")
    st.metric("Exoneración 0%", "SÍ" if tipo_tarifa == 0 else "NO")
    st.metric("Comprobante", "Válido (SRI)")
    st.metric("Contribuyente", "Sociedad / Jurídica")

with c3:
    st.success("### 3️⃣ CAPA DE CÁLCULO\n*Opera con pesos*")
    st.metric("IVA en Ventas", f"${iva_en_ventas:,.2f}")
    st.metric("Crédito Tributario", f"${credito_tributario:,.2f}")
    st.metric("IVA Retenido", f"${iva_retenido:,.2f}")
    st.metric("Base Imponible Renta", f"${base_imponible_renta:,.2f}")

with c4:
    st.error("### 4️⃣ CAPA DE SALIDA\n*Resultado fiscal*")
    st.metric("IVA A PAGAR", f"${iva_a_pagar:,.2f}")
    st.metric("Crédito a Favor", f"${iva_a_favor:,.2f}")
    st.metric("Renta a Pagar", f"${renta_a_pagar:,.2f}")
    st.metric("Plazo Declaración", "Día 14 (9.° RUC)")

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 0.85rem;'>Modelo"
    f" educativo basado en LORTI y SRI (2026) • Desarrollado por"
    f" {DEVELOPER_NAME}</p>",
    unsafe_allow_html=True,
)
