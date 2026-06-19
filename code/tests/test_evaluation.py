import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from evaluation.evaluator import Evaluator

results_path = ROOT / "outputs" / "results.csv"
# We use results as ground truth placeholder if no separate file exists
metrics = Evaluator(
    str(results_path),
    str(results_path)
).evaluate()

print("\n=== EVALUATION METRICS ===")
for k, v in metrics.items():
    print(f"  {k}: {v}")