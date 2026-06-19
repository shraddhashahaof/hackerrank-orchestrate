from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str
    ):

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    def generate_vision(
        self,
        prompt,
        image
    ):

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                image
            ]
        )

        return response.text.strip()