import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader

from agents.claim_extractor import (
    ClaimExtractor
)

from agents.vision_inspector import (
    VisionInspector
)

from agents.evidence_validator import (
    EvidenceValidator
)

from agents.risk_assessor import (
    RiskAssessor
)

from agents.decision_engine import (
    DecisionEngine
)

loader = DataLoader()

claims = loader.load_claims()
history = loader.load_user_history()

sample = claims.iloc[0]

claim_data = ClaimExtractor().extract(
    sample["user_claim"],
    sample["claim_object"]
)

raw_paths = sample["image_paths"].split(";")

image_paths = [
    str(ROOT.parent / "dataset" / p)
    for p in raw_paths
]

vision_results = (
    VisionInspector()
    .inspect_multiple(
        image_paths,
        sample["claim_object"]
    )
)

validation = (
    EvidenceValidator()
    .validate(
        claim_data,
        vision_results
    )
)

user_row = history[
    history["user_id"]
    == sample["user_id"]
].iloc[0]

risk = (
    RiskAssessor()
    .assess(user_row)
)

decision = (
    DecisionEngine()
    .decide(
        claim_data,
        validation,
        risk
    )
)

print("\nCLAIM")
print(claim_data)

print("\nVALIDATION")
print(validation)

print("\nRISK")
print(risk)

print("\nDECISION")
print(decision)