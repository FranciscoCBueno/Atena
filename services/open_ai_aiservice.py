import openai
from .ai_service import AIService

class OpenAIService(AIService):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"

    def classificar_email(self, conteudo_email: str) -> str:
        """
        Usa o modelo GPT para classificar o email.
        """
        try:
            system_prompt = """
            Você é um especialista em análise de e-mails. Sua tarefa é seguir um processo de duas etapas.

            Etapa 1: Análise do E-mail
            Analise o e-mail do usuário e determine se ele exige uma ação ou resposta. Considere os seguintes critérios:
            - O email requer uma ação ou resposta específica do destinatário (ex: uma pergunta, uma solicitação, um pedido de suporte).
            - O email é meramente informativo, social ou de encerramento, não necessitando de uma ação imediata (ex: agradecimentos, felicitações, confirmações de recebimento, avisos).
            Etapa 2: Classificação Final
            Com base na sua análise, classifique o e-mail estritamente como 'Produtivo' ou 'Improdutivo'.
            - 'Produtivo': Requer uma ação ou resposta específica (suporte, dúvidas, solicitações).
            - 'Improdutivo': Não requer ação imediata (agradecimentos, felicitações).

            Após a análise, responda apenas com a palavra 'Produtivo' ou 'Improdutivo', sem explicações adicionais.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conteudo_email}
                ],
                temperature=0.0,
                max_tokens=5
            )
            classificacao = response.choices[0].message.content.strip()
            return classificacao
        except Exception as e:
            print(f"Erro na API da OpenAI (classificação): {e}")
            return "Erro ao classificar"


    def gerar_resposta(self, conteudo_email: str, classificacao: str) -> str:
        """
        Usa o modelo GPT para gerar uma sugestão de resposta.
        """
        try:
            system_prompt = f"""
            Você é um assistente que escreve respostas de email curtas e profissionais.
            O email do usuário foi classificado como '{classificacao}'.
            Com base no email original, escreva uma sugestão de resposta curta, concisa e útil.
            Responda apenas com a sugestão de resposta, sem saudações ou despedidas adicionais.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user", 
                        "content": f"Email Original:\n---\n{conteudo_email}\n---\nSugestão de Resposta:"
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            sugestao = response.choices[0].message.content.strip()
            return sugestao
        except Exception as e:
            print(f"Erro na API da OpenAI (geração): {e}")
            return "Ocorreu um erro ao gerar a sugestão."