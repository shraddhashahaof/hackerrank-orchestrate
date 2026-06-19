import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from agents.risk_assessor import RiskAssessor

loader = DataLoader()

history = loader.load_user_history()

assessor = RiskAssessor()

print("\nHIGH RISK USERS\n")

for _, row in history.iterrows():

    result = assessor.assess(row)

    if result["risk_level"] != "low":

        print("-" * 60)

        print("USER:", row["user_id"])

        print(result)