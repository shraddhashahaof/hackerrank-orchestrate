from config import PROVIDER

if PROVIDER == "groq":
    from utils.groq_client import GroqClient

class LLMFactory:

    @staticmethod
    def get_client():
        if PROVIDER == "groq":
            return GroqClient()
        raise ValueError(f"Unknown provider: {PROVIDER}")