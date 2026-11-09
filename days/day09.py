"""Day 9: Prediction engine integration."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.phishing_ml.engine import predict_url
for url in ["https://example.com","https://www.google.com","http://192.168.1.1/login"]:
 print(predict_url(url,version="v3"))
