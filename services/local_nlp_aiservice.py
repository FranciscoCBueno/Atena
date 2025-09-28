import joblib
import os
import spacy
from nltk.corpus import stopwords
import string
from .ai_service import AIService

try:
    nlp = spacy.load("pt_core_news_sm")
    stop_words = stopwords.words('portuguese')
    punctuations = string.punctuation
except IOError:
    print("Erro: Modelo 'pt_core_news_sm' do spaCy não encontrado.")
    print("Execute: python -m spacy download pt_core_news_sm")
    nlp = None

def preprocess_text(text):
    if not nlp:
        return text
        
    doc = nlp(text.lower())
    processed_tokens = [
        token.lemma_ 
        for token in doc 
        if token.is_alpha and token.lemma_ not in stop_words and token.lemma_ not in punctuations
    ]
    return " ".join(processed_tokens)

class LocalNLPService(AIService):
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__),'..', 'model_training', 'email_classifier_pipeline.pkl')
        try:
            self.model = joblib.load(model_path)
            print("Modelo de NLP local (pipeline.pkl) carregado com sucesso.")
        except FileNotFoundError:
            print(f"ERRO: Arquivo do modelo '{model_path}' não encontrado.")
            print("Execute o script 'train_model.py' primeiro para gerar o modelo.")
            self.model = None

    def classificar_email(self, conteudo_email: str) -> str:
        if not self.model:
            return "Erro: modelo local não foi carregado."
        
        texto_processado = preprocess_text(conteudo_email)
        
        prediction = self.model.predict([texto_processado])
        return prediction[0]

    def gerar_resposta(self, conteudo_email: str, classificacao: str) -> str:
        return "Este modelo não suporta geração de respostas."