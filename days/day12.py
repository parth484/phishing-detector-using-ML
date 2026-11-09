"""Day 12: Full pipeline latency profiling."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.phishing_ml.latency import profile_extractor, profile_inference
path="artifacts/holdout_50_v3.csv"
frame=pd.read_csv(path); urls=frame["URL"].astype(str).head(10).tolist()
print("Feature extraction:",profile_extractor(urls))
print("Inference latency:",profile_inference(urls,version="v3"))
