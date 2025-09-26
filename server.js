// Backend Node.js para proxy de Cohere
const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const COHERE_API_KEY = process.env.COHERE_API_KEY || 'TU_API_KEY_AQUI';

app.post('/generar-informe', async (req, res) => {
    const { prompt } = req.body;
    try {
        const response = await fetch('https://api.cohere.ai/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${COHERE_API_KEY}`
            },
            body: JSON.stringify({
                model: 'command',
                prompt: prompt,
                max_tokens: 800,
                temperature: 0.7
            })
        });
        const data = await response.json();
        res.json({ informe: data.generations?.[0]?.text || 'No se obtuvo respuesta de la IA.' });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Servidor backend escuchando en puerto ${PORT}`);
});
