
"""Day 3: Baseline Random Forest training."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from src.phishing_ml.model import train

p = argparse.ArgumentParser()
p.add_argument("--csv", default="urllinks.csv")
p.add_argument("--per-class", type=int, default=5000)
a = p.parse_args()

model, metrics, _ = train(
    a.csv,
    "artifacts",
    a.per_class,
    include_https=True
)

print("\n========== V2 BASELINE MODEL RESULTS ==========")

print(f"\nAccuracy: {metrics['accuracy']:.4%}")

print("\nAll available evaluation metrics:")
for name, value in metrics.items():
    print(f"{name}: {value}")

print("\n================================================")
