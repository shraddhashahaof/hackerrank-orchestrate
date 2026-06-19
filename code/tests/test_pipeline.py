import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from data_loader import DataLoader
from services.pipeline_service import PipelineService

loader = DataLoader()
claims = loader.load_claims().head(3)
history = loader.load_user_history()

pipeline = PipelineService(loader, ROOT)

for _, claim in claims.iterrows():
    result = pipeline.process_claim(claim, history)
    print(result)