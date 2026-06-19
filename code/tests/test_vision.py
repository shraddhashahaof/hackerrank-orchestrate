import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from agents.vision_inspector import VisionInspector

loader = DataLoader()

claims = loader.load_claims()

sample = claims.iloc[0]

raw_paths = sample["image_paths"].split(";")

image_paths = [
    str(ROOT.parent / "dataset" / path)
    for path in raw_paths
]

print("\nCLAIM")
print(sample["user_claim"])

print("\nOBJECT")
print(sample["claim_object"])

print("\nIMAGES")
for img in image_paths:
    print(img)

vision = VisionInspector()

results = vision.inspect_multiple(
    image_paths=image_paths,
    claim_object=sample["claim_object"]
)

print("\nVISION RESULTS")

for idx, result in enumerate(results, start=1):

    print(f"\nImage {idx}")

    print(result)