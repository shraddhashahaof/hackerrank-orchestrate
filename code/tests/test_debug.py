import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from agents.claim_extractor import ClaimExtractor
from agents.vision_inspector import VisionInspector
from agents.evidence_validator import EvidenceValidator
from agents.risk_assessor import RiskAssessor
from agents.decision_engine import DecisionEngine

loader = DataLoader()
claims = loader.load_claims()
history = loader.load_user_history()

# Test first 3 claims only
for _, sample in claims.head(3).iterrows():
    print("\n" + "="*50)
    print(f"USER: {sample['user_id']} | OBJECT: {sample['claim_object']}")
    print(f"CLAIM TEXT: {sample['user_claim']}")

    claim_data = ClaimExtractor().extract(
        sample["user_claim"],
        sample["claim_object"]
    )
    print(f"\nEXTRACTED: {claim_data}")

    raw_paths = sample["image_paths"].split(";")
    image_paths = [
        str(ROOT.parent / "dataset" / p) for p in raw_paths
    ]
    print(f"IMAGE PATHS: {image_paths}")

    vision_results = VisionInspector().inspect_multiple(
        image_paths, sample["claim_object"]
    )
    print(f"\nVISION RESULTS: {vision_results}")

    validation = EvidenceValidator().validate(claim_data, vision_results)
    print(f"\nVALIDATION: {validation}")

    user_row = history[history["user_id"] == sample["user_id"]].iloc[0]
    risk = RiskAssessor().assess(user_row)
    print(f"RISK: {risk}")

    decision = DecisionEngine().decide(claim_data, validation, risk)
    print(f"DECISION: {decision}")