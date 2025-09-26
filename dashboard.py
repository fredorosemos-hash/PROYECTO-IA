

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from io import BytesIO

st.set_page_config(page_title="Dashboard Fiscalía", layout="wide")

# Estilos CSS cibernéticos futuristas
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
        color: #fff;
    }
    .neon-box {
        background: rgba(20,30,40,0.85);
        border-radius: 18px;
        box-shadow: 0 0 24px #00eaff, 0 0 8px #ff3b3b;
        padding: 32px 24px;
        margin-bottom: 32px;
        border: 2px solid #00eaff;
    }
    .neon-title {
        font-family: 'Orbitron', 'Segoe UI', sans-serif;
        font-size: 2.5rem;
        color: #00eaff;
        text-shadow: 0 0 12px #00eaff, 0 0 4px #fff;
        margin-bottom: 0;
    }
    .neon-sub {
        font-size: 1.2rem;
        color: #ffb700;
        text-shadow: 0 0 8px #ffb700;
        margin-top: 0;
    }
    .neon-btn button {
        background: linear-gradient(90deg, #00eaff 0%, #ff3b3b 100%);
        color: #fff;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        box-shadow: 0 0 8px #00eaff;
    }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Orbitron:700" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='neon-box' style='display:flex;align-items:center;justify-content:center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/2/2e/Fiscalia_General_de_la_Nacion_de_Colombia_logo.png' width='60' style='margin-right:16px;filter:drop-shadow(0 0 8px #00eaff);'>
        <div>
            <h1 class='neon-title' style='text-align:center;'>INFORME DE GESTIÓN 2020-2024</h1>
            <h3 class='neon-sub' style='text-align:center;'>Fiscalía General de la Nación</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Carga de datos (sin panel lateral)
st.markdown("<div class='neon-box' style='margin-bottom:16px;'><h3 class='neon-sub'>Carga de datos</h3>", unsafe_allow_html=True)
data_file = st.file_uploader("Sube un archivo CSV o JSON", type=["csv", "json"])
st.markdown("</div>", unsafe_allow_html=True)

# Datos por defecto
ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
delitos_reportados = [120, 90, 70, 50, 40]
delitos = ['Hurto', 'Homicidio', 'Fraude', 'Secuestro']
delitos_cant = [60, 25, 10, 5]

if data_file:
    if data_file.name.endswith('.csv'):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_json(data_file)
    if 'ciudad' in df.columns and 'cantidad' in df.columns:
        ciudades = df['ciudad'].tolist()
        delitos_reportados = df['cantidad'].tolist()
    if 'delito' in df.columns and 'cantidad' in df.columns:
        delitos = df['delito'].tolist()
        delitos_cant = df['cantidad'].tolist()

col1, col2 = st.columns([3,2])

with col1:
    st.markdown("<div class='neon-box'><h2 class='neon-title'>Delitos por ciudad</h2>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5.5,3.5), facecolor='#0f2027')
    ax.bar(ciudades, delitos_reportados, color=['#00eaff','#ffb700','#ff3b3b','#00ffae','#2c5364'])
    ax.set_ylabel('Cantidad', color='#fff')
    ax.set_xlabel('Ciudad', color='#fff')
    ax.tick_params(colors='#00eaff')
    fig.patch.set_facecolor('#0f2027')
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='neon-box'><h2 class='neon-title'>Distribución de delitos</h2>", unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(4.2,4.2), facecolor='#0f2027')
    ax2.pie(delitos_cant, labels=delitos, autopct='%1.1f%%', colors=['#ff3b3b','#00eaff','#ffb700','#00ffae'])
    fig2.patch.set_facecolor('#0f2027')
    st.pyplot(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='neon-box'><h2 class='neon-title'>Mapa de delitos por ciudad</h2>", unsafe_allow_html=True)
    coords = {
        'Bogotá': [4.7110, -74.0721],
        'Medellín': [6.2442, -75.5812],
        'Cali': [3.4516, -76.5320],
        'Barranquilla': [10.9685, -74.7813],
        'Cartagena': [10.3910, -75.4794]
    }
    mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=5)
    for ciudad, cantidad in zip(ciudades, delitos_reportados):
        if ciudad in coords:
            folium.Marker(coords[ciudad], popup=f"{ciudad}: {cantidad} delitos").add_to(mapa)
    st_folium(mapa, width=370, height=220)
    st.markdown("</div>", unsafe_allow_html=True)

# Botón para descargar informe
st.markdown("<div class='neon-box'><h2 class='neon-title'>Generar informe tipo Word</h2>", unsafe_allow_html=True)
if st.button("Descargar informe", key="neon-btn"):
    from docx import Document
    doc = Document()
    doc.add_heading('INFORME DE GESTIÓN 2020-2024', 0)
    doc.add_paragraph('Fiscalía General de la Nación')

    # Redacción automática con IA
    resumen = f"Durante el periodo 2020-2024, la Fiscalía General de la Nación ha gestionado un total de {sum(delitos_reportados)} delitos reportados en las principales ciudades del país. "
    resumen += f"La ciudad con mayor incidencia fue {ciudades[delitos_reportados.index(max(delitos_reportados))]} con {max(delitos_reportados)} casos, mientras que la de menor incidencia fue {ciudades[delitos_reportados.index(min(delitos_reportados))]} con {min(delitos_reportados)} casos. "
    resumen += "Los delitos más frecuentes fueron: " + ", ".join([f"{delito} ({cant})" for delito, cant in zip(delitos, delitos_cant)]) + ". "
    resumen += "El análisis de estos datos permite identificar tendencias y orientar estrategias institucionales para la prevención y judicialización de los delitos más relevantes."
    doc.add_paragraph(resumen)

    doc.add_paragraph('Detalle de delitos reportados por ciudad:')
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Ciudad'
    hdr_cells[1].text = 'Delitos reportados'
    for ciudad, cantidad in zip(ciudades, delitos_reportados):
        row_cells = table.add_row().cells
        row_cells[0].text = ciudad
        row_cells[1].text = str(cantidad)

    doc.add_paragraph('Distribución de delitos:')
    for delito, cant in zip(delitos, delitos_cant):
        doc.add_paragraph(f"- {delito}: {cant} casos")

    conclusion = f"En conclusión, el periodo analizado evidencia que {ciudades[delitos_reportados.index(max(delitos_reportados))]} requiere especial atención por su alta incidencia delictiva, mientras que el delito más frecuente es {delitos[delitos_cant.index(max(delitos_cant))]}. La Fiscalía continuará fortaleciendo sus capacidades investigativas y preventivas para mejorar la seguridad ciudadana."
    doc.add_paragraph(conclusion)

    # Guardar y descargar
    buffer = BytesIO()
    doc.save(buffer)
    st.download_button(
        label="Descargar Informe Word",
        data=buffer.getvalue(),
        file_name="Informe_Gestion_Fiscalia.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
st.markdown("</div>", unsafe_allow_html=True)
