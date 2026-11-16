import html
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------
st.set_page_config(
    page_title="Red Neuronal del IVA y del Impuesto a la Renta",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEVELOPER_NAME = "Jonathan Toasa"

# ------------------------------------------------------------
# ESTILOS GENERALES
# ------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: #0b1224;
        color: #e8eefc;
    }
    [data-testid="stSidebar"] {
        background: #111b32;
        border-right: 1px solid rgba(148, 163, 184, .16);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #eaf0ff;
    }
    .main-title {
        color: #f3f6ff;
        font-size: clamp(1.65rem, 3vw, 2.45rem);
        font-weight: 800;
        line-height: 1.15;
        margin: 0;
        letter-spacing: -.5px;
    }
    .sub-title {
        color: #a9b9d8;
        font-size: 1rem;
        margin-top: 8px;
        margin-bottom: 0;
    }
    .author {
        color: #c4d2ef;
        text-align: right;
        font-size: .88rem;
        line-height: 1.55;
    }
    .top-rule {
        height: 4px;
        border-radius: 10px;
        background: linear-gradient(90deg, #3977ff, #a855f7, #13b8a6, #ef4444);
        margin: 20px 0 18px 0;
    }
    .result-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin-top: 14px;
    }
    .result-box {
        background: #17233c;
        border: 1px solid rgba(148,163,184,.18);
        border-radius: 11px;
        padding: 12px 14px;
    }
    .result-label {
        color: #9fb1d2;
        font-size: .72rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: .5px;
    }
    .result-value {
        color: #f7f9ff;
        font-size: 1.22rem;
        font-weight: 800;
        margin-top: 3px;
    }
    .footnote {
        color: #8292b2;
        text-align: center;
        font-size: .78rem;
        margin-top: 18px;
    }
    @media (max-width: 750px) {
        .result-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# CASOS DE EJEMPLO Y CONTROLES
# ------------------------------------------------------------
st.sidebar.markdown("## ⚙️ Casos de ejemplo y controles")
caso = st.sidebar.selectbox(
    "Seleccionar escenario:",
    [
        "Comercial Los Andes S.A. (Caso Base)",
        "Tienda tarifa 0% / Crédito a favor",
        "Persona natural – Servicios profesionales",
    ],
)

if "Los Andes" in caso:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        10000.0, 6000.0, 15.0, 1290.0, 200000.0, 160000.0
    )
elif "0%" in caso:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        5000.0, 8000.0, 0.0, 200.0, 80000.0, 70000.0
    )
else:
    v_def, c_def, t_def, ret_def, ing_def, cos_def = (
        15000.0, 2000.0, 15.0, 1500.0, 120000.0, 40000.0
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Parámetros de entrada")
ventas_mes = st.sidebar.number_input(
    "Ventas del mes (USD sin IVA)", min_value=0.0, value=float(v_def), step=500.0
)
compras_mes = st.sidebar.number_input(
    "Compras del mes (USD sin IVA)", min_value=0.0, value=float(c_def), step=500.0
)
tipo_tarifa = st.sidebar.selectbox(
    "Tarifa IVA aplicable",
    [15.0, 5.0, 0.0],
    index=[15.0, 5.0, 0.0].index(float(t_def)),
    format_func=lambda x: f"{x:g} %",
)
retenciones_recibidas = st.sidebar.number_input(
    "Retenciones recibidas (total)",
    min_value=0.0, value=float(ret_def), step=50.0
)
ingresos_anual = st.sidebar.number_input(
    "Ingresos del año (USD)", min_value=0.0, value=float(ing_def), step=5000.0
)
costos_anual = st.sidebar.number_input(
    "Costos y gastos deducibles (USD)",
    min_value=0.0, value=float(cos_def), step=5000.0
)
st.sidebar.caption("Los valores se actualizan automáticamente al modificar los campos.")

# ------------------------------------------------------------
# CÁLCULOS ORIGINALES DEL PROGRAMA
# Se conservan las fórmulas del archivo entregado.
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# FUNCIONES AUXILIARES PARA EL DIAGRAMA SVG
# ------------------------------------------------------------
def money(value):
    return f"${value:,.2f}"

def svg_text(x, y, text, size=11, color="#eaf0ff", weight="500",
             anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{html.escape(str(text))}</text>'
    )

def node(x, y, title, value, color, subtitle="", radius=27):
    # Nodo circular con halo, borde y etiqueta de valor.
    parts = [
        f'<circle cx="{x}" cy="{y}" r="{radius+5}" fill="{color}" opacity=".10"/>',
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#17243e" '
        f'stroke="{color}" stroke-width="2.5"/>',
    ]
    lines = title.split("|")
    start_y = y - (len(lines)-1)*5
    for i, line in enumerate(lines):
        parts.append(svg_text(x, start_y + i*10 + 3, line, 8.5, "#ffffff", "800"))
    # Valor en una pequeña cápsula encima del nodo.
    label = str(value)
    pill_w = max(42, min(104, 12 + len(label)*6.2))
    parts.append(
        f'<rect x="{x-pill_w/2}" y="{y-radius-17}" width="{pill_w}" height="16" '
        f'rx="8" fill="#ffd65a"/>'
    )
    parts.append(svg_text(x, y-radius-5, label, 9, "#392b08", "800"))
    if subtitle:
        parts.append(svg_text(x, y+radius+15, subtitle, 8, "#aebddb", "500"))
    return "".join(parts)

# ------------------------------------------------------------
# CONSTRUCCIÓN DE LAS CUATRO CAPAS
# ------------------------------------------------------------
W, H = 1240, 730
layer_x = [155, 465, 775, 1085]
layer_colors = ["#3977f6", "#b34be8", "#0fb7a5", "#ef5148"]
layer_bg = ["#142b53", "#321d49", "#103b38", "#421f27"]
layer_titles = [
    ("1", "CAPA DE ENTRADA", "Datos del negocio"),
    ("2", "CAPA DE CLASIFICACIÓN", "Aplica la ley"),
    ("3", "CAPA DE CÁLCULO", "Opera con pesos"),
    ("4", "CAPA DE SALIDA", "Resultado fiscal"),
]
panel_x = [12, 322, 632, 942]
panel_w = 286

# Nodos por capa. Cada nodo muestra el dato calculado en tiempo real.
input_nodes = [
    ("VENTAS|DEL MES", money(ventas_mes), "valor sin IVA"),
    ("COMPRAS|DEL MES", money(compras_mes), "valor sin IVA"),
    ("TIPO DE|BIEN O SERVICIO", f"{tipo_tarifa:g} %", "tarifa seleccionada"),
    ("RETENCIONES|RECIBIDAS", money(retenciones_recibidas), "valores ingresados"),
    ("INGRESOS|DEL AÑO", money(ingresos_anual), "ingresos gravados"),
    ("COSTOS Y GASTOS|DEDUCIBLES", money(costos_anual), "permitidos en el modelo"),
]
class_nodes = [
    ("HECHO|GENERADOR", "SÍ", "Art. 61"),
    ("TARIFA DE|IVA APLICABLE", f"{tipo_tarifa:g} %", "Art. 65"),
    ("APLICA|TARIFA 0 %", "SÍ" if tipo_tarifa == 0 else "NO", "según selección"),
    ("COMPROBANTE|VÁLIDO", "SÍ", "supuesto del modelo"),
    ("TIPO DE|CONTRIBUYENTE", "SOC.", "sociedad / persona natural"),
]
calc_nodes = [
    ("IVA EN|VENTAS", money(iva_en_ventas), "ventas × tarifa"),
    ("CRÉDITO|TRIBUTARIO", money(credito_tributario), "compras × tarifa"),
    ("IVA|RETENIDO", money(iva_retenido), "retenciones × 7 %"),
    ("BASE|IMPONIBLE RENTA", money(base_imponible_renta), "ingresos − costos"),
    ("RENTA|RETENIDA", money(retenciones_recibidas * 0.9), "retenciones × 90 %"),
]
out_nodes = [
    ("IVA A|PAGAR", money(iva_a_pagar), "resultado positivo"),
    ("CRÉDITO|A FAVOR", money(iva_a_favor), "si el saldo es negativo"),
    ("RENTA A|PAGAR", money(renta_a_pagar), "impuesto menos retención"),
    ("PLAZO DE|DECLARACIÓN", "DÍA 14", "ejemplo: 9.° dígito RUC"),
]

layers = [input_nodes, class_nodes, calc_nodes, out_nodes]
ys = [
    [125, 225, 325, 425, 525, 625],
    [165, 275, 385, 495, 605],
    [145, 255, 365, 475, 585],
    [190, 330, 470, 610],
]

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'width="100%" role="img" aria-label="Diagrama de red neuronal tributaria">',
    '<defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
    '<rect x="0" y="0" width="1240" height="730" rx="18" fill="#0d172c"/>',
]

# Paneles de fondo para cada capa.
for i in range(4):
    svg.append(
        f'<rect x="{panel_x[i]}" y="12" width="{panel_w}" height="700" '
        f'rx="19" fill="{layer_bg[i]}" opacity=".82" '
        f'stroke="{layer_colors[i]}" stroke-opacity=".22"/>'
    )
    num, title, subtitle = layer_titles[i]
    svg.append(
        f'<circle cx="{panel_x[i]+25}" cy="39" r="12" fill="{layer_colors[i]}"/>'
    )
    svg.append(svg_text(panel_x[i]+25, 43, num, 11, "#fff", "800"))
    svg.append(svg_text(panel_x[i]+45, 36, title, 11, layer_colors[i], "800", "start"))
    svg.append(svg_text(panel_x[i]+45, 51, subtitle, 9, "#aebddb", "500", "start"))

# Conexiones suaves entre todos los nodos de capas adyacentes.
for layer_index in range(3):
    for y1 in ys[layer_index]:
        for y2 in ys[layer_index+1]:
            svg.append(
                f'<line x1="{layer_x[layer_index]+28}" y1="{y1}" '
                f'x2="{layer_x[layer_index+1]-28}" y2="{y2}" '
                f'stroke="#8294b7" stroke-width="1" opacity=".15"/>'
            )

# Conexiones principales coloreadas que representan el flujo del cálculo.
active_edges = [
    (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 1, 1),
    (0, 2, 1, 1), (0, 3, 1, 3), (0, 4, 1, 4),
    (0, 5, 1, 4),
    (1, 0, 2, 0), (1, 1, 2, 0), (1, 1, 2, 1),
    (1, 3, 2, 1), (1, 3, 2, 2), (1, 4, 2, 3),
    (1, 4, 2, 4),
    (2, 0, 3, 0), (2, 1, 3, 0), (2, 2, 3, 0),
    (2, 3, 3, 2), (2, 4, 3, 2),
]
for a, ia, b, ib in active_edges:
    y1, y2 = ys[a][ia], ys[b][ib]
    color = layer_colors[b]
    svg.append(
        f'<line x1="{layer_x[a]+28}" y1="{y1}" '
        f'x2="{layer_x[b]-28}" y2="{y2}" '
        f'stroke="{color}" stroke-width="2.2" opacity=".88" '
        f'stroke-dasharray="7 5"/>'
    )

# Etiquetas pequeñas de pesos entre capas.
for x, y, label, color in [
    (310, 245, "LEY", "#b34be8"),
    (620, 310, "TARIFA", "#0fb7a5"),
    (930, 385, "RESULTADO", "#ef5148"),
]:
    svg.append(
        f'<rect x="{x-34}" y="{y-10}" width="68" height="20" rx="9" '
        f'fill="{color}" opacity=".95"/>'
    )
    svg.append(svg_text(x, y+3, label, 8, "#fff", "800"))

# Nodos.
for layer_index, layer in enumerate(layers):
    for node_index, item in enumerate(layer):
        title, value, subtitle = item
        svg.append(
            node(layer_x[layer_index], ys[layer_index][node_index],
                 title, value, layer_colors[layer_index], subtitle)
        )

svg.append("</svg>")
svg_markup = "".join(svg)

# ------------------------------------------------------------
# ENCABEZADO Y PRESENTACIÓN
# ------------------------------------------------------------
left, right = st.columns([4, 1.35], vertical_alignment="center")
with left:
    st.markdown(
        '<p class="main-title">🧠 Red neuronal del IVA y del Impuesto a la Renta</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Escribe los datos de un negocio y observa cómo '
        'la red los clasifica, procesa y transforma en resultados tributarios.</p>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f'<div class="author"><b>{DEVELOPER_NAME}</b><br>'
        'NRC 34801 · Contabilidad I · ESPE<br>'
        'Ecuador · Modelo educativo</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)

# El diagrama se genera como SVG para que las líneas y nodos permanezcan
# nítidos al ampliar o reducir la ventana del navegador.
components.html(
    f"""
    <div style="width:100%; overflow-x:auto; background:#0d172c; border-radius:18px;">
        {svg_markup}
    </div>
    """,
    height=755,
    scrolling=False,
)

# ------------------------------------------------------------
# RESUMEN DE RESULTADOS
# ------------------------------------------------------------
st.markdown("### 📊 Resumen de resultados")
st.markdown(
    f"""
    <div class="result-strip">
        <div class="result-box">
            <div class="result-label">IVA a pagar</div>
            <div class="result-value">{money(iva_a_pagar)}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Crédito a favor</div>
            <div class="result-value">{money(iva_a_favor)}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Renta a pagar</div>
            <div class="result-value">{money(renta_a_pagar)}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Base imponible de renta</div>
            <div class="result-value">{money(base_imponible_renta)}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="footnote">Modelo educativo con las fórmulas del código original. '
    'Los resultados dependen de los datos ingresados y de los supuestos programados. '
    f'· Desarrollado por {DEVELOPER_NAME}</p>',
    unsafe_allow_html=True,
)
