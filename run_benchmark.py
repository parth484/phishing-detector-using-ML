import argparse
from src.phishing_ml.benchmark import run_benchmark

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="benchmark_urls.csv")
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--version", default="v3", choices=["v2", "v3"])
    args = parser.parse_args()
    print(run_benchmark(args.input, args.artifacts, args.version))

if __name__ == "__main__":
    main()
