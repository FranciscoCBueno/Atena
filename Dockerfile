# Usar uma imagem oficial do Python como imagem base
FROM python:3.11-slim

# Definir o diretório de trabalho no conteiner
WORKDIR /app

# Copiar o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Baixa e instala os modelos de linguagem necessários
RUN python -m spacy download pt_core_news_sm
RUN python -c "import nltk; nltk.download('stopwords')"

# Copiar o resto do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta em que a aplicação roda
EXPOSE 8000

# Rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]