# Atena - Analisador Inteligente de E-mails
Atena é uma aplicação web construída com Flask que utiliza diversos modelos de Inteligência Artificial para analisar o conteúdo de e-mails e os classifica como "Produtivos" ou "Improdutivos", e gera uma sugestão de resposta com base no diagnóstico.

Disponível em produção: https://atena-iajs.onrender.com/

## Funcionalidades
- Classificação de E-mails: Determina se um e-mail requer uma ação imediata (Produtivo) ou não (Improdutivo).
- Sugestão de Respostas: Gera sugestões de respostas contextuais e profissionais com base no conteúdo e na classificação do e-mail.
- Suporte a Múltiplos Modelos de IA: Permite escolher entre diferentes provedores de IA, incluindo:

    - Google Gemini (Pro e Flash)

    - OpenAI (GPT)

    - Modelos do Hugging Face

    - Um modelo de NLP tradicional treinado localmente (usando Scikit-learn e spaCy)
- Flexibilidade de Entrada: Aceita tanto texto colado diretamente quanto o upload de arquivos .txt e .pdf.

## Tecnologias Usadas
- Backend: Python, Flask

- Servidor de Produção: Gunicorn

- APIs dos Modelos de Linguagem: Gemini API, OpenAI API, Hugging Face API

- NLP Local: Scikit-learn, spaCy, NLTK, Pandas

- Frontend: HTML, CSS, JavaScript

- Containerização: Docker

## Utilização
Com a aplicação aberta no navegador:
1. Escolha entre colar um texto copiado de um e-mail, ou fazer upload de um arquivo .pdf ou .txt.
2. Escolha o modelo de IA para ser usado no menu dropdown.
3. Clique em "Analisar Email" e aguarde.

## Rodando Localmente
### Pré-requisitos
- Git
- Python 3.9+ e Pip
- Docker (Opcional)

### 1. Clone o repositório e entre no diretório clonado
```
git clone https://github.com/FranciscoCBueno/Atena.git
cd Atena
```
### 2. Criar e ativar o ambiente virtual
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```
Windows
```
python -m venv venv
.\venv\Scripts\activate
```
### 3. Instalar dependências
```
pip install -r requirements.txt
```
### 4. Baixar modelos de linguagem para NLP
(Necessário para o funcionamento do modelo local)
```
python -m spacy download pt_core_news_sm
python -c "import nltk; nltk.download('stopwords')"
```
### 5. Configurar variáveis de ambiente
Crie um arquivo .env na raíz do projeto (Atena/.env) e adicione suas chaves conforme o formato:
```
GEMINI_PRO_KEY="SUA_CHAVE_API_AQUI"
GEMINI_FLASH_KEY="SUA_CHAVE_API_AQUI"
OPEN_AI_KEY="SUA_CHAVE_API_AQUI"
HUGGING_FACE_KEY="SUA_CHAVE_API_AQUI"
```
### 6. Treine o modelo NLP local
Para garantir o funcionamento do modelo local na aplicação:
```
python model_training/train_model.py
```

### 7. Execute a Aplicação
#### 7.1 Servidor local
Apenas execute o comando:
```
python app.py
```
A aplicação estará rodando em: http://127.0.0.1:5001
#### 7.2 Docker
Para rodar pelo Docker, simulando o ambiente de produção, certifique-se de que o Docker está rodando no seu sistema e execute:
```
docker build -t atena .
```
```
docker run -p 8080:8000 --env-file .env atena
```
A aplicação estará rodando em: http://localhost:8080