import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from evaluation.evaluator import Evaluator

results_path = ROOT / "outputs" / "results.csv"

if not results_path.exists():
    print("ERROR: outputs/results.csv not found.")
    print("Run: python main.py first")
    sys.exit(1)

evaluator = Evaluator(str(results_path))
evaluator.print_report()