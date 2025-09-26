document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('email-form');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const categoriaSpan = document.getElementById('resultado-categoria');
    const sugestaoP = document.getElementById('resultado-sugestao');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Mostra o loading e esconde resultados antigos
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');

        // Objeto FormData para enviar tanto texto quanto arquivo
        const formData = new FormData(form);

        try {
            // Chamada para a análise
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Erro na resposta do servidor.');
            }

            const data = await response.json();

            // Atualiza a página com os resultados
            categoriaSpan.textContent = data.categoria || 'N/A';
            sugestaoP.textContent = data.sugestao || 'N/A';
            
            // Mostra os resultados
            resultsDiv.classList.remove('hidden');

        } catch (error) {
            console.error('Erro:', error);
            sugestaoP.textContent = 'Ocorreu um erro ao processar a solicitação. Tente novamente.';
            resultsDiv.classList.remove('hidden');
        } finally {
            // Esconde o loading em qualquer caso (sucesso ou erro)
            loadingDiv.classList.add('hidden');
        }
    });
});