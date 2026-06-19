import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.llm_factory import LLMFactory

client = LLMFactory.get_client()
response = client.generate('Return exactly {"status":"working"}')
print(response)