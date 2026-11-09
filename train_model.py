import argparse
from src.phishing_ml.model import train

def main():
    parser = argparse.ArgumentParser(description="Train the URL phishing ML model.")
    parser.add_argument("--csv", default="urllinks.csv")
    parser.add_argument("--per-class", type=int, default=5000)
    parser.add_argument("--include-https", action="store_true")
    parser.add_argument("--artifacts", default="artifacts")
    args = parser.parse_args()
    _, metrics, _ = train(
        args.csv, args.artifacts, args.per_class, args.include_https
    )
    print("\nTraining complete.")
    print(f"Version: {metrics['version']}")
    print(f"Accuracy: {metrics['accuracy']:.4%}")
    print(f"Features: {metrics['feature_count']}")

if __name__ == "__main__":
    main()
