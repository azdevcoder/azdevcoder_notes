<!DOCTYPE html>
<html lang="pt-br" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AzDev Studio - Python Pro</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/dracula.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.3.0/css/xterm.min.css">

    <style>
        /* --- LAYOUT FIXO (App Style) --- */
        body, html { height: 100%; margin: 0; overflow: hidden; background: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
        .app-container { height: 100vh; display: flex; flex-direction: column; }
        
        /* Navbar Fixa */
        .fixed-header { flex-shrink: 0; z-index: 1000; background: #161b22; border-bottom: 1px solid #30363d; }
        
        /* Área Principal */
        .main-workspace { flex-grow: 1; display: flex; overflow: hidden; position: relative; }
        
        /* Sidebar */
        .sidebar { width: 250px; background: #0d1117; border-right: 1px solid #30363d; display: flex; flex-direction: column; }
        
        /* Coluna do Editor */
        .editor-area { flex-grow: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
        
        /* CodeMirror */
        .editor-wrapper { flex-grow: 1; position: relative; overflow: hidden; }
        .CodeMirror { height: 100% !important; font-family: 'Fira Code', monospace; font-size: 14px; background: #0d1117; }
        
        /* Terminal */
        #terminal-panel { 
            height: 35%; 
            background: #000; 
            border-top: 1px solid #30363d; 
            display: none; 
            flex-direction: column; 
        }
        .show-terminal #terminal-panel { display: flex; }
        .show-terminal .editor-wrapper { height: 65%; } /* Editor diminui quando terminal abre */
        
        #xterm-container { flex-grow: 1; overflow: hidden; padding: 5px; }

        @media (max-width: 768px) { .sidebar { display: none; } }
    </style>
</head>
<body>

<div class="app-container">
    <nav class="navbar navbar-expand-lg fixed-header px-3 py-2">
        <span class="navbar-brand mb-0 h1 text-white fs-6"><i class="bi bi-code-square me-2 text-primary"></i>AzDev Studio</span>
        
        <div class="ms-auto d-flex gap-2">
            <button class="btn btn-sm btn-success fw-bold px-3" onclick="runPython()">
                <i class="bi bi-play-fill me-1"></i> EXECUTAR PYTHON
            </button>
            <button class="btn btn-sm btn-outline-secondary" onclick="toggleTerminal()">
                <i class="bi bi-terminal"></i> Console
            </button>
        </div>
    </nav>

    <div class="main-workspace">
        <div class="sidebar">
            <div class="p-2 border-bottom border-secondary d-flex justify-content-between align-items-center">
                <small class="fw-bold text-muted ps-2">EXPLORER</small>
                <button class="btn btn-link btn-sm text-secondary" onclick="fetchFileList()"><i class="bi bi-arrow-clockwise"></i></button>
            </div>
            <div class="list-group list-group-flush overflow-auto" id="fileList"></div>
        </div>

        <div class="editor-area">
            <div class="d-flex align-items-center gap-2 p-2 bg-dark border-bottom border-secondary fixed-header">
                <input type="text" id="fileName" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="script.py" style="max-width: 250px;">
                <button class="btn btn-sm btn-primary" onclick="saveToGitHub()" title="Salvar na Nuvem"><i class="bi bi-cloud-arrow-up"></i></button>
                <button class="btn btn-sm btn-danger" onclick="deleteFile()" title="Excluir"><i class="bi bi-trash"></i></button>
                <span id="status" class="badge bg-secondary ms-auto">Pronto</span>
            </div>

            <div class="editor-wrapper">
                <textarea id="code-editor"></textarea>
            </div>

            <div id="terminal-panel">
                <div class="d-flex justify-content-between align-items-center bg-dark px-2 py-1 border-bottom border-secondary" style="height: 30px;">
                    <small class="text-success font-monospace"><i class="bi bi-terminal-fill me-2"></i>PYTHON CONSOLE</small>
                    <button class="btn btn-link btn-sm text-secondary p-0" onclick="toggleTerminal()"><i class="bi bi-x-lg"></i></button>
                </div>
                <div id="xterm-container"></div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/mode/python/python.min.js"></script>
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.3.0/lib/xterm.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@xterm/addon-fit@0.8.0/lib/addon-fit.min.js"></script>

<script>
    // --- CONFIGURAÇÕES ---
    const BACKEND_URL = "https://azdevcoder-notes.onrender.com/api/notes";
    let pyodide = null;
    let term = null;
    let fitAddon = null;
    let pythonInputBuffer = "";

    // 1. EDITOR SETUP
    const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
        lineNumbers: true, 
        theme: "dracula", 
        mode: "python",
        indentUnit: 4
    });

    // 2. TERMINAL & PYTHON SETUP
    async function initTerminal() {
        if (term) return; // Já iniciado

        term = new Terminal({
            cursorBlink: true,
            fontSize: 14,
            fontFamily: '"Fira Code", monospace',
            theme: { background: '#000000', foreground: '#00ff00' }
        });

        fitAddon = new FitAddon.FitAddon();
        term.loadAddon(fitAddon);
        term.open(document.getElementById('xterm-container'));
        fitAddon.fit();

        term.writeln('\x1B[1;36mInicializando Python Environment...\x1B[0m');
        
        // Carrega o Pyodide
        try {
            pyodide = await loadPyodide();
            // Redireciona o print() do Python para o Terminal
            pyodide.setStdout({ batched: (msg) => term.writeln(msg) });
            pyodide.setStderr({ batched: (msg) => term.writeln(`\x1B[1;31m${msg}\x1B[0m`) });
            
            term.writeln('\x1B[1;32mPython 3.11 Pronto! Digite código abaixo ou clique em Executar.\x1B[0m');
            term.write('>>> ');
        } catch (e) {
            term.writeln(`\x1B[1;31mErro ao carregar Python: ${e}\x1B[0m`);
        }

        // Lógica de Digitação no Terminal (REPL)
        term.onData(async e => {
            if (!pyodide) return;

            if (e === '\r') { // Enter
                term.write('\r\n');
                await runPythonLine(pythonInputBuffer);
                pythonInputBuffer = "";
            } else if (e === '\u007F') { // Backspace
                if (pythonInputBuffer.length > 0) {
                    pythonInputBuffer = pythonInputBuffer.slice(0, -1);
                    term.write('\b \b');
                }
            } else {
                pythonInputBuffer += e;
                term.write(e);
            }
        });
    }

    // Executa uma linha digitada no terminal
    async function runPythonLine(line) {
        try {
            let result = await pyodide.runPythonAsync(line);
            if (result !== undefined) term.writeln(String(result));
        } catch (err) {
            term.writeln(`\x1B[1;31m${err}\x1B[0m`);
        }
        term.write('>>> ');
    }

    // 3. FUNÇÃO PRINCIPAL: RODAR O CÓDIGO DO EDITOR
    async function runPython() {
        // Abre o terminal se estiver fechado
        if (!document.body.classList.contains('show-terminal')) {
            toggleTerminal();
        }

        if (!pyodide) {
            // Se o terminal não iniciou ainda, aguarda
            if(!term) await initTerminal();
            // Pequeno delay para garantir que pyodide carregou se initTerminal foi chamado agora
            if(!pyodide) { term.writeln("Aguarde o carregamento do Python..."); return; }
        }

        const code = editor.getValue();
        term.writeln('\x1B[1;33m--- Executando Script ---\x1B[0m');
        
        try {
            await pyodide.runPythonAsync(code);
        } catch (err) {
            term.writeln(`\x1B[1;31mErro de Execução:\n${err}\x1B[0m`);
        }
        
        term.writeln('\x1B[1;33m--- Fim ---\x1B[0m');
        term.write('>>> ');
    }

    function toggleTerminal() {
        document.body.classList.toggle('show-terminal');
        if (document.body.classList.contains('show-terminal')) {
            setTimeout(() => {
                initTerminal();
                if(fitAddon) fitAddon.fit();
                if(term) term.focus();
            }, 100);
        }
    }

    // 4. API GITHUB (Back to Normal)
    async function fetchFileList() {
        const list = document.getElementById('fileList');
        try {
            const r = await fetch(`${BACKEND_URL}?t=${Date.now()}`);
            const files = await r.json();
            list.innerHTML = '';
            files.forEach(f => {
                if(f.type === 'file') {
                    const btn = document.createElement('button');
                    btn.className = 'list-group-item list-group-item-action bg-transparent text-white border-bottom border-secondary small';
                    btn.innerHTML = `<i class="bi bi-file-earmark-code me-2"></i>${f.name}`;
                    btn.onclick = () => loadFile(f.name);
                    list.appendChild(btn);
                }
            });
        } catch (e) { console.error(e); }
    }

    async function loadFile(name) {
        try {
            const r = await fetch(`${BACKEND_URL}/${name}`);
            const data = await r.json();
            const content = decodeURIComponent(escape(atob(data.content)));
            document.getElementById('fileName').value = data.name;
            editor.setValue(content);
        } catch (e) { alert("Erro ao abrir"); }
    }

    async function saveToGitHub() {
        const name = document.getElementById('fileName').value;
        if (!name) return alert("Nome obrigatório");
        setStatus("Salvando...", "warning");
        try {
            let sha = "";
            try {
                const check = await fetch(`${BACKEND_URL}/${name}`);
                if(check.ok) { const d = await check.json(); sha = d.sha; }
            } catch(e){}

            await fetch(`${BACKEND_URL}/${name}`, {
                method: "PUT",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({
                    message: "Update via Studio",
                    content: btoa(unescape(encodeURIComponent(editor.getValue()))),
                    sha: sha || null
                })
            });
            setStatus("Salvo!", "success");
            fetchFileList();
        } catch(e) { setStatus("Erro", "danger"); }
    }

    async function deleteFile() {
        const name = document.getElementById('fileName').value;
        if(!name || !confirm('Excluir?')) return;
        try {
            const check = await fetch(`${BACKEND_URL}/${name}`);
            const d = await check.json();
            await fetch(`${BACKEND_URL}/${name}`, {
                method: "DELETE",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({ message: "Delete", sha: d.sha })
            });
            document.getElementById('fileName').value = ""; editor.setValue(""); fetchFileList();
        } catch(e) { setStatus("Erro", "danger"); }
    }

    function setStatus(msg, type) {
        const el = document.getElementById('status');
        el.innerText = msg;
        el.className = `badge bg-${type} ms-auto`;
    }

    window.onload = fetchFileList;
    window.addEventListener('resize', () => { if(fitAddon) fitAddon.fit(); });
</script>

</body>
</html>