from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from reader import extract_txt, extract_pdf
from services.ai_factory import get_ai_service

load_dotenv()
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

API_KEYS = {
    'geminipro': os.getenv('GEMINI_PRO_KEY'),
    'geminiflash': os.getenv('GEMINI_FLASH_KEY'),
    'huggingface': os.getenv('HUGGING_FACE_KEY'),
    'openai': os.getenv('OPEN_AI_KEY')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_model = request.form.get('model', 'geminipro').lower()
    if selected_model == 'localnlp':
        api_key = "local"
    else:
        api_key = API_KEYS.get(selected_model)

    if not api_key:
        error_msg = f"A chave de API para o modelo '{selected_model}' não foi encontrada no arquivo .env."
        print(error_msg)
        return jsonify({'error': error_msg}), 503
    
    try:
        ai_service = get_ai_service(provider=selected_model, api_key=api_key)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    print(f"Usando modelo: {selected_model}")
    texto_final = ""
    
    texto_colado = request.form.get('texto')
    
    arquivo = request.files.get('arquivo')

    if arquivo and arquivo.filename != '':
        filename = secure_filename(arquivo.filename)
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo.save(caminho_arquivo)

        if filename.endswith('.pdf'):
            texto_final = extract_pdf(caminho_arquivo)
        elif filename.endswith('.txt'):
            texto_final = extract_txt(caminho_arquivo)
        
        os.remove(caminho_arquivo)

    elif texto_colado:
        texto_final = texto_colado
    
    else:
        return jsonify({'error': 'Nenhum texto ou arquivo fornecido'}), 400

    if texto_final:
        try:
            classificacao = ai_service.classificar_email(texto_final)
            sugestao = ai_service.gerar_resposta(texto_final, classificacao)
            
            return jsonify({
                'categoria': classificacao,
                'sugestao': sugestao
            })
        except Exception as e:
            print(f"Erro no processamento da IA: {e}")
            return jsonify({'error': 'Falha ao processar a solicitação de IA'}), 500
    
    return jsonify({'error': 'Não foi possível extrair texto para análise'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)