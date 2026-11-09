"""Day 4: Save model and standalone inference."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
from src.phishing_ml.engine import predict_url
required=[Path("artifacts/rf_model_v2.joblib"),Path("artifacts/url_medians_v2.joblib"),Path("artifacts/url_features_v2.joblib")]
missing=[str(p) for p in required if not p.exists()]
if missing: raise SystemExit("Run Day 3 first; missing: "+", ".join(missing))
print(predict_url("https://www.google.com",version="v2"))
