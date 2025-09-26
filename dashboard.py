
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
st.markdown("""
<div style='width:100%;background:#e30613;padding:0;margin:0;'>
    <marquee behavior='scroll' direction='left' style='color:#fff;font-size:1.3rem;font-family:Segoe UI,Arial,sans-serif;font-weight:bold;padding:8px 0;'>
        PROYECTO TALENTO TECH REGION 2 FISCALIA GENERAL DE LA NACION
    </marquee>
</div>
""", unsafe_allow_html=True)
st.markdown(f"""
<div style='background:#fff; border:2px solid #e30613; border-radius:12px; width:240px; margin:18px auto 10px auto; padding:10px;'>
    <img src='{LOGO_FISCALIA}' alt='Logo Fiscalía' style='width:220px; display:block; margin:auto;'>
</div>
""", unsafe_allow_html=True)
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
    font-size: 1.15rem;
    color: #002855;
    font-weight: bold;
    margin-bottom: 6px;
    text-transform: uppercase;
    text-align: center;
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
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches
    import matplotlib.pyplot as plt
    import io

    doc = Document()
    # Título principal
    title = doc.add_heading('INFORME DE GESTIÓN 2022-2025', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    run = subtitle.add_run('Fiscalía General de la Nación')
    run.bold = True
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Análisis automático
    total_delitos = sum(delitos_reportados)
    total_casos = sum(delitos_cant)
    ciudad_max = ciudades[delitos_reportados.index(max(delitos_reportados))]
    ciudad_min = ciudades[delitos_reportados.index(min(delitos_reportados))]
    delito_max = delitos[delitos_cant.index(max(delitos_cant))]
    delito_min = delitos[delitos_cant.index(min(delitos_cant))]
    ranking_ciudades = sorted(zip(ciudades, delitos_reportados), key=lambda x: x[1], reverse=True)
    ranking_delitos = sorted(zip(delitos, delitos_cant), key=lambda x: x[1], reverse=True)

    # Resumen
    resumen = doc.add_paragraph()
    resumen.add_run('Resumen Ejecutivo').bold = True
    resumen.alignment = WD_ALIGN_PARAGRAPH.CENTER
    texto = doc.add_paragraph(
        f"Durante el periodo 2020-2024, la Fiscalía General de la Nación gestionó un total de {total_delitos} delitos reportados en las principales ciudades del país. "
        f"La ciudad con mayor incidencia fue {ciudad_max} ({max(delitos_reportados)} casos, {max(delitos_reportados)/total_delitos:.1%} del total), mientras que la de menor incidencia fue {ciudad_min} ({min(delitos_reportados)} casos, {min(delitos_reportados)/total_delitos:.1%}). "
        "Los delitos más frecuentes fueron: " + ", ".join([f"{delito} ({cant})" for delito, cant in ranking_delitos]) + ". "
        "El análisis de estos datos permite identificar tendencias y orientar estrategias institucionales para la prevención y judicialización de los delitos más relevantes."
    )
    texto.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Sección institucional: Cartilla 5
    cartilla_title = doc.add_paragraph()
    run_cartilla = cartilla_title.add_run('CARTILLA 5: HERRAMIENTAS ANALÍTICAS PARA LA INVESTIGACIÓN Y EL EJERCICIO DE LA ACCIÓN PENAL')
    run_cartilla.bold = True
    cartilla_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cartilla_text = (
        "La política de priorización implica una aproximación analítica y rigurosa a la investigación y al ejercicio de la acción penal. Contribuye al planteamiento de hipótesis delictivas que puedan ser confirmadas o rechazadas a medida que avanza la investigación.\n\n"
        "La resolución 1343 de 2014 establece actividades de priorización respecto a situaciones y casos: fijar un orden en el que serán atendidos; destinar más funcionarios y herramientas; agrupar e investigar casos asociados; aplicar herramientas analíticas en el trámite, investigación y judicialización; enfocar esfuerzos en ciertos casos o hechos delictivos y en algunos presuntos responsables. Tres de las seis actividades proponen el uso del análisis en contexto y la focalización de la investigación y la acción penal en hechos y responsables.\n\n"
        "Esta cartilla presenta cinco herramientas analíticas para analistas criminales, fiscales, investigadores y asistentes de fiscal. Todas son de fácil uso, retoman la forma de analizar la información con la que cuenta la Fiscalía e indican fuentes que pueden contribuir a una investigación más integral. No reemplazan la labor investigativa de la policía judicial.\n\n"
        "Las cinco herramientas parten de tres cambios metodológicos fundamentales:\n"
        "1. Ampliar el foco de la investigación: reconocer que los hechos delictivos no ocurren de manera aislada sino que se explican por su contexto y plantear hipótesis de trabajo para ser confirmadas o rechazadas a través del análisis de la información y evidencia disponibles.\n"
        "2. Disponer de diversas fuentes de información y ser riguroso con su uso: analizar elementos materiales probatorios (EMP), evidencia física (EF) e información de fuentes formales y no formales sobre los hechos y su contexto.\n"
        "3. Utilizar otras disciplinas para explicar fenómenos criminales, situaciones y casos: incluir la aproximación de las ciencias sociales y exactas para comprender el delito e ilustrar la teoría del caso.\n\n"
        "Las herramientas contribuyen a la toma de decisiones de priorización y facilitan el diseño de hipótesis criminales y estrategias de persecución en las diferentes etapas de la investigación, independientemente del régimen procesal. La identificación de fenómenos criminales y la delimitación de situaciones y asociación de casos permiten determinar relaciones entre investigaciones y delitos no denunciados, focalizar la atención en grupos de casos no aislados, distribuir eficazmente recursos y talento humano, y plantear la teoría del caso en etapas preliminares. Las otras tres herramientas aportan elementos para la caracterización de hechos delictivos y actores (víctimas y responsables), útiles en momentos posteriores de la investigación. Permiten focalizar decisiones sobre hechos y personas según criterios de priorización y alimentar la comprensión de la evidencia recolectada.\n\n"
        "Las herramientas son:\n"
        "- Identificación de fenómenos criminales y estudio de resultados.\n"
        "- Delimitación de situación y asociación de casos.\n"
        "- Caracterización de situaciones a partir de prácticas y patrones criminales.\n"
        "- Caracterización de víctimas.\n"
        "- Caracterización de estructuras criminales.\n\n"
        "Estas herramientas permiten investigaciones integrales, rigurosas y estratégicas, orientadas a la priorización y judicialización efectiva."
    )
    cartilla_paragraph = doc.add_paragraph(cartilla_text)
    cartilla_paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Gráfico de barras: total de delitos por ciudad
    fig, ax = plt.subplots(figsize=(5,3))
    ax.bar(ciudades, delitos_reportados, color='#e30613', edgecolor='#002855', linewidth=1.5)
    ax.set_ylabel('Cantidad', fontsize=12, fontweight='bold', fontname='Arial')
    ax.set_xlabel('Ciudad', fontsize=12, fontweight='bold', fontname='Arial')
    ax.set_title('Total de delitos por ciudad', fontsize=14, fontweight='bold', fontname='Arial', pad=16)
    ax.tick_params(labelsize=11)
    for i, v in enumerate(delitos_reportados):
        ax.text(i, v + 20, str(v), ha='center', va='bottom', color='#e30613', fontweight='bold', fontsize=11)

    # Título principal
    title = doc.add_heading('INFORME DE GESTIÓN 2022-2025', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    run = subtitle.add_run('Fiscalía General de la Nación')
    run.bold = True
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Resumen ejecutivo
    resumen = doc.add_paragraph()
    resumen.add_run('Resumen Ejecutivo').bold = True
    resumen.alignment = WD_ALIGN_PARAGRAPH.CENTER
    texto = doc.add_paragraph(
        f"Durante el periodo 2020-2024, la Fiscalía General de la Nación gestionó un total de {sum(delitos_reportados)} delitos reportados en las principales ciudades del país. "
        f"La ciudad con mayor incidencia fue {ciudades[delitos_reportados.index(max(delitos_reportados))]} ({max(delitos_reportados)} casos, {max(delitos_reportados)/sum(delitos_reportados):.1%} del total), mientras que la de menor incidencia fue {ciudades[delitos_reportados.index(min(delitos_reportados))]} ({min(delitos_reportados)} casos, {min(delitos_reportados)/sum(delitos_reportados):.1%}). "
        "Los delitos más frecuentes fueron: " + ", ".join([f"{delito} ({cant})" for delito, cant in sorted(zip(delitos, delitos_cant), key=lambda x: x[1], reverse=True)]) + ". "
        "El análisis de estos datos permite identificar tendencias y orientar estrategias institucionales para la prevención y judicialización de los delitos más relevantes."
    )
    texto.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Sección institucional: Cartilla 5
    cartilla_title = doc.add_paragraph()
    run_cartilla = cartilla_title.add_run('CARTILLA 5: HERRAMIENTAS ANALÍTICAS PARA LA INVESTIGACIÓN Y EL EJERCICIO DE LA ACCIÓN PENAL')
    run_cartilla.bold = True
    cartilla_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cartilla_text = '''La política de priorización implica una aproximación analítica y rigurosa a la investigación y al ejercicio de la acción penal. Contribuye al planteamiento de hipótesis delictivas que puedan ser confirmadas o rechazadas a medida que avanza la investigación.
        row_cells[1].text = ciudad
        row_cells[2].text = str(cantidad)

    par2 = doc.add_paragraph()
    par2.add_run('Ranking de delitos por frecuencia:').bold = True
    par2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table2 = doc.add_table(rows=1, cols=3)
    hdr2 = table2.rows[0].cells
    hdr2[0].text = 'Posición'
    hdr2[1].text = 'Delito'
    hdr2[2].text = 'Casos reportados'
    for idx, (delito, cant) in enumerate(ranking_delitos, 1):
        row_cells = table2.add_row().cells
    par3.add_run('Distribución porcentual de delitos por ciudad:').bold = True
    par3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cartilla_paragraph = doc.add_paragraph(cartilla_text)
    cartilla_paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for ciudad, cantidad in ranking_ciudades:
        p = doc.add_paragraph(f"- {ciudad}: {cantidad} casos ({cantidad/total_delitos:.1%})")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    par4 = doc.add_paragraph()
    par4.add_run('Distribución porcentual de delitos por tipo:').bold = True
    par4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for delito, cant in ranking_delitos:
        p = doc.add_paragraph(f"- {delito}: {cant} casos ({cant/total_casos:.1%})")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Recomendaciones automáticas
    recomendaciones = []
    if max(delitos_reportados)/total_delitos > 0.35:
        recomendaciones.append(f"Se recomienda focalizar recursos y estrategias en la ciudad de {ciudad_max}, que concentra más del 35% de los delitos reportados.")
    if max(delitos_cant)/total_casos > 0.5:
        recomendaciones.append(f"El delito de mayor frecuencia es {delito_max}, representando más del 50% de los casos. Es prioritario fortalecer acciones preventivas y de investigación en este tipo de delito.")
    if not recomendaciones:
        recomendaciones.append("La distribución de delitos es relativamente equilibrada entre ciudades y tipos, se recomienda mantener el monitoreo y ajustar estrategias según nuevas tendencias.")
    par5 = doc.add_paragraph()
    par5.add_run('Recomendaciones automáticas:').bold = True
    par5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for rec in recomendaciones:
        p = doc.add_paragraph(f"- {rec}")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    conclusion = doc.add_paragraph()
    conclusion.add_run(f"En conclusión, el periodo analizado evidencia que {ciudad_max} requiere especial atención por su alta incidencia delictiva, mientras que el delito más frecuente es {delito_max}. La Fiscalía continuará fortaleciendo sus capacidades investigativas y preventivas para mejorar la seguridad ciudadana.").bold = True
    conclusion.alignment = WD_ALIGN_PARAGRAPH.CENTER

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
