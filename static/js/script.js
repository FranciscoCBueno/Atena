document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('email-form');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results-container');
    const categoriaSpan = document.getElementById('resultado-categoria');
    const sugestaoP = document.getElementById('resultado-sugestao');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        loadingDiv.classList.remove('hidden');
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

        } catch (error) {
            console.error('Erro:', error);
            sugestaoP.textContent = 'Ocorreu um erro ao processar a solicitação. Tente novamente.';
            resultsDiv.classList.remove('hidden');
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('arquivo-email');
    const fileNameDisplay = document.getElementById('file-name');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            let fileName = fileInput.files[0].name;
            const maxLength = 15;

            if (fileName.length > maxLength) {
                const start = fileName.substring(0, 7);
                const end = fileName.substring(fileName.length - 5);
                fileName = `${start}...${end}`;
            }
            
            fileNameDisplay.textContent = fileName;
        } else {
            fileNameDisplay.textContent = 'Nenhum arquivo selecionado';
        }
    });
});