import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from services.pipeline_service import PipelineService
from evaluation.evaluator import Evaluator
from utils.logger import logger

logger.info("=== Evaluation Entry Point ===")

loader = DataLoader()
claims = loader.load_claims()
history = loader.load_user_history()

pipeline = PipelineService(loader, ROOT)
results = []

for idx, claim in claims.iterrows():
    try:
        result = pipeline.process_claim(claim, history)
        results.append(result)
    except Exception as e:
        logger.error(f"Failed claim {idx}: {e}")

import pandas as pd

output_df = pd.DataFrame(results)

# Save as output.csv in repo root (as required by AGENTS.md)
output_file = ROOT.parent / "output.csv"
output_df.to_csv(output_file, index=False)
logger.info(f"Saved output.csv → {output_file}")

# Also save internal copy
internal = ROOT / "outputs"
internal.mkdir(exist_ok=True)
output_df.to_csv(internal / "results.csv", index=False)

# Print evaluation report
evaluator = Evaluator(str(output_file))
evaluator.print_report()