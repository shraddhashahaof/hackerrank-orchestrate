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

loader = DataLoader()

claims = loader.load_claims()

sample = claims.iloc[0]

claim_extractor = ClaimExtractor()

claim_data = claim_extractor.extract(
    claim_text=sample["user_claim"],
    claim_object=sample["claim_object"]
)

raw_paths = sample[
    "image_paths"
].split(";")

image_paths = [
    str(ROOT.parent / "dataset" / p)
    for p in raw_paths
]

vision = VisionInspector()

vision_results = (
    vision.inspect_multiple(
        image_paths=image_paths,
        claim_object=sample[
            "claim_object"
        ]
    )
)

validator = EvidenceValidator()

result = validator.validate(
    claim_extraction=claim_data,
    vision_results=vision_results
)

print("\nCLAIM EXTRACTION")
print(claim_data)

print("\nVISION RESULTS")
print(vision_results)

print("\nVALIDATION RESULT")
print(result)