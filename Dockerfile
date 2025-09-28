# Usar uma imagem oficial do Python como imagem base
FROM python:3.11-slim

# Definir o diretório de trabalho no conteiner
WORKDIR /app

# Copiar o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta em que a aplicação roda
EXPOSE 5001

# Rodar a aplicação
CMD ["python", "app.py"]