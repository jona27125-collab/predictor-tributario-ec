import html
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# RED NEURONAL TRIBUTARIA
# Interfaz visual original para IVA e Impuesto a la Renta
# ============================================================

st.set_page_config(
    page_title="Red Neuronal Tributaria",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEVELOPER_NAME = "Jonathan Toasa"

# --------------------------- ESTILOS -------------------------
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(34, 76, 145, .20), transparent 38%),
            #080e1c;
        color: #eaf1ff;
    }
    [data-testid="stSidebar"] {
        background: #101a2d;
        border-right: 1px solid rgba(117, 151, 211, .18);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #edf3ff;
    }
    .hero {
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:18px;
        flex-wrap:wrap;
        padding: 8px 2px 16px 2px;
    }
    .hero-title {
        font-size:clamp(1.7rem, 3vw, 2.55rem);
        line-height:1.12;
        font-weight:850;
        letter-spacing:-.7px;
        margin:0;
        color:#f4f7ff;
    }
    .hero-sub {
        color:#9fb2d5;
        font-size:1rem;
        margin-top:9px;
        max-width:720px;
    }
    .hero-meta {
        color:#9fb2d5;
        font-size:.82rem;
        text-align:right;
        line-height:1.6;
    }
    .neon-rule {
        height:3px;
        border-radius:9px;
        background:linear-gradient(90deg,#3985ff,#9a5cff,#18d5bd,#ff9b45);
        box-shadow:0 0 16px rgba(74,125,255,.28);
        margin:8px 0 20px;
    }
    .section-label {
        color:#91a6ca;
        font-size:.72rem;
        font-weight:800;
        letter-spacing:1.4px;
        text-transform:uppercase;
        margin: 4px 0 10px;
    }
    .metric-grid {
        display:grid;
        grid-template-columns:repeat(4,minmax(0,1fr));
        gap:12px;
        margin-top:16px;
    }
    .metric-card {
        background:linear-gradient(145deg,#14223a,#101a2d);
        border:1px solid rgba(126,157,207,.20);
        border-radius:13px;
        padding:14px 16px;
        box-shadow:0 8px 24px rgba(0,0,0,.13);
    }
    .metric-name {
        color:#91a6ca;
        font-size:.72rem;
        font-weight:750;
        text-transform:uppercase;
        letter-spacing:.7px;
    }
    .metric-number {
        color:#f3f7ff;
        font-size:1.35rem;
        font-weight:850;
        margin-top:5px;
    }
    .hint {
        color:#8296b9;
        font-size:.8rem;
        margin-top:12px;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background:#17243a;
    }
    @media(max-width:850px) {
        .metric-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- PANEL DE ENTRADA ---------------------
st.sidebar.markdown("## ⚙️ Centro de control")
st.sidebar.caption("Introduce los datos para activar el procesamiento de la red.")
st.sidebar.markdown("---")
st.sidebar.markdown("### 01 · Datos del IVA")

ventas_mes = st.sidebar.number_input(
    "Ventas del mes (USD sin IVA)", min_value=0.0, value=0.0, step=100.0
)
compras_mes = st.sidebar.number_input(
    "Compras del mes (USD sin IVA)", min_value=0.0, value=0.0, step=100.0
)
tipo_tarifa = st.sidebar.selectbox(
    "Tarifa IVA aplicable",
    [15.0, 5.0, 0.0],
    index=0,
    format_func=lambda x: f"{x:g} %",
)
retenciones_recibidas = st.sidebar.number_input(
    "Retenciones recibidas (USD)", min_value=0.0, value=0.0, step=10.0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 02 · Datos del Impuesto a la Renta")

ingresos_anual = st.sidebar.number_input(
    "Ingresos del año (USD)", min_value=0.0, value=0.0, step=1000.0
)
costos_anual = st.sidebar.number_input(
    "Costos y gastos deducibles (USD)", min_value=0.0, value=0.0, step=1000.0
)

st.sidebar.markdown("---")
st.sidebar.caption("Los resultados y el diagrama se actualizan al cambiar los valores.")

# --------------------------- CÁLCULOS ------------------------
# Se mantienen las fórmulas del código original proporcionado.
iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = compras_mes * (tipo_tarifa / 100.0)
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))

base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_retenida = retenciones_recibidas * 0.9
renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

def fmt(n):
    return f"${n:,.2f}"

def safe(s):
    return html.escape(str(s))

# ----------------------- RED NEURONAL SVG --------------------
# Diagrama de flujo con nodos luminosos y enlaces curvos.
# Las posiciones forman una red orgánica, no cuatro tarjetas.
W, H = 1440, 790
svg = [f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%"
     role="img" aria-label="Red neuronal interactiva del proceso tributario">
<defs>
  <linearGradient id="lineGrad" x1="0" x2="1">
    <stop offset="0%" stop-color="#438cff"/>
    <stop offset="52%" stop-color="#a46aff"/>
    <stop offset="100%" stop-color="#1bd5bd"/>
  </linearGradient>
  <radialGradient id="core">
    <stop offset="0%" stop-color="#243c67"/>
    <stop offset="100%" stop-color="#101a2e"/>
  </radialGradient>
  <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="1440" height="790" rx="22" fill="#0a1427"/>
<g opacity=".18" stroke="#7894c5" stroke-width="1">
"""]

# Retícula técnica sutil.
for x in range(40, W, 40):
    svg.append(f'<path d="M{x} 0 V790"/>')
for y in range(30, H, 40):
    svg.append(f'<path d="M0 {y} H1440"/>')
svg.append('</g>')

# Cabeceras de las cuatro zonas de procesamiento.
zones = [
    (42,  "ENTRADA", "Datos ingresados", "#438cff"),
    (405, "ANÁLISIS", "Clasificación tributaria", "#b06cff"),
    (770, "PROCESAMIENTO", "Operaciones y cálculos", "#18cdb8"),
    (1135,"RESULTADOS", "Salida del sistema", "#ff9a54"),
]
for x, title, sub, color in zones:
    svg.append(f'<circle cx="{x+7}" cy="48" r="5" fill="{color}"/>')
    svg.append(f'<text x="{x+20}" y="52" fill="{color}" font-size="13" '
               f'font-weight="800" letter-spacing="1.5">{title}</text>')
    svg.append(f'<text x="{x+20}" y="70" fill="#8298bd" font-size="10">{sub}</text>')

# Coordenadas de los nodos por etapa.
input_nodes = [
    (105, 165, "VENTAS", fmt(ventas_mes), "IVA"),
    (105, 300, "COMPRAS", fmt(compras_mes), "IVA"),
    (105, 435, "TARIFA", f"{tipo_tarifa:g} %", "SELECCIÓN"),
    (105, 570, "RETENCIONES", fmt(retenciones_recibidas), "RECIBIDAS"),
    (105, 690, "INGRESOS / COSTOS", fmt(ingresos_anual), "RENTA"),
]
analysis_nodes = [
    (470, 205, "HECHO GENERADOR", "IVA", "REGLA"),
    (470, 390, "TARIFA APLICABLE", f"{tipo_tarifa:g} %", "CLASIFICACIÓN"),
    (470, 575, "BASE DE ANÁLISIS", "DATOS", "VALIDACIÓN"),
]
process_nodes = [
    (835, 165, "IVA EN VENTAS", fmt(iva_en_ventas), "VENTAS × TARIFA"),
    (835, 315, "CRÉDITO TRIBUTARIO", fmt(credito_tributario), "COMPRAS × TARIFA"),
    (835, 465, "IVA RETENIDO", fmt(iva_retenido), "RETENCIONES × 7 %"),
    (835, 635, "BASE IMPONIBLE", fmt(base_imponible_renta), "INGRESOS − COSTOS"),
]
output_nodes = [
    (1195, 205, "IVA A PAGAR", fmt(iva_a_pagar), "RESULTADO IVA"),
    (1195, 390, "CRÉDITO A FAVOR", fmt(iva_a_favor), "SALDO IVA"),
    (1195, 575, "RENTA A PAGAR", fmt(renta_a_pagar), "RESULTADO RENTA"),
]
all_nodes = [input_nodes, analysis_nodes, process_nodes, output_nodes]

# Conexiones de cada grupo hacia el siguiente con curvas Bezier.
def connect_groups(left, right, color, opacity=.56):
    for lx, ly, *_ in left:
        for rx, ry, *_ in right:
            mid = (lx + rx) / 2
            svg.append(
                f'<path d="M{lx+31} {ly} C{mid} {ly}, {mid} {ry}, {rx-39} {ry}" '
                f'fill="none" stroke="{color}" stroke-width="1.35" '
                f'opacity="{opacity}"/>'
            )

connect_groups(input_nodes, analysis_nodes, "#638fe8", .24)
connect_groups(analysis_nodes, process_nodes, "#a66be8", .36)
connect_groups(process_nodes, output_nodes, "#23cbb8", .38)

# Unas conexiones destacadas para dar sensación de flujo.
highlight_links = [
    (136,165,431,205,"#438cff"), (136,300,431,390,"#438cff"),
    (136,435,431,390,"#438cff"), (136,570,431,575,"#438cff"),
    (501,205,796,165,"#b06cff"), (501,390,796,315,"#b06cff"),
    (501,575,796,635,"#b06cff"), (866,165,1156,205,"#18cdb8"),
    (866,315,1156,205,"#18cdb8"), (866,465,1156,205,"#18cdb8"),
    (866,635,1156,575,"#18cdb8"),
]
for x1,y1,x2,y2,color in highlight_links:
    mid=(x1+x2)/2
    svg.append(
        f'<path d="M{x1} {y1} C{mid} {y1-18}, {mid} {y2+18}, {x2} {y2}" '
        f'fill="none" stroke="{color}" stroke-width="2.4" '
        f'stroke-dasharray="6 7" opacity=".95"/>'
    )

# Nodos: núcleo, anillo luminoso, texto y etiqueta de dato.
def draw_node(x, y, title, value, subtitle, color, radius=30):
    value_short = safe(value)
    title_short = safe(title)
    sub_short = safe(subtitle)
    svg.append(f'<circle cx="{x}" cy="{y}" r="{radius+10}" fill="{color}" opacity=".08"/>')
    svg.append(f'<circle cx="{x}" cy="{y}" r="{radius+4}" fill="none" '
               f'stroke="{color}" stroke-opacity=".55" stroke-width="1.3"/>')
    svg.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="url(#core)" '
               f'stroke="{color}" stroke-width="2.2" filter="url(#softGlow)"/>')
    # Punto central tipo circuito.
    svg.append(f'<circle cx="{x}" cy="{y-5}" r="4" fill="{color}" opacity=".95"/>')
    svg.append(f'<text x="{x}" y="{y+10}" fill="#f4f7ff" font-size="8.5" '
               f'font-weight="800" text-anchor="middle">{title_short}</text>')
    # Etiqueta de valor superior.
    pill_w = min(150, max(72, len(value_short)*7+20))
    svg.append(f'<rect x="{x-pill_w/2}" y="{y-radius-27}" width="{pill_w}" '
               f'height="19" rx="9.5" fill="{color}" opacity=".98"/>')
    svg.append(f'<text x="{x}" y="{y-radius-14}" fill="#07111f" '
               f'font-size="10" font-weight="850" text-anchor="middle">{value_short}</text>')
    svg.append(f'<text x="{x}" y="{y+radius+17}" fill="#91a5c8" '
               f'font-size="9" text-anchor="middle">{sub_short}</text>')

for item in input_nodes:
    draw_node(*item, "#438cff", 27)
for item in analysis_nodes:
    draw_node(*item, "#b06cff", 32)
for item in process_nodes:
    draw_node(*item, "#18cdb8", 32)
for item in output_nodes:
    draw_node(*item, "#ff9a54", 34)

# Núcleo visual decorativo entre etapas, sin alterar cálculos.
svg.append("""
<g opacity=".95">
  <circle cx="652" cy="390" r="57" fill="#101d35" stroke="#6d79ff"
          stroke-width="1.5" stroke-dasharray="4 7"/>
  <circle cx="652" cy="390" r="42" fill="#19294a" stroke="#8b74ff"
          stroke-width="1.5" filter="url(#softGlow)"/>
  <circle cx="652" cy="390" r="24" fill="#253d68" stroke="#b18aff" stroke-width="1.5"/>
  <text x="652" y="387" fill="#ffffff" text-anchor="middle"
        font-size="19" font-weight="900">RN</text>
  <text x="652" y="402" fill="#b9c9ec" text-anchor="middle"
        font-size="8" font-weight="700">CORE</text>
  <text x="652" y="468" fill="#a9b8d6" text-anchor="middle"
        font-size="10" font-weight="800">NÚCLEO</text>
  <text x="652" y="482" fill="#7489ad" text-anchor="middle"
        font-size="9">de procesamiento</text>
</g>
""")

# Leyenda inferior.
legend = [
    (390, "ENTRADAS", "#438cff"),
    (560, "ANÁLISIS", "#b06cff"),
    (720, "CÁLCULOS", "#18cdb8"),
    (900, "SALIDAS", "#ff9a54"),
]
for x, label, color in legend:
    svg.append(f'<circle cx="{x}" cy="755" r="5" fill="{color}"/>')
    svg.append(f'<text x="{x+12}" y="759" fill="#91a5c8" font-size="10" '
               f'font-weight="700">{label}</text>')

svg.append("</svg>")
diagram = "".join(svg)

# ---------------------------- ENCABEZADO ---------------------
st.markdown(
    f"""
    <div class="hero">
      <div>
        <p class="hero-title">🧠 Red Neuronal Tributaria</p>
        <p class="hero-sub">Un sistema visual que transforma los datos financieros
        en un recorrido de análisis, procesamiento y resultados de IVA e Impuesto a la Renta.</p>
      </div>
      <div class="hero-meta"><b>{safe(DEVELOPER_NAME)}</b><br>
      Modelo interactivo · Ecuador</div>
    </div>
    <div class="neon-rule"></div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Mapa de procesamiento neuronal · Flujo de datos en tiempo real</div>',
            unsafe_allow_html=True)

components.html(
    f"""
    <div style="width:100%; overflow-x:auto; background:#0a1427; border-radius:22px;
                border:1px solid rgba(112,145,202,.20);">
      {diagram}
    </div>
    """,
    height=805,
    scrolling=False,
)

# ------------------------- RESULTADOS ------------------------
st.markdown("### 📊 Panel de resultados")
st.markdown(
    f"""
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-name">IVA a pagar</div>
        <div class="metric-number">{fmt(iva_a_pagar)}</div>
      </div>
      <div class="metric-card">
        <div class="metric-name">Crédito a favor</div>
        <div class="metric-number">{fmt(iva_a_favor)}</div>
      </div>
      <div class="metric-card">
        <div class="metric-name">Renta a pagar</div>
        <div class="metric-number">{fmt(renta_a_pagar)}</div>
      </div>
      <div class="metric-card">
        <div class="metric-name">Base imponible de renta</div>
        <div class="metric-number">{fmt(base_imponible_renta)}</div>
      </div>
    </div>
    <p class="hint">Los resultados se calculan con las fórmulas que ya tenía tu código.
    Este diseño es una representación visual del flujo de cálculo, no un modelo de
    aprendizaje automático entrenado ni una validación de la normativa tributaria.</p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption(f"Red Neuronal Tributaria · Desarrollado por {DEVELOPER_NAME}")
