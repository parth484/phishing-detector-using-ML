import argparse
from pathlib import Path
import joblib
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v3", choices=["v2", "v3"])
    parser.add_argument("--artifacts", default="artifacts")
    args = parser.parse_args()
    base = Path(args.artifacts)
    model = joblib.load(base / f"rf_model_{args.version}.joblib")
    features = joblib.load(base / f"url_features_{args.version}.joblib")
    frame = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    print(frame.to_string(index=False))

if __name__ == "__main__":
    main()
