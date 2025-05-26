import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from .base import Translator

load_dotenv()

class GeminiTranslator(Translator):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash"

    async def translate_to_german(self, text: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are an English to German translator. "
                        "You will be translating jokes. You must behave like Google Translate: "
                        "just return the translation, nothing else."
                    ),
                ),
                contents=text,
            )
            return response.text.strip()
        except Exception as e:
            print(f"[GeminiTranslator] Error: {e}")
            return "[Translation failed]"
