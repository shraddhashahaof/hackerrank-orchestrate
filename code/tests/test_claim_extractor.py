import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from agents.claim_extractor import ClaimExtractor


loader = DataLoader()

claims = loader.load_claims()

sample = claims.iloc[0]

extractor = ClaimExtractor()

result = extractor.extract(
    claim_text=sample["user_claim"],
    claim_object=sample["claim_object"]
)

print("\nUSER CLAIM\n")
print(sample["user_claim"])

print("\nOBJECT\n")
print(sample["claim_object"])

print("\nEXTRACTION RESULT\n")
print(result)