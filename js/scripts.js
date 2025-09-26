// Gráficos con datos simulados
const barChart = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena'],
        datasets: [{
            label: 'Delitos reportados',
            data: [120, 90, 70, 50, 40],
            backgroundColor: [
                '#00eaff', // Bogotá
                '#ffb700', // Medellín
                '#ff3b3b', // Cali
                '#00ffae', // Barranquilla
                '#2c5364'  // Cartagena
            ],
            borderColor: [
                '#00b3ff',
                '#c97c00',
                '#b80000',
                '#009e7a',
                '#1a2a3a'
            ],
            borderWidth: 2
        }]
    },
    options: {
        plugins: {
            legend: { labels: { color: '#00ffae' } }
        },
        scales: {
            x: { ticks: { color: '#00eaff' } },
            y: { ticks: { color: '#00eaff' } }
        }
    }
});

const pieChart = new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
        labels: ['Hurto', 'Homicidio', 'Fraude', 'Secuestro'],
        datasets: [{
            data: [60, 25, 10, 5],
            backgroundColor: [
                '#ff3b3b', // Hurto
                '#00eaff', // Homicidio
                '#ffb700', // Fraude
                '#00ffae'  // Secuestro
            ],
            borderColor: [
                '#b80000',
                '#00b3ff',
                '#c97c00',
                '#009e7a'
            ],
            borderWidth: 2
        }]
    },
    options: {
        plugins: {
            legend: { labels: { color: '#00ffae' } }
        }
    }
});

    // Función para procesar archivo cargado y actualizar gráficos/mapa
    document.getElementById('fileInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(evt) {
            let data;
            // Procesamiento básico para CSV y JSON
            if (file.name.endsWith('.json')) {
                try {
                    data = JSON.parse(evt.target.result);
                } catch (err) {
                    alert('Archivo JSON inválido');
                    return;
                }
            } else if (file.name.endsWith('.csv')) {
                const lines = evt.target.result.split('\n').map(l => l.trim()).filter(l => l);
                // Espera formato: ciudad,delito,cantidad
                data = lines.slice(1).map(line => {
                    const [ciudad, delito, cantidad] = line.split(',');
                    return { ciudad, delito, cantidad: Number(cantidad) };
                });
            } else {
                alert('Solo se soportan archivos CSV y JSON en esta demo.');
                return;
            }
            // Agrupar datos por ciudad y delito
            const ciudades = {};
            const delitos = {};
            data.forEach(d => {
                if (!ciudades[d.ciudad]) ciudades[d.ciudad] = 0;
                ciudades[d.ciudad] += d.cantidad;
                if (!delitos[d.delito]) delitos[d.delito] = 0;
                delitos[d.delito] += d.cantidad;
            });
            // Actualizar gráfico de barras
            barChart.data.labels = Object.keys(ciudades);
            barChart.data.datasets[0].data = Object.values(ciudades);
            // Colores dinámicos
            barChart.data.datasets[0].backgroundColor = barChart.data.labels.map((_,i)=>['#00eaff','#ffb700','#ff3b3b','#00ffae','#2c5364','#b80000','#00b3ff','#c97c00','#009e7a','#1a2a3a'][i%10]);
            barChart.update();
            // Actualizar gráfico de torta
            pieChart.data.labels = Object.keys(delitos);
            pieChart.data.datasets[0].data = Object.values(delitos);
            pieChart.data.datasets[0].backgroundColor = pieChart.data.labels.map((_,i)=>['#ff3b3b','#00eaff','#ffb700','#00ffae','#b80000','#00b3ff','#c97c00','#009e7a'][i%8]);
            pieChart.update();
            // Actualizar mapa
            if (mapInstance) {
                mapInstance.eachLayer(layer => {
                    if (layer instanceof L.Marker) mapInstance.removeLayer(layer);
                });
                Object.entries(ciudades).forEach(([ciudad, cantidad]) => {
                    // Coordenadas simuladas para demo
                    const coords = {
                        'Bogotá': [4.7110, -74.0721],
                        'Medellín': [6.2442, -75.5812],
                        'Cali': [3.4516, -76.5320],
                        'Barranquilla': [10.9685, -74.7813],
                        'Cartagena': [10.3910, -75.4794]
                    };
                    if (coords[ciudad]) {
                        L.marker(coords[ciudad]).addTo(mapInstance)
                            .bindPopup(`<b>${ciudad}</b><br>Delitos: ${cantidad}`);
                    }
                });
            }
        };
        reader.readAsText(file);
    });

// Mapa de Colombia con Leaflet y datos simulados
let mapInitialized = false;
let mapInstance = null;
function toggleMapa() {
    const mapDiv = document.getElementById('map');
    if (mapDiv.style.display === 'none' || mapDiv.style.display === '') {
        mapDiv.style.display = 'block';
        if (!mapInitialized) {
            mapInstance = L.map('map').setView([4.5709, -74.2973], 5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(mapInstance);
            const ciudades = [
                { nombre: 'Bogotá', coords: [4.7110, -74.0721], delitos: 120 },
                { nombre: 'Medellín', coords: [6.2442, -75.5812], delitos: 90 },
                { nombre: 'Cali', coords: [3.4516, -76.5320], delitos: 70 },
                { nombre: 'Barranquilla', coords: [10.9685, -74.7813], delitos: 50 },
                { nombre: 'Cartagena', coords: [10.3910, -75.4794], delitos: 40 }
            ];
            ciudades.forEach(c => {
                L.marker(c.coords).addTo(mapInstance)
                    .bindPopup(`<b>${c.nombre}</b><br>Delitos: ${c.delitos}`);
            });
            mapInitialized = true;
        } else {
            setTimeout(() => { mapInstance.invalidateSize(); }, 200);
        }
    } else {
        mapDiv.style.display = 'none';
    }
}

document.getElementById('btnGeo').addEventListener('click', toggleMapa);

// Función para el botón de informe detallado
const btnInforme = document.getElementById('btnInforme');
btnInforme.addEventListener('click', async () => {
        const fecha = new Date().toLocaleDateString('es-CO');
        const ciudades = [
                { nombre: 'Bogotá', delitos: 120 },
                { nombre: 'Medellín', delitos: 90 },
                { nombre: 'Cali', delitos: 70 },
                { nombre: 'Barranquilla', delitos: 50 },
                { nombre: 'Cartagena', delitos: 40 }
        ];
            let indicadores = ciudades.map(c => `<tr><td>${c.nombre}</td><td>${c.delitos}</td></tr>`).join('');

            // Captura los gráficos como imágenes base64
            function getChartImage(chartId) {
                    const canvas = document.getElementById(chartId);
                    return canvas ? canvas.toDataURL('image/png') : '';
            }
            const barImg = getChartImage('barChart');
            const pieImg = getChartImage('pieChart');

                // Obtener el logo como base64
        // Usar logo en línea para asegurar visualización
        const logoURL = 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Fiscalia_General_de_la_Nacion_de_Colombia_logo.png';

        let informe = `
    <div style='text-align:center;margin-bottom:20px;'>
        <img src='${logoURL}' alt='Logo Fiscalía' style='height:110px;'/>
    </div>
        <h1 style='text-align:center;'>INFORME DE GESTIÓN 2020-2024</h1>
        <h2 style='text-align:center;'>Fiscalía General de la Nación</h2>
        <h3 style='text-align:center;'>Balance de la Administración</h3>
        <p><b>Fecha:</b> ${fecha}</p>
        <h3>Contenido</h3>
        <ul>
            <li>Presentación y contenido</li>
            <li>¿QUÉ LOGRAMOS?</li>
            <li>¿CÓMO LO LOGRAMOS?</li>
            <li>¿DÓNDE SE MATERIALIZAN NUESTRAS ACCIONES?</li>
        </ul>
        <h3>Presentación</h3>
        <p>El 13 de febrero de 2020, inicia nuestra administración, enfrentando los retos del contexto social y político de Colombia y la criminalidad. Este informe da cuenta de los resultados brindados por la ejecución de los direccionamientos estratégicos, destacando logros cuantitativos y cualitativos, y presentando casos emblemáticos que ejemplarizan el esfuerzo institucional.</p>
        <h3>¿QUÉ LOGRAMOS?</h3>
        <p>Se destacan los logros misionales y operativos obtenidos, con especial enfoque en los resultados acumulados "en la calle y en los territorios".</p>
        <h4>Principales cifras de los resultados de la gestión 2020 – 2024</h4>
        <table border='1' cellpadding='4' style='border-collapse:collapse;'>
            <tr><th>Ciudad</th><th>Delitos reportados</th></tr>
            ${indicadores}
        </table>
        <div style='text-align:center;margin:20px 0;'>
            <b>Gráfico de barras:</b><br>
            <img src='${barImg}' style='max-width:500px;'/>
        </div>
        <h4>Resultados para la Seguridad Territorial</h4>
        <ul>
            <li><b>Homicidio doloso:</b> Tasa de esclarecimiento acumulada del 43,53%.</li>
            <li><b>Violencia sexual e intrafamiliar:</b> Estrategias implementadas para mejorar el esclarecimiento.</li>
            <li><b>Hurto violento:</b> Trabajo estratégico para alcanzar niveles históricos de avance.</li>
            <li><b>Maltrato animal:</b> Priorización de investigaciones relevantes.</li>
            <li><b>Protección de pueblos indígenas:</b> Fortalecimiento de la respuesta institucional.</li>
        </ul>
        <div style='text-align:center;margin:20px 0;'>
            <b>Gráfico de torta:</b><br>
            <img src='${pieImg}' style='max-width:400px;'/>
        </div>
        <h4>Resultados en la lucha contra la criminalidad organizada</h4>
        <ul>
            <li>Desmantelamiento de estructuras criminales.</li>
            <li>Impacto a Grupos Armados Organizados y Grupos de Delincuencia Organizada.</li>
            <li>Resultados en delitos informáticos y narcotráfico.</li>
        </ul>
        <h4>Resultados en la lucha contra la corrupción</h4>
        <ul>
            <li>Judicialización de servidores públicos y casos relevantes.</li>
        </ul>
        <h3>¿CÓMO LO LOGRAMOS?</h3>
        <div class='section'>
        <p>Más allá de las cifras, los resultados operativos y estratégicos de nuestra administración han sido posibles gracias a la implementación de estrategias del Direccionamiento Estratégico “En la calle y los territorios”, ejecutadas por las distintas dependencias de la Fiscalía General de la Nación. Los datos presentados en los gráficos del informe reflejan el impacto de estas acciones en las principales ciudades del país y en los delitos priorizados.</p>
        <p><b>Enfoque territorial:</b> El análisis de los delitos reportados en ciudades como Bogotá (120 casos), Medellín (90), Cali (70), Barranquilla (50) y Cartagena (40) evidencia la focalización de esfuerzos en los territorios con mayor incidencia criminal. La metodología de proyectos y microproyectos investigativos permitió intervenir situaciones específicas, caracterizar el comportamiento delictivo y generar alertas para la focalización de la investigación.</p>
        <p><b>Monitoreo y acompañamiento regional:</b> Se agruparon las direcciones seccionales en regiones estratégicas, asignando fiscales padrinos y madrinas para el acompañamiento y asesoría en la gestión de casos complejos, lo que contribuyó al esclarecimiento de delitos como homicidio doloso y hurto violento, presentes en los gráficos.</p>
        <p><b>Transferencia de conocimiento y articulación:</b> La coordinación entre el nivel central y las regiones permitió la transferencia de metodologías investigativas y la aplicación de estrategias diferenciadas para delitos como violencia sexual, intrafamiliar y feminicidio, que se reflejan en la distribución de delitos del gráfico de torta.</p>
        <p><b>Innovación y fortalecimiento de la investigación:</b> Se implementaron herramientas analíticas y tecnológicas para el seguimiento de fenómenos criminales, lo que facilitó la identificación de patrones y la toma de decisiones informadas. El trabajo itinerante y la presencia institucional en zonas de difícil acceso fortalecieron la capacidad de respuesta y el acceso a la justicia.</p>
        <p><b>Impacto en la seguridad ciudadana:</b> Los resultados visualizados en los gráficos muestran avances en el esclarecimiento de homicidios, violencia sexual, hurto y otros delitos, gracias a la priorización de casos y la articulación interinstitucional. La estrategia de rutas itinerantes permitió atender poblaciones vulnerables y mejorar la atención a víctimas en todo el territorio nacional.</p>
        <p>En conclusión, la gestión integral y el enfoque territorial han sido claves para alcanzar los resultados históricos presentados, consolidando el compromiso de la Fiscalía General de la Nación con la seguridad ciudadana y la reducción de los índices delictivos.</p>
        </div>
        <h3>¿DÓNDE SE MATERIALIZAN NUESTRAS ACCIONES?</h3>
        <ul>
            <li>Afectaciones a la seguridad ciudadana: homicidios, violencia sexual, hurtos, estafa, maltrato animal.</li>
            <li>Corrupción y crimen organizado.</li>
            <li>Medio ambiente, delitos informáticos y narcotráfico.</li>
            <li>Protesta social, trata de personas y justicia transicional.</li>
        </ul>
        <p style='margin-top:30px;'><b>Conclusión:</b> La Fiscalía General de la Nación reitera su compromiso con la seguridad ciudadana y la reducción de los índices delictivos, promoviendo acciones coordinadas y el uso de herramientas tecnológicas para la gestión eficiente de la información.</p>
        `;

                        // HTML robusto para Word, con estilos y formato compatible
                        const wordHTML = `
<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
    <meta charset='utf-8'>
    <title>Informe de Gestión Fiscalía</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1, h2, h3 { text-align: center; }
        table { border-collapse: collapse; width: 80%; margin: 0 auto; }
        th, td { border: 1px solid #333; padding: 6px; }
        .img-center { display: block; margin: 0 auto; }
        .section { margin-bottom: 30px; }
    </style>
</head>
<body>
${informe}
</body>
</html>`;
                        const blob = new Blob([wordHTML], { type: 'application/msword' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'Informe_Gestion_Fiscalia.doc';
                        document.body.appendChild(a);
                        a.click();
                        setTimeout(() => {
                                document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                        }, 100);
});
