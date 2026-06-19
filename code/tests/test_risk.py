import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from agents.risk_assessor import RiskAssessor

loader = DataLoader()

history = loader.load_user_history()

assessor = RiskAssessor()

for idx, row in history.iterrows():

    result = assessor.assess(row)

    print("\n" + "=" * 70)

    print("USER:", row["user_id"])

    print("Past Claims:",
          row["past_claim_count"])

    print("Rejected Claims:",
          row["rejected_claim"])

    print("Manual Reviews:",
          row["manual_review_claim"])

    print("Last 90 Days Claims:",
          row["last_90_days_claim_count"])

    print("History Flags:",
          row["history_flags"])

    print("Summary:")
    print(row["history_summary"])

    print("\nRisk Result:")
    print(result)