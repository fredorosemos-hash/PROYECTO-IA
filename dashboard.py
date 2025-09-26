import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from io import BytesIO

st.set_page_config(page_title="Dashboard Fiscalía", layout="wide")
st.title("INFORME DE GESTIÓN 2020-2024 - Fiscalía General de la Nación")

# Logo
st.image("https://upload.wikimedia.org/wikipedia/commons/2/2e/Fiscalia_General_de_la_Nacion_de_Colombia_logo.png", width=150)

# Carga de datos
st.sidebar.header("Carga de datos")
data_file = st.sidebar.file_uploader("Sube un archivo CSV o JSON", type=["csv", "json"])

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

# Gráfico de barras
st.subheader("Delitos reportados por ciudad")
fig, ax = plt.subplots()
ax.bar(ciudades, delitos_reportados, color=['#00eaff','#ffb700','#ff3b3b','#00ffae','#2c5364'])
ax.set_ylabel('Cantidad')
ax.set_xlabel('Ciudad')
st.pyplot(fig)

# Gráfico de torta
st.subheader("Distribución de delitos")
fig2, ax2 = plt.subplots()
ax2.pie(delitos_cant, labels=delitos, autopct='%1.1f%%', colors=['#ff3b3b','#00eaff','#ffb700','#00ffae'])
st.pyplot(fig2)

# Mapa de Colombia
st.subheader("Mapa de delitos por ciudad")
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
st_folium(mapa, width=700, height=400)

# Botón para descargar informe
st.subheader("Generar informe tipo Word")
if st.button("Descargar informe"):
    from docx import Document
    doc = Document()
    doc.add_heading('INFORME DE GESTIÓN 2020-2024', 0)
    doc.add_paragraph('Fiscalía General de la Nación')
    doc.add_paragraph('Balance de la Administración')
    doc.add_paragraph('Delitos reportados por ciudad:')
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Ciudad'
    hdr_cells[1].text = 'Delitos'
    for ciudad, cantidad in zip(ciudades, delitos_reportados):
        row_cells = table.add_row().cells
        row_cells[0].text = ciudad
        row_cells[1].text = str(cantidad)
    doc.add_paragraph('Distribución de delitos:')
    for delito, cant in zip(delitos, delitos_cant):
        doc.add_paragraph(f"{delito}: {cant}")
    # Guardar y descargar
    buffer = BytesIO()
    doc.save(buffer)
    st.download_button(
        label="Descargar Informe Word",
        data=buffer.getvalue(),
        file_name="Informe_Gestion_Fiscalia.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
