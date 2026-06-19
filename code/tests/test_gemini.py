import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.gemini_client import GeminiClient

client = GeminiClient()

print(
    client.generate(
        "Reply ONLY with Gemini Working"
    )
)