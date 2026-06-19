from pathlib import Path
import pandas as pd

from data_loader import DataLoader
from services.pipeline_service import PipelineService

ROOT = Path(__file__).resolve().parent

loader = DataLoader()
claims = loader.load_claims()
history = loader.load_user_history()

pipeline = PipelineService(loader, ROOT)

results = []

for idx, claim in claims.iterrows():
    print(f"Processing {idx+1}/{len(claims)} — user: {claim['user_id']}")
    try:
        result = pipeline.process_claim(claim, history)
        results.append(result)
        print(f"  → {result['decision']} ({result['confidence']})")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

output_df = pd.DataFrame(results)
output_dir = ROOT / "outputs"
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "results.csv"
output_df.to_csv(output_file, index=False)
print(f"\n✅ Saved {len(results)} results to {output_file}")