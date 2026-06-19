import pandas as pd
from pathlib import Path


class Evaluator:

    def __init__(self, results_path: str, ground_truth_path: str):
        self.results = pd.read_csv(results_path)
        self.ground_truth = pd.read_csv(ground_truth_path)

    def evaluate(self) -> dict:
        merged = self.results.merge(
            self.ground_truth,
            on="user_id",
            suffixes=("_pred", "_actual")
        )

        if "expected_decision" not in merged.columns:
            # No ground truth column — generate basic stats only
            return self._basic_stats()

        correct = (
            merged["decision"] == merged["expected_decision"]
        ).sum()

        total = len(merged)
        accuracy = round(correct / total, 3) if total > 0 else 0

        decision_counts = self.results["decision"].value_counts().to_dict()

        avg_confidence = round(
            self.results["confidence"].mean(), 3
        )

        return {
            "total_claims": total,
            "accuracy": accuracy,
            "correct": int(correct),
            "avg_confidence": avg_confidence,
            "decision_distribution": decision_counts
        }

    def _basic_stats(self) -> dict:
        total = len(self.results)
        decision_counts = self.results["decision"].value_counts().to_dict()
        avg_confidence = round(self.results["confidence"].mean(), 3)

        return {
            "total_claims": total,
            "avg_confidence": avg_confidence,
            "decision_distribution": decision_counts
        }