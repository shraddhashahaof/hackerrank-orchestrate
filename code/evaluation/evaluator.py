import pandas as pd
from pathlib import Path


class Evaluator:
    """
    Evaluates pipeline output against expected decisions.
    If no ground truth file exists, computes basic statistics.
    """

    def __init__(self, results_path: str, ground_truth_path: str = None):
        self.results = pd.read_csv(results_path)
        self.ground_truth_path = ground_truth_path

        if ground_truth_path and Path(ground_truth_path).exists():
            gt = pd.read_csv(ground_truth_path)
            if "expected_decision" in gt.columns:
                self.ground_truth = gt
            else:
                self.ground_truth = None
        else:
            self.ground_truth = None

    def evaluate(self) -> dict:
        total = len(self.results)
        decision_counts = self.results["decision"].value_counts().to_dict()
        avg_confidence = round(self.results["confidence"].mean(), 3)

        approve_count = decision_counts.get("approve", 0)
        reject_count = decision_counts.get("reject", 0)
        review_count = decision_counts.get("manual_review", 0)

        approve_pct = round(approve_count / total * 100, 1) if total > 0 else 0
        reject_pct = round(reject_count / total * 100, 1) if total > 0 else 0
        review_pct = round(review_count / total * 100, 1) if total > 0 else 0

        metrics = {
            "total_claims": total,
            "avg_confidence": avg_confidence,
            "approve_count": approve_count,
            "reject_count": reject_count,
            "manual_review_count": review_count,
            "approve_pct": approve_pct,
            "reject_pct": reject_pct,
            "manual_review_pct": review_pct,
            "decision_distribution": decision_counts,
        }

        # If ground truth available, compute accuracy
        if self.ground_truth is not None:
            merged = self.results.merge(
                self.ground_truth[["user_id", "expected_decision"]],
                on="user_id",
                how="inner"
            )
            if not merged.empty:
                correct = (merged["decision"] == merged["expected_decision"]).sum()
                accuracy = round(correct / len(merged), 3)
                metrics["accuracy"] = accuracy
                metrics["correct_predictions"] = int(correct)
                metrics["evaluated_claims"] = len(merged)

        return metrics

    def print_report(self):
        metrics = self.evaluate()

        print("\n" + "=" * 50)
        print("   ORCHESTRATE PIPELINE — EVALUATION REPORT")
        print("=" * 50)
        print(f"  Total Claims Processed : {metrics['total_claims']}")
        print(f"  Avg Confidence Score   : {metrics['avg_confidence']}")
        print()
        print("  Decision Distribution:")
        print(f"    ✅ Approved      : {metrics['approve_count']}  ({metrics['approve_pct']}%)")
        print(f"    🔍 Manual Review : {metrics['manual_review_count']}  ({metrics['manual_review_pct']}%)")
        print(f"    ❌ Rejected      : {metrics['reject_count']}  ({metrics['reject_pct']}%)")

        if "accuracy" in metrics:
            print()
            print(f"  Accuracy (vs ground truth): {metrics['accuracy']}")
            print(f"  Correct Predictions       : {metrics['correct_predictions']}/{metrics['evaluated_claims']}")

        print("=" * 50)
        return metrics