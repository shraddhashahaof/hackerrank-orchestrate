from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(self):

        self.root = Path(__file__).resolve().parents[1]
        self.dataset_dir = self.root / "dataset"

    def load_claims(self):

        return pd.read_csv(
            self.dataset_dir / "claims.csv"
        )

    def load_user_history(self):

        return pd.read_csv(
            self.dataset_dir / "user_history.csv"
        )

    def load_evidence_requirements(self):

        return pd.read_csv(
            self.dataset_dir / "evidence_requirements.csv"
        )

    def load_all(self):

        return {
            "claims": self.load_claims(),
            "history": self.load_user_history(),
            "requirements": self.load_evidence_requirements()
        }


if __name__ == "__main__":

    loader = DataLoader()

    claims = loader.load_claims()
    history = loader.load_user_history()
    requirements = loader.load_evidence_requirements()

    print(f"Claims: {len(claims)}")
    print(f"History: {len(history)}")
    print(f"Requirements: {len(requirements)}")

    print("\nClaims Columns:")
    print(claims.columns.tolist())