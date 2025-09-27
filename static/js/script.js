document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('email-form');
    const analyzeBtn = document.getElementById('analisar-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results-container');
    const categoriaSpan = document.getElementById('resultado-categoria');
    const sugestaoP = document.getElementById('resultado-sugestao');
    const fileInput = document.getElementById('arquivo-email');
    const fileNameDisplay = document.getElementById('file-name');
    const textarea = document.getElementById('texto-email');
    const avisoArquivos = document.getElementById('aviso-arquivos');
    const avisoVazio = document.getElementById('aviso-vazio');
    const btnTexto = document.getElementById('btn-texto');
    const btnArquivo = document.getElementById('btn-arquivo');
    const containerTexto = document.getElementById('container-texto');
    const containerArquivo = document.getElementById('container-arquivo');
    const logo = document.getElementById('logo');

    fileInput.value = '';
    fileNameDisplay.textContent = '';
    textarea.value = '';

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (textarea.value.trim() === '' && fileInput.files.length === 0) {
            avisoArquivos.classList.add('hidden');
            avisoVazio.classList.remove('hidden');
            return;
        }

        if (textarea.value.trim() && fileInput.files.length > 0) {
            avisoVazio.classList.add('hidden');
            avisoArquivos.classList.remove('hidden');
            return;
        }

        loadingDiv.classList.remove('hidden');
        analyzeBtn.classList.add('hidden');
        avisoVazio.classList.add('hidden');
        avisoArquivos.classList.add('hidden');
        resultsDiv.classList.add('hidden');

        // Objeto FormData para enviar tanto texto quanto arquivo
        const formData = new FormData(form);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Erro na resposta do servidor.');
            }

            const data = await response.json();

            categoriaSpan.textContent = data?.categoria?.toLowerCase() || 'N/A';
            sugestaoP.textContent = data.sugestao || 'N/A';
            
            resultsDiv.classList.remove('hidden');

            fileInput.value = '';
            fileNameDisplay.textContent = '';
        } catch (error) {
            console.error('Erro:', error);
            sugestaoP.textContent = 'Ocorreu um erro ao processar a solicitação. Tente novamente.';
            resultsDiv.classList.remove('hidden');
        } finally {
            loadingDiv.classList.add('hidden');
            analyzeBtn.classList.remove('hidden');
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            let fileName = fileInput.files[0].name;
            const maxLength = 40;

            if (fileName.length > maxLength) {
                const start = fileName.substring(0, 35);
                const end = fileName.substring(fileName.length - 5);
                fileName = `${start}...${end}`;
            }
            
            fileNameDisplay.textContent = fileName;
        } else {
            fileNameDisplay.textContent = '';
        }
    });

    btnTexto.addEventListener('click', () => {
        btnTexto.classList.add('selected-btn');
        btnArquivo.classList.remove('selected-btn');
        containerTexto.classList.remove('hidden');
        containerArquivo.classList.add('hidden');
        avisoArquivos.classList.add('hidden');
        avisoVazio.classList.add('hidden');
        textarea.value = '';
        fileInput.value = '';
        fileNameDisplay.textContent = '';
    });

    btnArquivo.addEventListener('click', () => {
        btnArquivo.classList.add('selected-btn');
        btnTexto.classList.remove('selected-btn');
        containerTexto.classList.add('hidden');
        containerArquivo.classList.remove('hidden');
        avisoArquivos.classList.add('hidden');
        avisoVazio.classList.add('hidden');
        textarea.value = '';
        fileInput.value = '';
        fileNameDisplay.textContent = '';
    });

    logo.addEventListener('click', () => {
        window.location.href = '/';
    });
});