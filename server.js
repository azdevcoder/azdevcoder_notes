const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO_OWNER = 'azdevcoder';
const REPO_NAME = 'azdevcoder_notes';
const PATH = 'notes';

const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${PATH}`;

// Rota de teste para você abrir no navegador e ver se está online
app.get('/', (req, res) => {
    res.json({ status: "Online", endpoint: "/api/notes" });
});

app.all('/api/notes*', async (req, res) => {
    // Melhoria: Garante que o subPath não venha com barras problemáticas
    let subPath = req.params[0] || ""; 
    
    // Se o subPath não começar com barra e não estiver vazio, adiciona uma
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
                "Authorization": `token ${GITHUB_TOKEN.trim()}`, // .trim() remove espaços acidentais
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
app.listen(PORT, () => console.log(`Servidor AzDev Coder rodando na porta ${PORT}`));
