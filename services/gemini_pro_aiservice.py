import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-2.5-pro", generation_config=generation_config)

def classificar_email(conteudo_email):
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
    response = model.generate_content(prompt)
    classificacao = response.text.strip().replace("'", "").replace('"', '')
    return classificacao

def gerar_resposta(conteudo_email, classificacao):
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
    response = model.generate_content(prompt)
    return response.text.strip()

# Teste rápido
if __name__ == '__main__':
    email_exemplo_produtivo = "Olá, time. Por favor, não se esqueçam de enviar o relatório de vendas até o final do dia. Precisamos consolidar os números para a reunião de amanhã. Obrigado."
    
    classificacao = classificar_email(email_exemplo_produtivo)
    print(f"Classificação: {classificacao}")

    resposta_sugerida = gerar_resposta(email_exemplo_produtivo, classificacao)
    print(f"Resposta Sugerida:\n{resposta_sugerida}")