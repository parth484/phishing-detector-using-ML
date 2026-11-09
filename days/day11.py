"""Day 11: execute a benchmark smoke test and prepare an independent benchmark template."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.phishing_ml.benchmark import create_template
from src.phishing_ml.evaluation import evaluate_urls

smoke_path = Path("artifacts/benchmark_smoke_20_v3.csv")
if smoke_path.exists():
    smoke = pd.read_csv(smoke_path)
    print("Dataset-derived 20-row benchmark smoke test (NOT independent/live):")
    print(evaluate_urls(smoke, version="v3"))
else:
    print("Run `python train_model.py` first to create the benchmark smoke test.")

template = Path("benchmark_urls.csv")
if not template.exists():
    create_template(template)
print("\nIndependent benchmark template:", template.resolve())
print("For the final external benchmark, fill 20 independently verified URLs:")
print("- 10 phishing URLs with label 0")
print("- 10 legitimate URLs with label 1")
print("Record source and verification notes; then run `python run_benchmark.py`.")
