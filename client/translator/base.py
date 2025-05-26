from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    async def translate_to_german(self, text: str) -> str:
        pass
