const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Puxa o token e limpa espaços ou prefixos acidentais
const GITHUB_TOKEN = process.env.GITHUB_TOKEN 
    ? process.env.GITHUB_TOKEN.replace(/token\s+/i, '').trim() 
    : "";

const REPO_OWNER = 'azdevcoder';
const REPO_NAME = 'azdevcoder_notes';
const PATH = 'notes';
const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${PATH}`;

// Rota de diagnóstico para testar no navegador
app.get('/', (req, res) => {
    res.json({ 
        status: "Servidor Online", 
        token_detectado: GITHUB_TOKEN.length > 0,
        prefixo: GITHUB_TOKEN.substring(0, 4),
        repositorio: `${REPO_OWNER}/${REPO_NAME}`
    });
});

// Rota principal do Proxy
app.all('/api/notes*', async (req, res) => {
    let subPath = req.params[0] || ""; 
    if (subPath && !subPath.startsWith('/')) subPath = '/' + subPath;

    const url = `${BASE_URL}${subPath}`;

    try {
        const response = await axios({
            method: req.method,
            url: url,
            data: req.body,
            headers: {
                "Authorization": `token ${GITHUB_TOKEN}`,
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AzDev-Proxy-App"
            }
        });
        res.status(response.status).json(response.data);
    } catch (error) {
        console.error("Erro GitHub:", error.response?.data || error.message);
        res.status(error.response?.status || 500).json(
            error.response?.data || { error: "Erro interno no servidor" }
        );
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Rodando na porta ${PORT}`));
