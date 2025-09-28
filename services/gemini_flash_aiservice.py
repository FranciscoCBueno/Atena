import google.generativeai as genai
from .ai_service import AIService

class GeminiFlashService(AIService):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config
        )

    def classificar_email(self, conteudo_email: str) -> str:
        prompt = f"""
        Analise o conteúdo do seguinte email e classifique-o estritamente como 'Produtivo' ou 'Improdutivo'.
        - 'Produtivo' significa que é um email que requer uma ação ou resposta específica, como por exemplo: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, etc.
        - 'Improdutivo' significa que é um email que não necessita de uma ação imediata, como por exemplo: mensagens de felicitações, agradecimentos, etc.

        Responda apenas com a palavra 'Produtivo' ou 'Improdutivo'.

        Email:
        ---
        {conteudo_email}
        ---
        Classificação:
        """
        response = self.model.generate_content(prompt)
        classificacao = response.text.strip().replace("'", "").replace('"', '')
        return classificacao

    def gerar_resposta(self, conteudo_email: str, classificacao: str) -> str:
        prompt = f"""
        Com base no seguinte email, que foi classificado como '{classificacao}', escreva uma sugestão de resposta curta e profissional.
        A resposta deve ser um ponto de partida para o usuário.

        Responda apenas com a sugestão de resposta, sem introduções ou conclusões.

        Email Original:
        ---
        {conteudo_email}
        ---
        Sugestão de Resposta:
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()