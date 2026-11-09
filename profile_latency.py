import argparse
import pandas as pd
from src.phishing_ml.latency import profile_extractor, profile_inference

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="artifacts/holdout_50_v3.csv")
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--version", default="v3", choices=["v2", "v3"])
    args = parser.parse_args()
    frame = pd.read_csv(args.input)
    urls = frame["URL"].astype(str).tolist()
    print("Feature extractor latency (ms):", profile_extractor(urls))
    print("Cached inference latency (ms):", profile_inference(urls, args.artifacts, args.version))

if __name__ == "__main__":
    main()
