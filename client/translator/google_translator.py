from google.cloud import translate_v2 as translate
from translator.base import Translator
import asyncio
from dotenv import load_dotenv

load_dotenv()

class GoogleTranslator(Translator):
    def __init__(self):
        self.client = translate.Client()

    async def translate_to_german(self, text: str) -> str:
        try:
            result = await asyncio.to_thread(self.client.translate, text, target_language="de")
            return result["translatedText"]
        except Exception as e:
            print(f"[GoogleTranslateAPITranslator] Error: {e}")
            return "[Translation failed]"
