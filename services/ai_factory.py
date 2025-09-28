from .ai_service import AIService
from .gemini_pro_aiservice import GeminiProService
from .gemini_flash_aiservice import GeminiFlashService
from .hugging_face_aiservice import HuggingFaceService
from .open_ai_aiservice import OpenAIService

def get_ai_service(provider: str, api_key: str) -> AIService:
    if provider.lower() == 'geminipro':
        return GeminiProService(api_key=api_key)
    elif provider.lower() == 'geminiflash':
        return GeminiFlashService(api_key=api_key)
    elif provider == 'huggingface':
        return HuggingFaceService(api_key=api_key)
    elif provider == 'openai':
        return OpenAIService(api_key=api_key)
    else:
        raise ValueError(f"Provedor de IA desconhecido: {provider}")