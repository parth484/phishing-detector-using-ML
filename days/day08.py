"""Day 8: 50 URL holdout evaluation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import pandas as pd
from src.phishing_ml.evaluation import evaluate_urls
path=Path("artifacts/holdout_50_v3.csv")
if not path.exists(): raise SystemExit("Run the final V3 training first: python train_model.py")
frame=pd.read_csv(path)
print("Holdout URLs:",len(frame))
print(evaluate_urls(frame,version="v3"))
