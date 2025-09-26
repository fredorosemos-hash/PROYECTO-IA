
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd
from io import BytesIO
from docx import Document

with st.sidebar:
    st.markdown("""
    <div style='margin-top:30px;'>
        <a href='https://www.presidencia.gov.co/' target='_blank'><button class='btn' style='width:100%;margin-bottom:12px;'>Presidencia</button></a>
        <a href='https://www.procuraduria.gov.co/' target='_blank'><button class='btn' style='width:100%;margin-bottom:12px;'>Procuraduría</button></a>
        <a href='https://www.mintic.gov.co/' target='_blank'><button class='btn' style='width:100%;margin-bottom:12px;'>MinTIC</button></a>
        <a href='https://www.fiscalia.gov.co/colombia/' target='_blank'><button class='btn' style='width:100%;margin-bottom:12px;'>Fiscalía</button></a>
    </div>
    """, unsafe_allow_html=True)

# Encabezado institucional con logo Fiscalía
LOGO_FISCALIA = "https://upload.wikimedia.org/wikipedia/commons/2/2e/Logo_Fiscalia_General_de_la_Nacion_Colombia.png"
st.image(LOGO_FISCALIA, width=220)
st.markdown(f"""
<div style='background-color:#002855;padding:10px 0 16px 0;text-align:center;'>
    <h1 style='color:#fff;font-family:Segoe UI,Arial,sans-serif;font-size:2.7rem;margin:0;'>Fiscalía General de la Nación</h1>
    <h2 style='color:#e30613;font-family:Segoe UI,Arial,sans-serif;font-size:1.4rem;margin:0;'>Dashboard de Ciberseguridad</h2>
</div>
""", unsafe_allow_html=True)

# Datos de ejemplo
ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
delitos_reportados = [1200, 950, 800, 600, 400]
delitos = ['Hurto', 'Homicidio', 'Estafa', 'Secuestro']
delitos_cant = [1800, 700, 500, 250]

# Layout de columnas
col1, col2 = st.columns([2,2])
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f4f6fa 0%, #e9ecf2 100%);
}
.card {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(0,40,85,0.10);
    border: 2px solid #e30613;
    padding: 18px 16px 12px 16px;
    margin-bottom: 28px;
}
.title {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 2rem;
    color: #002855;
    font-weight: bold;
    margin-bottom: 8px;
}
.subtitle {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 1.2rem;
    color: #e30613;
    margin-bottom: 12px;
}
.btn {
    background-color: #e30613;
    color: #fff;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 1rem;
    font-family: 'Segoe UI', Arial, sans-serif;
    border: none;
    cursor: pointer;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)
with col1:
    # Gráfico de barras: total de delitos por ciudad
    st.markdown("<div class='card' style='text-align:center;'><div class='title'>Total de delitos por ciudad</div>", unsafe_allow_html=True)
    fig_total, ax_total = plt.subplots(figsize=(5,3), facecolor='#fff')
    ax_total.bar(ciudades, delitos_reportados, color='#e30613', edgecolor='#002855', linewidth=1.5)
    ax_total.set_ylabel('Cantidad', fontsize=12, fontweight='bold', fontname='Arial')
    ax_total.set_xlabel('Ciudad', fontsize=12, fontweight='bold', fontname='Arial')
    ax_total.set_title('Total de delitos por ciudad', color='#002855', fontsize=14, fontweight='bold', fontname='Arial', pad=16)
    ax_total.tick_params(colors='#002855', labelsize=11)
    for label in ax_total.get_xticklabels() + ax_total.get_yticklabels():
        label.set_fontsize(11)
        label.set_fontname('Arial')
    fig_total.patch.set_facecolor('#fff')
    ax_total.spines['top'].set_visible(False)
    ax_total.spines['right'].set_visible(False)
    ax_total.spines['left'].set_color('#002855')
    ax_total.spines['bottom'].set_color('#002855')
    # Etiquetas de valores sobre las barras
    for i, v in enumerate(delitos_reportados):
        ax_total.text(i, v + 20, str(v), ha='center', va='bottom', color='#e30613', fontweight='bold', fontsize=11)
    st.pyplot(fig_total, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # Gráfico de barras por delitos en cada ciudad
    st.markdown("<div class='card' style='text-align:center;'><div class='title'>Delitos por tipo y ciudad</div>", unsafe_allow_html=True)
    # Datos de ejemplo para delitos por ciudad
    delitos_ciudad = {
        'Bogotá': [700, 300, 150, 50],
        'Medellín': [500, 250, 150, 50],
        'Cali': [400, 200, 150, 50],
        'Barranquilla': [300, 200, 80, 20],
        'Cartagena': [200, 100, 80, 20]
    }
    fig3, ax3 = plt.subplots(figsize=(6,3), facecolor='#fff')
    width = 0.18
    x = range(len(ciudades))
    for i, delito in enumerate(delitos):
        valores = [delitos_ciudad[ciudad][i] for ciudad in ciudades]
        ax3.bar([p + i*width for p in x], valores, width=width, label=delito)
    ax3.set_xticks([p + 1.5*width for p in x])
    ax3.set_xticklabels(ciudades, fontsize=11, fontname='Arial')
    ax3.set_ylabel('Cantidad', fontsize=12, fontweight='bold', fontname='Arial')
    ax3.set_xlabel('Ciudad', fontsize=12, fontweight='bold', fontname='Arial')
    ax3.set_title('Delitos por tipo y ciudad', color='#e30613', fontsize=14, fontweight='bold', fontname='Arial', pad=16)
    ax3.legend(title="Delito", fontsize=9)
    fig3.patch.set_facecolor('#fff')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#002855')
    ax3.spines['bottom'].set_color('#002855')
    st.pyplot(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='card' style='text-align:center;'><div class='title'>Distribución de delitos</div>", unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(3,3), facecolor='#181c2b')
    wedges, texts, autotexts = ax2.pie(delitos_cant, labels=delitos, autopct='%1.1f%%', colors=['#ff3b3b','#00eaff','#ffb700','#00ffae'], wedgeprops={'edgecolor':'#fff','linewidth':1.2}, startangle=90)
    for text in texts:
        text.set_fontsize(11)
    fig2.patch.set_facecolor('#181c2b')
    ax2.set_title('Distribución de Delitos', color='#ffb700', fontsize=10, fontweight='bold', fontname='Arial')
    # Leyenda fuera del gráfico
    ax2.legend(wedges, delitos, title="Delitos", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7)
    st.pyplot(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'><div class='title'>Mapa de delitos por ciudad</div>", unsafe_allow_html=True)
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
    st_folium(mapa, width=480, height=320)
    st.markdown("</div>", unsafe_allow_html=True)

# Botón para descargar informe
st.markdown("<div class='card'><div class='title'>Generar informe tipo Word</div>", unsafe_allow_html=True)
if st.button("Descargar informe", key="neon-btn"):
    from docx import Document
    doc = Document()
    doc.add_heading('INFORME DE GESTIÓN 2022-2025', 0)
    doc.add_paragraph('Fiscalía General de la Nación')

    # Redacción automática con IA y análisis avanzado
    total_delitos = sum(delitos_reportados)
    total_casos = sum(delitos_cant)
    ciudad_max = ciudades[delitos_reportados.index(max(delitos_reportados))]
    ciudad_min = ciudades[delitos_reportados.index(min(delitos_reportados))]
    delito_max = delitos[delitos_cant.index(max(delitos_cant))]
    delito_min = delitos[delitos_cant.index(min(delitos_cant))]

    # Ranking de ciudades
    ranking_ciudades = sorted(zip(ciudades, delitos_reportados), key=lambda x: x[1], reverse=True)
    ranking_delitos = sorted(zip(delitos, delitos_cant), key=lambda x: x[1], reverse=True)

    resumen = f"Durante el periodo 2020-2024, la Fiscalía General de la Nación gestionó un total de {total_delitos} delitos reportados en las principales ciudades del país. "
    resumen += f"La ciudad con mayor incidencia fue {ciudad_max} ({max(delitos_reportados)} casos, {max(delitos_reportados)/total_delitos:.1%} del total), mientras que la de menor incidencia fue {ciudad_min} ({min(delitos_reportados)} casos, {min(delitos_reportados)/total_delitos:.1%}). "
    resumen += "Los delitos más frecuentes fueron: " + ", ".join([f"{delito} ({cant})" for delito, cant in ranking_delitos]) + ". "
    resumen += "El análisis de estos datos permite identificar tendencias y orientar estrategias institucionales para la prevención y judicialización de los delitos más relevantes."
    doc.add_paragraph(resumen)

    doc.add_paragraph('Ranking de ciudades por cantidad de delitos reportados:')
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Posición'
    hdr_cells[1].text = 'Ciudad'
    hdr_cells[2].text = 'Delitos reportados'
    for idx, (ciudad, cantidad) in enumerate(ranking_ciudades, 1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = ciudad
        row_cells[2].text = str(cantidad)

    doc.add_paragraph('Ranking de delitos por frecuencia:')
    table2 = doc.add_table(rows=1, cols=3)
    hdr2 = table2.rows[0].cells
    hdr2[0].text = 'Posición'
    hdr2[1].text = 'Delito'
    hdr2[2].text = 'Casos reportados'
    for idx, (delito, cant) in enumerate(ranking_delitos, 1):
        row_cells = table2.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = delito
        row_cells[2].text = str(cant)

    doc.add_paragraph('Distribución porcentual de delitos por ciudad:')
    for ciudad, cantidad in ranking_ciudades:
        doc.add_paragraph(f"- {ciudad}: {cantidad} casos ({cantidad/total_delitos:.1%})")

    doc.add_paragraph('Distribución porcentual de delitos por tipo:')
    for delito, cant in ranking_delitos:
        doc.add_paragraph(f"- {delito}: {cant} casos ({cant/total_casos:.1%})")

    # Recomendaciones automáticas
    recomendaciones = []
    if max(delitos_reportados)/total_delitos > 0.35:
        recomendaciones.append(f"Se recomienda focalizar recursos y estrategias en la ciudad de {ciudad_max}, que concentra más del 35% de los delitos reportados.")
    if max(delitos_cant)/total_casos > 0.5:
        recomendaciones.append(f"El delito de mayor frecuencia es {delito_max}, representando más del 50% de los casos. Es prioritario fortalecer acciones preventivas y de investigación en este tipo de delito.")
    if not recomendaciones:
        recomendaciones.append("La distribución de delitos es relativamente equilibrada entre ciudades y tipos, se recomienda mantener el monitoreo y ajustar estrategias según nuevas tendencias.")
    doc.add_paragraph('Recomendaciones automáticas:')
    for rec in recomendaciones:
        doc.add_paragraph(f"- {rec}")

    conclusion = f"En conclusión, el periodo analizado evidencia que {ciudad_max} requiere especial atención por su alta incidencia delictiva, mientras que el delito más frecuente es {delito_max}. La Fiscalía continuará fortaleciendo sus capacidades investigativas y preventivas para mejorar la seguridad ciudadana."
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
