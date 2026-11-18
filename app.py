import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Red neuronal tributaria | IVA e Impuesto a la Renta",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DEVELOPER_NAME = "Jonathan Toasa"

# ------------------------- ESTILOS -------------------------
st.markdown("""
<style>
.stApp {
    background: #080f1e;
    color: #e8eefc;
}
.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
.main-title {
    color: #f4f7ff;
    font-size: clamp(1.7rem, 3vw, 2.55rem);
    font-weight: 850;
    line-height: 1.15;
    margin: 0;
}
.sub-title {
    color: #9fb1d2;
    font-size: 1rem;
    margin: .55rem 0 1rem;
}
.section-title {
    color: #f2f6ff;
    font-size: 1.35rem;
    font-weight: 800;
    margin: 1.5rem 0 .3rem;
}
div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
    background: #111d33;
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 12px;
    padding: 10px 12px 2px;
}
.metric-card {
    background: linear-gradient(145deg,#14233e,#101a2d);
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 14px;
    padding: 15px 17px;
    min-height: 92px;
}
.metric-label {
    color: #9fb1d2;
    font-size: .76rem;
    text-transform: uppercase;
    font-weight: 750;
    letter-spacing: .5px;
}
.metric-value {
    color: #f8faff;
    font-size: 1.35rem;
    font-weight: 850;
    margin-top: 5px;
}
.note {
    color: #91a2c1;
    font-size: .82rem;
}
hr { border-color: rgba(148,163,184,.18); }
</style>
""", unsafe_allow_html=True)

def money(value):
    return f"${value:,.2f}"

# ------------------------- ENCABEZADO -------------------------
st.markdown('<p class="main-title">🧠 Red neuronal tributaria</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Ley Orgánica de Régimen Tributario Interno (LRTI): '
    'explora cómo sus disposiciones se ramifican hacia el IVA y el Impuesto a la Renta.</p>',
    unsafe_allow_html=True,
)

# ------------------------- DATOS INICIALES Y CÁLCULOS -------------------------
# Los valores iniciales son únicamente demostrativos. Se pueden editar debajo del gráfico.
if "ventas_mes" not in st.session_state:
    st.session_state.ventas_mes = 10000.0
if "compras_mes" not in st.session_state:
    st.session_state.compras_mes = 6000.0
if "iva_compras_pagado" not in st.session_state:
    st.session_state.iva_compras_pagado = 900.0
if "tipo_tarifa" not in st.session_state:
    st.session_state.tipo_tarifa = 15.0
if "retenciones_recibidas" not in st.session_state:
    st.session_state.retenciones_recibidas = 1290.0
if "ingresos_anual" not in st.session_state:
    st.session_state.ingresos_anual = 200000.0
if "costos_anual" not in st.session_state:
    st.session_state.costos_anual = 160000.0

ventas_mes = st.session_state.ventas_mes
compras_mes = st.session_state.compras_mes
iva_compras_pagado = st.session_state.iva_compras_pagado
tipo_tarifa = st.session_state.tipo_tarifa
retenciones_recibidas = st.session_state.retenciones_recibidas
ingresos_anual = st.session_state.ingresos_anual
costos_anual = st.session_state.costos_anual

iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = iva_compras_pagado
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))

base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_retenida = retenciones_recibidas * 0.90
renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

# ------------------------- RED NEURONAL INTERACTIVA -------------------------
# Los nodos se pueden pulsar: el panel inferior del gráfico muestra su explicación.
def esc(value):
    return html.escape(str(value), quote=True)

# Distribución visual inspirada en la referencia: cuatro columnas de proceso,
# dos recorridos (IVA e IR) y la LRTI como núcleo central de la red.
W, H = 1400, 760

def text_svg(x, y, value, size=13, color="#eaf0ff", weight=600):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{esc(value)}</text>')

def node_svg(node_id, x, y, title, value, color, heading, detail):
    safe_heading, safe_detail = esc(heading), esc(detail)
    return f'''
    <g class="node" tabindex="0" role="button" aria-label="{safe_heading}"
       data-title="{safe_heading}" data-detail="{safe_detail}" data-node="{node_id}" style="cursor:pointer">
      <rect x="{x-39}" y="{y-83}" width="78" height="19" rx="9.5" fill="{color}" opacity=".96"/>
      {text_svg(x, y-69, value, 10, "#071326", 850)}
      <circle cx="{x}" cy="{y}" r="43" fill="{color}" opacity=".10" class="halo"/>
      <circle cx="{x}" cy="{y}" r="33" fill="#101e35" stroke="{color}" stroke-width="2.2"/>
      <circle cx="{x}" cy="{y}" r="25" fill="none" stroke="{color}" stroke-opacity=".25"/>
      <circle cx="{x}" cy="{y}" r="3.5" fill="{color}"/>
      {text_svg(x, y+12, title, 8.5, "#f4f7ff", 850)}
      {text_svg(x, y+59, heading, 10, "#c7d5ed", 700)}
    </g>'''

node_specs = [
    ("iva_in", 145, 220, "VENTAS", money(ventas_mes), "#438cff", "Entrada IVA · Ventas", "Ventas del mes antes de IVA, usadas como referencia para calcular el impuesto generado."),
    ("iva_purchases", 145, 390, "IVA COMPRAS", money(iva_compras_pagado), "#438cff", "IVA pagado en compras", "Valor del IVA pagado en adquisiciones. Se ingresa por separado para reflejar facturas con distintas tarifas y el crédito tributario que efectivamente corresponda."),
    ("iva_analysis", 500, 305, "TARIFA", f"{tipo_tarifa:g}%", "#b46cff", "Análisis IVA", "La tarifa seleccionada se aplica a las ventas gravadas. El IVA pagado en compras se registra separadamente y puede constituir crédito tributario si cumple los requisitos legales."),
    ("iva_process", 855, 305, "IVA VENTAS", money(iva_en_ventas), "#12c8b5", "Procesamiento IVA", f"IVA generado estimado: {money(iva_en_ventas)}. Crédito tributario estimado: {money(credito_tributario)}."),
    ("iva_result", 1210, 305, "A PAGAR", money(iva_a_pagar), "#ff9b50", "Resultado IVA", f"IVA estimado a pagar: {money(iva_a_pagar)}. Saldo a favor estimado: {money(iva_a_favor)}."),
    ("ir_in", 145, 570, "INGRESOS", money(ingresos_anual), "#438cff", "Entrada IR", "Ingresos anuales y costos o gastos deducibles declarados para el ejercicio fiscal."),
    ("ir_analysis", 500, 570, "BASE", money(base_imponible_renta), "#b46cff", "Análisis IR", "La base imponible se obtiene depurando los ingresos gravados con los costos, gastos y deducciones permitidos por la LRTI."),
    ("ir_process", 855, 570, "IMPUESTO", money(impuesto_causado_renta), "#12c8b5", "Procesamiento IR", f"Impuesto causado estimado con tarifa referencial del 25%: {money(impuesto_causado_renta)}."),
    ("ir_result", 1210, 570, "A PAGAR", money(renta_a_pagar), "#ff9b50", "Resultado IR", f"Impuesto a la Renta estimado por pagar: {money(renta_a_pagar)}."),
]

svg = [f'''
<div id="neural-wrap" style="width:100%;overflow:hidden;border:1px solid #233653;
     border-radius:22px;background:#0b1528;box-shadow:0 18px 55px rgba(0,0,0,.25)">
<div class="zoom-toolbar" style="display:flex;align-items:center;gap:8px;padding:10px 12px;background:#101d33;border-bottom:1px solid #263958">
 <span style="color:#aebddb;font:700 12px Inter,Segoe UI,Arial">ZOOM DEL GRÁFICO</span>
 <button type="button" class="zoom-btn" data-zoom="in" aria-label="Acercar">＋</button>
 <button type="button" class="zoom-btn" data-zoom="out" aria-label="Alejar">−</button>
 <button type="button" class="zoom-btn reset" data-zoom="reset">Restablecer</button>
 <span class="zoom-help">También puedes usar la rueda del ratón y arrastrar para desplazarte.</span>
 <span id="zoom-level" style="margin-left:auto;color:#c4b5fd;font:700 12px Inter,Segoe UI,Arial">100%</span>
</div>
<svg id="neural-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     style="display:block;width:100%;height:auto;touch-action:none;cursor:grab" aria-label="Red neuronal tributaria interactiva">
<defs>
 <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
  <path d="M26 0H0V26" fill="none" stroke="#263958" stroke-width=".8" opacity=".62"/>
 </pattern>
 <filter id="glow"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#283e72"/><stop offset="1" stop-color="#111d38"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="#0b1528"/>
<rect width="{W}" height="{H}" rx="22" fill="url(#grid)"/>
''']

for x, color, label, sub in [
    (145, "#438cff", "ENTRADA", "Datos de entrada"),
    (500, "#b46cff", "ANÁLISIS", "Clasificación tributaria"),
    (855, "#12c8b5", "PROCESAMIENTO", "Operaciones y cálculos"),
    (1210, "#ff9b50", "RESULTADOS", "Salidas del sistema"),
]:
    svg.append(f'<circle cx="{x-53}" cy="55" r="4.5" fill="{color}"/>')
    svg.append(text_svg(x+2, 59, label, 12, color, 850))
    svg.append(text_svg(x+2, 76, sub, 8, "#8093b5", 550))

paths = [
    (145,220,500,305,"#438cff"),(145,390,500,305,"#438cff"),
    (500,305,855,305,"#b46cff"),(855,305,1210,305,"#12c8b5"),
    (145,570,500,570,"#438cff"),(500,570,855,570,"#b46cff"),(855,570,1210,570,"#12c8b5"),
    (145,220,500,570,"#438cff"),(145,570,500,305,"#438cff"),
    (500,305,855,570,"#b46cff"),(500,570,855,305,"#b46cff"),
    (855,305,1210,570,"#12c8b5"),(855,570,1210,305,"#12c8b5"),
]
for x1,y1,x2,y2,color in paths:
    svg.append(f'<path d="M{x1} {y1} C{(x1+x2)/2} {y1}, {(x1+x2)/2} {y2}, {x2} {y2}" fill="none" stroke="{color}" stroke-width="1.15" opacity=".22"/>')

svg += [
 '<path class="flow-line" d="M700 360 C650 320 590 270 535 255" fill="none" stroke="#438cff" stroke-width="2.5" stroke-dasharray="7 7"/>',
 '<path class="flow-line" d="M700 405 C650 455 590 520 535 535" fill="none" stroke="#b46cff" stroke-width="2.5" stroke-dasharray="7 7"/>',
 '<path d="M700 360 C570 170 340 165 178 235" fill="none" stroke="#438cff" stroke-width="1.2" opacity=".18"/>',
 '<path d="M700 405 C570 610 340 620 178 555" fill="none" stroke="#b46cff" stroke-width="1.2" opacity=".18"/>',
 '<g class="node central" tabindex="0" role="button" data-title="Ley Orgánica de Régimen Tributario Interno (LRTI)" data-detail="La LRTI es el núcleo normativo de esta red. De ella parten las reglas del Impuesto al Valor Agregado y del Impuesto a la Renta. Selecciona los nodos de cada rama para explorar sus etapas." style="cursor:pointer">',
 '<circle cx="700" cy="382" r="91" fill="#8b5cf6" opacity=".13" filter="url(#glow)"/>',
 '<circle cx="700" cy="382" r="67" fill="url(#core)" stroke="#a78bfa" stroke-width="2.7"/>',
 '<circle cx="700" cy="382" r="55" fill="none" stroke="#a78bfa" stroke-opacity=".38"/>',
 text_svg(700, 376, "LRTI", 28, "#ffffff", 900),
 text_svg(700, 398, "LEY TRIBUTARIA", 9, "#c4b5fd", 850),
 text_svg(700, 415, "ECUADOR · 2026", 8, "#aebddb", 650),
 '</g>',
]
for spec in node_specs:
    svg.append(node_svg(*spec))

for x,color,label in [(510,"#438cff","ENTRADAS"),(650,"#b46cff","ANÁLISIS"),(790,"#12c8b5","CÁLCULOS"),(930,"#ff9b50","SALIDAS")]:
    svg.append(f'<circle cx="{x}" cy="674" r="4.5" fill="{color}"/>')
    svg.append(text_svg(x+48,678,label,9,"#aebddb",700))
svg += ['</svg>', '''
<div id="node-info" style="margin:0 18px 18px;padding:13px 17px;border-radius:12px;
 background:#111f36;border:1px solid #2a3d5d;color:#dce7fb">
 <div id="node-title" style="font-weight:800;color:#c4b5fd;margin-bottom:4px">LEY ORGÁNICA DE RÉGIMEN TRIBUTARIO INTERNO</div>
 <div id="node-detail" style="font-size:13px;line-height:1.5;color:#b8c7e2">Pulsa cualquier nodo para conocer su función y relación con el proceso tributario.</div>
</div></div>
<style>
#neural-svg .node{outline:none}#neural-svg .node:hover .halo,#neural-svg .node:focus .halo{opacity:.3;filter:url(#glow)}
#neural-svg .node.selected circle:nth-of-type(2){stroke-width:4;filter:url(#glow)}
#neural-svg .flow-line{animation:flow 4.5s linear infinite}@keyframes flow{to{stroke-dashoffset:-56}}
#neural-wrap .zoom-btn{border:1px solid #385174;background:#1a2b47;color:#edf4ff;border-radius:7px;padding:5px 11px;font-weight:800;cursor:pointer}
#neural-wrap .zoom-btn:hover{background:#294269}#neural-wrap .zoom-btn.reset{font-size:11px;font-weight:650}
#neural-wrap .zoom-help{color:#8093b5;font:11px Inter,Segoe UI,Arial;margin-left:5px}
@media(max-width:700px){#neural-wrap .zoom-help{display:none}}
@media(prefers-reduced-motion:reduce){.flow-line{animation:none}}
</style>
<script>
(function(){const root=document.getElementById('neural-wrap');if(!root)return;
 const svg=root.querySelector('#neural-svg');
 const ns=root.querySelectorAll('.node'),title=root.querySelector('#node-title'),detail=root.querySelector('#node-detail');
 const zoomLabel=root.querySelector('#zoom-level');
 const base={x:0,y:0,w:1400,h:760};let view={...base},drag=null;
 function applyView(){svg.setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);zoomLabel.textContent=Math.round(base.w/view.w*100)+'%';}
 function zoom(factor,cx=view.x+view.w/2,cy=view.y+view.h/2){const nw=Math.max(base.w/2.5,Math.min(base.w*1.8,view.w/factor));const nh=nw*base.h/base.w;
 const rx=(cx-view.x)/view.w,ry=(cy-view.y)/view.h;view={x:cx-rx*nw,y:cy-ry*nh,w:nw,h:nh};applyView();}
 root.querySelectorAll('[data-zoom]').forEach(b=>b.addEventListener('click',()=>{const z=b.dataset.zoom;if(z==='in')zoom(1.25);else if(z==='out')zoom(1/1.25);else{view={...base};applyView();}}));
 svg.addEventListener('wheel',e=>{e.preventDefault();const r=svg.getBoundingClientRect();const px=(e.clientX-r.left)/r.width,py=(e.clientY-r.top)/r.height;zoom(e.deltaY<0?1.15:1/1.15,view.x+px*view.w,view.y+py*view.h);},{passive:false});
 svg.addEventListener('pointerdown',e=>{if(e.target.closest('.node'))return;drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y};svg.setPointerCapture(e.pointerId);svg.style.cursor='grabbing';});
 svg.addEventListener('pointermove',e=>{if(!drag)return;const r=svg.getBoundingClientRect();view.x=drag.vx-(e.clientX-drag.x)*view.w/r.width;view.y=drag.vy-(e.clientY-drag.y)*view.h/r.height;applyView();});
 function stopDrag(){drag=null;svg.style.cursor='grab';}svg.addEventListener('pointerup',stopDrag);svg.addEventListener('pointercancel',stopDrag);
 function activate(el){ns.forEach(n=>n.classList.remove('selected'));el.classList.add('selected');title.textContent=el.dataset.title||'Nodo tributario';detail.textContent=el.dataset.detail||'';}
 ns.forEach(el=>{el.addEventListener('click',()=>activate(el));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();activate(el);}});});
 applyView();})();
</script>
''']
components.html("".join(svg), height=820, scrolling=False)

st.markdown('<p class="note">Selecciona los nodos para explorar la red. Las conexiones animadas representan el flujo conceptual desde la LRTI hacia el IVA y el Impuesto a la Renta.</p>', unsafe_allow_html=True)

# ------------------------- CONTROLES DEBAJO DEL GRÁFICO -------------------------
st.markdown('<div class="section-title">⚙️ Centro de control y datos de entrada</div>', unsafe_allow_html=True)
st.markdown("Modifica los valores para actualizar los nodos y los resultados de la red.")

col_iva, col_ir = st.columns(2, gap="large")
with col_iva:
    st.markdown("#### 🔵 1. Datos del IVA")
    ventas_mes = st.number_input(
        "Ventas del mes (USD sin IVA)", min_value=0.0, step=500.0,
        key="ventas_mes", format="%.2f"
    )
    compras_mes = st.number_input(
        "Compras del mes (USD sin IVA)", min_value=0.0, step=500.0,
        key="compras_mes", format="%.2f"
    )
    iva_compras_pagado = st.number_input(
        "IVA pagado en compras (USD)", min_value=0.0, step=50.0,
        key="iva_compras_pagado", format="%.2f",
        help="Ingresa el IVA que consta en las facturas de compra. Solo será crédito tributario en la medida en que cumpla los requisitos legales."
    )
    tipo_tarifa = st.selectbox(
        "Tarifa IVA aplicable", [15.0, 8.0, 5.0, 0.0],
        key="tipo_tarifa", format_func=lambda x: ("8% · turismo en feriados autorizados" if x == 8.0 else f"{x:g}%")
    )
    retenciones_recibidas = st.number_input(
        "Retenciones recibidas (USD)", min_value=0.0, step=50.0,
        key="retenciones_recibidas", format="%.2f"
    )

with col_ir:
    st.markdown("#### 🟣 2. Datos del Impuesto a la Renta")
    ingresos_anual = st.number_input(
        "Ingresos del año (USD)", min_value=0.0, step=5000.0,
        key="ingresos_anual", format="%.2f"
    )
    costos_anual = st.number_input(
        "Costos y gastos deducibles (USD)", min_value=0.0, step=5000.0,
        key="costos_anual", format="%.2f"
    )
    st.info("En este prototipo, la tarifa de sociedades del 25% se utiliza como supuesto simplificado para estimar el IR. No sustituye la tabla progresiva de personas naturales ni los cálculos especiales del RIMPE.")

# Recalcular con los valores actuales.
iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = iva_compras_pagado
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))
base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_retenida = retenciones_recibidas * 0.90
renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

# Botón para forzar una nueva renderización del gráfico con los valores actualizados.
if st.button("🔄 Actualizar red neuronal", type="primary", use_container_width=True):
    st.rerun()

# ------------------------- RESULTADOS -------------------------
st.markdown('<div class="section-title">📊 Resultados del procesamiento</div>', unsafe_allow_html=True)
metrics = [
    ("IVA generado", money(iva_en_ventas)),
    ("IVA pagado en compras", money(iva_compras_pagado)),
    ("Crédito tributario estimado", money(credito_tributario)),
    ("IVA a pagar", money(iva_a_pagar)),
    ("Saldo IVA a favor", money(iva_a_favor)),
    ("Base imponible de renta", money(base_imponible_renta)),
    ("Impuesto a la renta causado", money(impuesto_causado_renta)),
    ("Retenciones de renta estimadas", money(renta_retenida)),
    ("Impuesto a la renta a pagar", money(renta_a_pagar)),
]
metric_cols = st.columns(3)
for i, (label, value) in enumerate(metrics):
    with metric_cols[i % 3]:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{esc(label)}</div>'
            f'<div class="metric-value">{esc(value)}</div></div>',
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown(
    '<p class="note">Modelo educativo. Los cálculos conservan las fórmulas simplificadas del archivo original '
    '(incluidos los porcentajes de retención parametrizados). Antes de utilizarlo para una declaración real, '
    'deben validarse las tarifas, porcentajes de retención, crédito tributario, régimen y tabla aplicable '
    'según la normativa vigente del SRI.</p>',
    unsafe_allow_html=True,
)
st.caption(f"Desarrollado por {DEVELOPER_NAME} · Ecuador · Modelo académico")
