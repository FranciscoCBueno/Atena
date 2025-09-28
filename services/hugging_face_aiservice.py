import requests
import os
from .ai_service import AIService

class HuggingFaceService(AIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.classification_model = "facebook/bart-large-mnli"
        self.generation_model = "HuggingFaceH4/zephyr-7b-beta"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _query_api(self, model_id, payload):
        """Função auxiliar para fazer a chamada à API."""
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        payload.setdefault("options", {"wait_for_model": True})
        response = requests.post(api_url, headers=self.headers, json=payload)
        
        response.raise_for_status() 
        return response.json()

    def classificar_email(self, conteudo_email: str) -> str:
        """
        Usa um modelo de classificação "Zero-Shot" para categorizar o email.
        """
        payload = {
            "inputs": conteudo_email,
            "parameters": {
                "candidate_labels": ["Produtivo", "Improdutivo"]
            }
        }
        
        try:
            output = self._query_api(self.classification_model, payload)
            classificacao = output['labels'][0]
            return classificacao
        except Exception as e:
            print(f"Erro na API de classificação do Hugging Face: {e}")
            return "Não foi possível classificar"


    def gerar_resposta(self, conteudo_email: str, classificacao: str) -> str:
        prompt = f"""<|system|>
        Você é um assistente que escreve respostas curtas e profissionais para emails. O email foi classificado como '{classificacao}'. Escreva uma sugestão de resposta que seja um bom ponto de partida. Responda apenas com a sugestão, sem introduções.</s>
        <|user|>
        Email Original:
        ---
        {conteudo_email}
        ---
        Sugestão de Resposta:</s>
        <|assistant|>
        """
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        try:
            output = self._query_api(self.generation_model, payload)
            sugestao = output[0]['generated_text'].strip()
            return sugestao
        except Exception as e:
            print(f"Erro na API de geração do Hugging Face: {e}")
            return "Ocorreu um erro ao gerar a sugestão de resposta."