import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader

loader = DataLoader()

data = loader.load_all()

print(data["claims"].head())
print(data["history"].head())
print(data["requirements"].head())