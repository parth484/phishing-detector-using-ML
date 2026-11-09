"""Day 10: Cached model loading."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.phishing_ml.engine import predict_url, _load_bundle
for url in ["https://example.com","https://www.google.com","https://example.com/login"]:
 print(predict_url(url,version="v3")["prediction"])
print("Artifact bundle cache:",_load_bundle.cache_info())
