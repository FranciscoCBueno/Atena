from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

from reader import extract_txt, extract_pdf
from services.gemini_pro_aiservice import classificar_email, gerar_resposta

app = Flask(__name__)

# Configuração para uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
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
            classificacao = classificar_email(texto_final)
            sugestao = gerar_resposta(texto_final, classificacao)
            
            return jsonify({
                'categoria': classificacao,
                'sugestao': sugestao
            })
        except Exception as e:
            return jsonify({'error': 'Falha ao processar a solicitação de IA'}), 500
    
    return jsonify({'error': 'Não foi possível extrair texto para análise'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)