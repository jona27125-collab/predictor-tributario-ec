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

# Estilos CSS avanzados para replicar el diseño de la red neuronal de 4 capas
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; color: #ffffff; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size: 1rem; color: #b0b0b0; text-align: center; margin-bottom: 25px; }
    
    /* Contenedores de Capas */
    .layer-box { border-radius: 12px; padding: 15px; margin-bottom: 15px; color: white; }
    .layer-1 { background-color: #1a365d; border-left: 6px solid #3182ce; }
    .layer-2 { background-color: #44337a; border-left: 6px solid #805ad5; }
    .layer-3 { background-color: #1c4532; border-left: 6px solid #38a169; }
    .layer-4 { background-color: #581c1c; border-left: 6px solid #e53e3e; }
    
    /* Nodos Neuronales Estilizados */
    .neuron { background: rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px; margin: 8px 0; border: 1px solid rgba(255,255,255,0.15); }
    .badge-val { background-color: #ecc94b; color: #1a202c; font-weight: bold; padding: 2px 8px; border-radius: 12px; float: right; font-size: 0.85rem; }
    
    /* Panel lateral de casos */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; }
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
    f'<p class="sub-title">Práctico-experimental • Modelo Predictivo Interactivo (SRI & LORTI) • Desarrollado por <b>{DEVELOPER_NAME}</b></p>',
    unsafe_allow_html=True,
)

# --- PANEL DE CONTROL LATERAL (CASOS Y ENTRADAS) ---
st.sidebar.markdown("### ⚙️ Casos de Ejemplo y Controles")
caso = st.sidebar.selectbox(
    "Seleccionar Escenario:",
    [
        "Comercial Los Andes S.A. (Caso Base)",
        "Tienda Tarifa 0% / Crédito a Favor",
        "Persona Natural Servicios Profesionales",
    ],
)

# Definir valores según el caso
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

# --- CÁLCULOS MATEMÁTICOS DE LA RED ---
iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = compras_mes * (tipo_tarifa / 100.0)
iva_retenido = retenciones_recibidas * 0.07  # proporción ponderada
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

# CAPA 1: ENTRADA
with c1:
    st.markdown(
        """
        <div class="layer-box layer-1">
            <h4>1️⃣ CAPA DE ENTRADA</h4>
            <p style="font-size:0.8rem; color:#cbd5e0;">Datos del negocio</p>
            
            <div class="neuron">
                <b>VENTAS DEL MES</b><br><span style="font-size:0.75rem;">valor sin IVA</span>
                <span class="badge-val">%{v:,.0f}</span>
            </div>
            <div class="neuron">
                <b>COMPRAS DEL MES</b><br><span style="font-size:0.75rem;">valor sin IVA</span>
                <span class="badge-val">%{c:,.0f}</span>
            </div>
            <div class="neuron">
                <b>TARIFA APLICABLE</b><br><span style="font-size:0.75rem;">tipo de bien/servicio</span>
                <span class="badge-val">%{t}%</span>
            </div>
            <div class="neuron">
                <b>RETENCIONES</b><br><span style="font-size:0.75rem;">IVA y renta retenida</span>
                <span class="badge-val">%{r:,.0f}</span>
            </div>
            <div class="neuron">
                <b>INGRESOS AÑO</b><br><span style="font-size:0.75rem;">gravados del ejercicio</span>
                <span class="badge-val">%{i:,.0f}</span>
            </div>
        </div>
    """.format(
            v=ventas_mes,
            c=compras_mes,
            t=tipo_tarifa,
            r=retenciones_recibidas,
            i=ingresos_anual,
        ),
        unsafe_allow_html=True,
    )

# CAPA 2: CLASIFICACIÓN
with c2:
    st.markdown(
        """
        <div class="layer-box layer-2">
            <h4>2️⃣ CLASIFICACIÓN</h4>
            <p style="font-size:0.8rem; color:#e2e8f0;">Aplica la ley</p>
            
            <div class="neuron">
                <b>HECHO GENERADOR</b><br><span style="font-size:0.75rem;">Art. 61 LORTI</span>
                <span class="badge-val" style="background:#48bb78; color:white;">SÍ</span>
            </div>
            <div class="neuron">
                <b>TARIFA DE IVA</b><br><span style="font-size:0.75rem;">Art. 65 General</span>
                <span class="badge-val">%{t}%</span>
            </div>
            <div class="neuron">
                <b>EXONERACIÓN / 0%</b><br><span style="font-size:0.75rem
