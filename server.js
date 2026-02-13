const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Puxa o token das Variáveis de Ambiente do Render
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO_OWNER = 'azdevcoder';
const REPO_NAME = 'azdevcoder_notes';
const PATH = 'notes';

const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${PATH}`;

app.all('/api/notes*', async (req, res) => {
    // Captura o nome do arquivo que vem após /api/notes
    const subPath = req.params[0] || ""; 
    const url = `${BASE_URL}${subPath}`;

    try {
        const response = await axios({
            method: req.method,
            url: url,
            data: req.body,
            headers: {
                "Authorization": `token ${GITHUB_TOKEN}`,
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AzDev-Notes-App" // O GitHub exige um User-Agent
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
app.listen(PORT, () => console.log(`Servidor AzDev Coder seguro rodando na porta ${PORT}`));
