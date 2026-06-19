from pathlib import Path
import pandas as pd

from data_loader import DataLoader
from services.pipeline_service import PipelineService
from evaluation.evaluator import Evaluator
from utils.logger import logger

ROOT = Path(__file__).resolve().parent

logger.info("=" * 50)
logger.info("  ORCHESTRATE — Insurance Claim AI Pipeline")
logger.info("=" * 50)

loader = DataLoader()
claims = loader.load_claims()
history = loader.load_user_history()

logger.info(f"Loaded {len(claims)} claims | {len(history)} user history records")

pipeline = PipelineService(loader, ROOT)
results = []

for idx, claim in claims.iterrows():
    logger.info(
        f"[{idx+1}/{len(claims)}] Processing user={claim['user_id']} "
        f"object={claim['claim_object']}"
    )
    try:
        result = pipeline.process_claim(claim, history)
        results.append(result)
        logger.info(
            f"  → decision={result['claim_status']} | "
            f"reason={result['claim_status_justification']}"
        )
    except Exception as e:
        logger.error(f"  ✗ Failed claim {idx}: {e}")

# Save results
output_df = pd.DataFrame(results)
output_dir = ROOT / "outputs"
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "results.csv"
output_df.to_csv(output_file, index=False)
logger.info(f"Results saved → {output_file}")

# Also write output.csv to repo root (required by AGENTS.md)
root_output = ROOT.parent / "output.csv"
output_df.to_csv(root_output, index=False)
logger.info(f"Also saved → {root_output}")

# Evaluation report
evaluator = Evaluator(str(output_file))
evaluator.print_report()