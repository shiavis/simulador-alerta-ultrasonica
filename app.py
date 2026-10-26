from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Alerta Ultrasónica · Streamlit",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&display=swap');
      html, body, [class*="css"] { font-family: 'Barlow Condensed', 'Arial Narrow', sans-serif; }
      .stApp { background: #0b1518; color: #f0f0e6; }
      [data-testid="stSidebar"] { background: #18272a; border-right: 1px solid rgba(213,226,220,.18); }
      [data-testid="stMetric"] { background: rgba(48,64,68,.65); border: 1px solid rgba(213,226,220,.16); padding: 12px; }
      .hero { padding: 18px 0 12px; border-bottom: 1px solid rgba(213,226,220,.16); }
      .kicker { color: #ffb300; font-size: 12px; font-weight: 800; letter-spacing: .16em; margin: 0 0 9px; }
      .hero h1 { color: #f0f0e6; font-size: clamp(36px, 5vw, 68px); line-height: .9; margin: 0 0 16px; text-transform: uppercase; }
      .hero h1 em { color: #2dd4bf; font-style: normal; }
      .hero p { max-width: 710px; color: #a6b4b0; font-family: Arial, sans-serif; line-height: 1.6; }
      .note { border-left: 4px solid #ffb300; background: rgba(255,179,0,.08); color: #d5e2dc; padding: 11px 14px; font-family: Arial, sans-serif; font-size: 12px; line-height: 1.5; }
      .formula { border-left: 3px solid #2dd4bf; background: rgba(45,212,191,.08); padding: 11px 14px; color: #a6b4b0; font-family: Arial, sans-serif; }
      .formula strong { display: block; color: #f0f0e6; font-size: 19px; font-family: 'Barlow Condensed', sans-serif; }
      .section-label { color: #ffb300; font-size: 11px; font-weight: 800; letter-spacing: .14em; margin: 22px 0 8px; }
      footer { color: #738482; font-size: 10px; letter-spacing: .12em; padding-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <p class="kicker">LABORATORIO DE FÍSICA APLICADA / STREAMLIT</p>
      <h1>¿Qué escucha un canal<br><em>antes de desbordarse?</em></h1>
      <p>Versión Python del simulador de alerta temprana. La escena conserva el sensor ultrasónico, el pulso, el eco, el nivel animado y la lógica de umbrales de la versión web.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Variables de campo")
    rain = st.slider("Intensidad de lluvia (%)", 0, 100, 65)
    sensor_height = st.slider("Altura del sensor H (m)", 1.5, 3.5, 2.5, 0.1)
    temperature = st.slider("Temperatura del aire T (°C)", -10, 50, 20)
    correction = st.toggle("Corregir velocidad del sonido", value=True)
    st.markdown("### Umbrales didácticos")
    caution = st.number_input("Precaución (m)", min_value=0.30, max_value=2.00, value=1.00, step=0.05)
    alert = st.number_input("Alerta (m)", min_value=0.35, max_value=2.10, value=1.45, step=0.05)
    emergency = st.number_input("Emergencia (m)", min_value=0.40, max_value=2.15, value=1.85, step=0.05)
    st.caption("Los límites son demostrativos y deben validarse en campo.")

# The component performs the same continuous animation in the browser while Python owns the initial physical state.
initial_level = 0.72
sound_speed = 331 + 0.6 * temperature if correction else 343.0
distance = max(0.05, sensor_height - initial_level)
time_of_flight = 2 * distance / sound_speed

st.markdown('<p class="section-label">ESCENA ANIMADA / SENSOR US-01</p>', unsafe_allow_html=True)
scene = (ROOT / "scene.html").read_text(encoding="utf-8")
replacements = {
    "__LEVEL__": f"{initial_level:.4f}",
    "__RAIN__": str(rain),
    "__HEIGHT__": f"{sensor_height:.2f}",
    "__TEMP__": str(temperature),
    "__SPEED__": f"{sound_speed:.3f}",
    "__CAUTION__": f"{caution:.2f}",
    "__ALERT__": f"{alert:.2f}",
    "__EMERGENCY__": f"{emergency:.2f}",
}
for token, value in replacements.items():
    scene = scene.replace(token, value)
components.html(scene, height=760, scrolling=False)

status = "EMERGENCIA" if initial_level >= emergency else "ALERTA" if initial_level >= alert else "PRECAUCIÓN" if initial_level >= caution else "NORMAL"
st.markdown('<p class="section-label">TELEMETRÍA CALCULADA EN PYTHON</p>', unsafe_allow_html=True)
metric_cols = st.columns(5)
metric_cols[0].metric("Nivel inicial", f"{initial_level:.2f} m", status)
metric_cols[1].metric("Distancia d", f"{distance:.2f} m")
metric_cols[2].metric("Tiempo de vuelo t", f"{time_of_flight * 1000:.2f} ms")
metric_cols[3].metric("Velocidad del sonido", f"{sound_speed:.1f} m/s")
metric_cols[4].metric("Lluvia", f"{rain}%")

st.markdown(
    f'<div class="formula"><strong>d = v · t / 2</strong>{distance:.2f} m = ({sound_speed:.1f} m/s × {time_of_flight * 1000:.2f} ms) / 2<br><br><strong>L = H − d</strong>{initial_level:.2f} m = {sensor_height:.2f} m − {distance:.2f} m</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="section-label">FUNDAMENTO FÍSICO</p><div class="note"><b>Onda mecánica longitudinal:</b> el ultrasonido necesita el aire para propagarse. Al llegar al agua se refleja; el sensor mide el tiempo de ida y vuelta del eco, calcula la distancia y reconstruye el nivel. Esta aplicación es una demostración educativa y no sustituye un sistema certificado de Protección Civil.</div>',
    unsafe_allow_html=True,
)
st.markdown("<footer>ALERTA·ULTRASÓNICA / MODELO EDUCATIVO / VERSIÓN STREAMLIT</footer>", unsafe_allow_html=True)
