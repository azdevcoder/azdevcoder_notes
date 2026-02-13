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

// Configuração padrão do cabeçalho
const headers = {
    "Authorization": `token ${GITHUB_TOKEN}`,
    "Content-Type": "application/json"
};

// Rota para listar e salvar (Proxy)
app.all('/api/notes*', async (req, res) => {
    const subPath = req.params[0] || ""; // Pega o nome do arquivo se houver
    const url = `${BASE_URL}${subPath}${req.url.includes('?t=') ? req.url.substring(req.url.indexOf('?t=')) : ''}`;

    try {
        const response = await axios({
            method: req.method,
            url: url,
            data: req.body,
            headers: headers
        });
        res.status(response.status).json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || {error: "Erro no servidor"});
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor AzDev Coder rodando na porta ${PORT}`));
