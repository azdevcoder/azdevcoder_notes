const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Puxa o token e remove qualquer espaço acidental
const GITHUB_TOKEN = process.env.GITHUB_TOKEN ? process.env.GITHUB_TOKEN.trim() : "";
const REPO_OWNER = 'azdevcoder';
const REPO_NAME = 'azdevcoder_notes';
const PATH = 'notes';

const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${PATH}`;

// Rota de Diagnóstico: Abra https://seu-app.onrender.com no navegador
app.get('/', (req, res) => {
    res.json({ 
        status: "Online", 
        token_carregado: GITHUB_TOKEN.length > 0,
        prefixo_token: GITHUB_TOKEN.substring(0, 4),
        endpoint_correto: "/api/notes"
    });
});

app.all('/api/notes*', async (req, res) => {
    // Pega o que vem após /api/notes (ex: /arquivo.md)
    let subPath = req.params[0] || ""; 
    
    // Garante que o caminho comece com barra se houver um arquivo
    if (subPath && !subPath.startsWith('/')) {
        subPath = '/' + subPath;
    }

    const url = `${BASE_URL}${subPath}`;

    try {
        const response = await axios({
            method: req.method,
            url: url,
            data: req.body,
            headers: {
                "Authorization": `token ${GITHUB_TOKEN}`,
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AzDev-Notes-App"
            }
        });
        res.status(response.status).json(response.data);
    } catch (error) {
        console.error("Erro no Proxy:", error.response?.data || error.message);
        res.status(error.response?.status || 500).json(
            error.response?.data || { error: "Erro interno no servidor proxy" }
        );
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
