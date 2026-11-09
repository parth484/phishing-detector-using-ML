import argparse
from src.phishing_ml.engine import predict_url

def main():
    parser = argparse.ArgumentParser(description="Predict a URL using the trained V3 model.")
    parser.add_argument("url", nargs="?")
    parser.add_argument("--version", default="v3", choices=["v2", "v3"])
    parser.add_argument("--artifacts", default="artifacts")
    args = parser.parse_args()
    url = args.url or input("Enter URL: ").strip()
    try:
        print(predict_url(url, args.artifacts, args.version))
    except Exception as exc:
        parser.exit(1, f"Prediction failed: {exc}\n")

if __name__ == "__main__":
    main()
