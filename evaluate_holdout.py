import argparse
import pandas as pd
from src.phishing_ml.evaluation import evaluate_urls, write_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="artifacts/holdout_50_v3.csv")
    parser.add_argument("--version", default="v3", choices=["v2", "v3"])
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--output", default="artifacts/holdout_evaluation.json")
    args = parser.parse_args()
    frame = pd.read_csv(args.input)
    metrics = evaluate_urls(frame, args.artifacts, args.version)
    write_report(metrics, args.output)
    print(metrics)

if __name__ == "__main__":
    main()
