import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Red Neuronal Tributaria - Ecuador 🇪🇨",
    page_icon="🧠",
    layout="wide",
)

# --- CRÉDITO OBLIGATORIO ---
DEVELOPER_NAME = "Jonathan Toasa"

# Estilos CSS personalizados para simular las 4 capas de la red neuronal
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; color: #1f77b4; font-weight: 800; text-align: center; }
    .sub-title { font-size: 1.1rem; color: #555; text-align: center; margin-bottom: 30px; }
    .layer-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; height: 100%; }
    .layer-1 { border-top: 5px solid #1f77b4; }
    .layer-2 { border-top: 5px solid #9467bd; }
    .layer-3 { border-top: 5px solid #2ca02c; }
    .layer-4 { border-top: 5px solid #d62728; }
    .metric-box { background-color: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">🧠 Red Neuronal del IVA y del Impuesto a la Renta</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<p class="sub-title">Modelo Predictivo e Interactivo Basado en el SRI y LORTI • Desarrollado por <b>{DEVELOPER_NAME}</b></p>',
    unsafe_allow_html=True,
)

# --- DISTRIBUCIÓN EN 4 CAPAS (ESTILO ARQUITECTURA NEURONAL) ---
col_l1, col_l2, col_l3, col_l4 = st.columns(4)

with col_l1:
    st.markdown(
        """
        <div class="layer-card layer-1">
            <h3>1️⃣ CAPA DE ENTRADA</h3>
            <p style="font-size:0.85rem; color:#666;">Datos del negocio y transacciones</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    ventas_mes = st.number_input(
        "Ventas del Mes (USD sin IVA)", min_value=0.0, value=10000.0, step=500.0
    )
    compras_mes = st.number_input(
        "Compras del Mes (USD sin IVA)", min_value=0.0, value=6000.0, step=500.0
    )
    tipo_tarifa = st.selectbox(
        "Tarifa IVA Aplicable", [15.0, 5.0, 0.0], index=0
    )
    retenciones_recibidas = st.number_input(
        "Retenciones Recibidas (IVA + Renta)",
        min_value=0.0,
        value=1290.0,
        step=50.0,
    )
    ingresos_anual = st.number_input(
        "Ingresos del Año (Proyectados)",
        min_value=0.0,
        value=200000.0,
        step=5000.0,
    )
    costos_anual = st.number_input(
        "Costos y Gastos Deducibles",
        min_value=0.0,
        value=160000.0,
        step=5000.0,
    )

with col_l2:
    st.markdown(
        """
        <div class="layer-card layer-2">
            <h3>2️⃣ CLASIFICACIÓN</h3>
            <p style="font-size:0.85rem; color:#666;">Aplica la normativa legal</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    hecho_generador = st.checkbox("¿Hecho generador válido?", value=True)
    comprobante_valido = st.checkbox(
        "¿Comprobante autorizado por el SRI?", value=True
    )
    tipo_contribuyente = st.selectbox(
        "Tipo de Contribuyente",
        ["Sociedad / Persona Jurídica", "Persona Natural"],
    )
    st.info(
        "⚖️ **Filtros de Ley:**\n- Art. 61 LORTI (Hecho Generador)\n- Art. 65 Tarifa General\n- Art. 55-56 Exoneraciones"
    )

with col_l3:
    st.markdown(
        """
        <div class="layer-card layer-3">
            <h3>3️⃣ CAPA DE CÁLCULO</h3>
            <p style="font-size:0.85rem; color:#666;">Operaciones y ponderación (Pesos)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Neuronas de cálculo internas con pesos ponderados
    iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
    credito_tributario = compras_mes * (tipo_tarifa / 100.0)
    iva_retenido = retenciones_recibidas * 0.07  # proporción estimada
    base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
    tarifa_renta_sociedad = 0.25 if "Sociedad" in tipo_contribuyente else 0.20
    renta_retenida = 1200.0

    st.markdown(
        f"""
        <div class="metric-box">
        <b>IVA Ventas (×{tipo_tarifa/100}):</b><br>${iva_en_ventas:,.2f}
        </div>
        <div class="metric-box">
        <b>Crédito Tributario:</b><br>${credito_tributario:,.2f}
        </div>
        <div class="metric-box">
        <b>Base Imponible Renta:</b><br>${base_imponible_renta:,.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_l4:
    st.markdown(
        """
        <div class="layer-card layer-4">
            <h3>4️⃣ CAPA DE SALIDA</h3>
            <p style="font-size:0.85rem; color:#666;">Resultado fiscal y plazos</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Resultados finales de la red
    iva_pagar_calc = iva_en_ventas - crédito_tributario - iva_retenido
    iva_a_pagar = max(0.0, iva_pagar_calc)
    iva_a_favor = abs(min(0.0, iva_pagar_calc))

    impuesto_causado_renta = base_imponible_renta * tarifa_renta_sociedad
    renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

    st.markdown(
        f"""
        <div class="metric-box" style="border-left: 4px solid #d62728;">
        <b>IVA A PAGAR:</b><br><span style="color:red; font-size:1.2rem;"><b>${iva_a_pagar:,.2f}</b></span>
        </div>
        <div class="metric-box" style="border-left: 4px solid #2ca02c;">
        <b>CRÉDITO A FAVOR:</b><br><span style="color:green; font-size:1.2rem;"><b>${iva_a_favor:,.2f}</b></span>
        </div>
        <div class="metric-box" style="border-left: 4px solid #d62728;">
        <b>RENTA A PAGAR:</b><br><span style="color:red; font-size:1.2rem;"><b>${renta_a_pagar:,.2f}</b></span>
        </div>
        <div class="metric-box">
        <b>PLAZO DE DECLARACIÓN:</b><br>Día 14 <span style="font-size:0.8rem;">(9.° dígito RUC)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- RESUMEN DE ECUACIONES Y MATRIZ DE PONDERACIÓN ---
st.subheader("📋 Matriz de Ecuaciones y Trazabilidad Neuronal (SRI)")
col_eq1, col_eq2 = st.columns(2)

with col_eq1:
    st.markdown(
        f"""
    **Flujo del IVA:**
    * $\\text{{IVA Ventas}} = \\text{{Ventas}} \\times {tipo_tarifa\\%}} = \\${iva_en_ventas:,.2f}$
    * $\\text{{IVA a Pagar}} = \\text{{IVA Ventas}} - \\text{{Crédito Tributario}} - \\text{{IVA Retenido}} = \\mathbf{{\\${iva_a_pagar:,.2f}}}$
    """
    )

with col_eq2:
    st.markdown(
        f"""
    **Flujo del Impuesto a la Renta:**
    * $\\text{{Base Imponible}} = \\text{{Ingresos}} - \\text{{Costos}} = \\${base_imponible_renta:,.2f}$
    * $\\text{{Renta a Pagar}} = (\\text{{Base}} \\times {tarifa_renta_sociedad*100}\\%) - \\text{{Retenciones}} = \\mathbf{{\\${renta_a_pagar:,.2f}}}$
    """
    )

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray;'>Red Neuronal Interactiva • Desarrollado por {DEVELOPER_NAME}</p>",
    unsafe_allow_html=True,
)
    
    
