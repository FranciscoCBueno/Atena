from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def classificar_email(self, conteudo_email: str) -> str:
        pass

    @abstractmethod
    def gerar_resposta(self, conteudo_email: str, classificacao: str) -> str:
        pass