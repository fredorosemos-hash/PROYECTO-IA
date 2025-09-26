st.markdown(
    """
        margin-bottom: 32px;
        border: 2px solid #00eaff;
    }
    .neon-title {
        font-family: 'Orbitron', 'Segoe UI', sans-serif;
        font-size: 2.5rem;
        with col1:
            st.markdown("<div class='neon-box' style='text-align:center;'><h2 class='neon-title'>Delitos por ciudad</h2>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5,3), facecolor='#181c2b')
            bars = ax.bar(ciudades, delitos_reportados, color=['#00eaff','#ffb700','#ff3b3b','#00ffae','#2c5364'], edgecolor='#fff', linewidth=1.2)
            ax.set_ylabel('Cantidad', color='#00eaff', fontsize=12, fontweight='bold', fontname='Arial')
            ax.set_xlabel('Ciudad', color='#00eaff', fontsize=12, fontweight='bold', fontname='Arial')
            ax.set_title('Delitos por Ciudad', color='#ffb700', fontsize=14, fontweight='bold', fontname='Arial', pad=16)
            ax.tick_params(colors='#fff', labelsize=11)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(11)
                label.set_fontname('Arial')
            fig.patch.set_facecolor('#181c2b')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#00eaff')
            ax.spines['bottom'].set_color('#00eaff')
            # Etiquetas de valores sobre las barras
            for bar in bars:
                ax.annotate(f'{bar.get_height()}',
                            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            xytext=(0, 6),
                            textcoords="offset points",
                            ha='center', va='bottom', color='#fff', fontsize=11, fontweight='bold')
            st.pyplot(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='neon-box' style='text-align:center;'><h2 class='neon-title'>Distribución de delitos</h2>", unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(3,3), facecolor='#181c2b')
            wedges, texts, autotexts = ax2.pie(delitos_cant, labels=delitos, autopct='%1.1f%%', colors=['#ff3b3b','#00eaff','#ffb700','#00ffae'], wedgeprops={'edgecolor':'#fff','linewidth':1.2}, startangle=90)
            for text in texts:
                text.set_fontsize(11)
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
                }
                </style>
                <link href="https://fonts.googleapis.com/css?family=Orbitron:700" rel="stylesheet">
                """,
                    unsafe_allow_html=True
                )
        text.set_fontname('Arial')
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color('#ffb700')
        autotext.set_fontname('Arial')
    fig2.patch.set_facecolor('#181c2b')
    ax2.set_title('Distribución de Delitos', color='#ffb700', fontsize=10, fontweight='bold', fontname='Arial')
    # Leyenda fuera del gráfico
    ax2.legend(wedges, delitos, title="Delitos", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7)
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
    st_folium(mapa, width=480, height=320)
    st.markdown("</div>", unsafe_allow_html=True)

# Botón para descargar informe
st.markdown("<div class='neon-box'><h2 class='neon-title'>Generar informe tipo Word</h2>", unsafe_allow_html=True)
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
