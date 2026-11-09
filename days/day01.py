"""Day 1: dataset exploration and cleaning audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
import pandas as pd
from src.phishing_ml.data import load_dataset

parser = argparse.ArgumentParser()
parser.add_argument("--csv", default="urllinks.csv")
args = parser.parse_args()

raw = pd.read_csv(args.csv, low_memory=False)
clean = load_dataset(args.csv)
print("Raw dataset shape:", raw.shape)
print("Clean dataset shape:", clean.shape)
print("\nLabel counts:\n", clean["label"].value_counts().sort_index())
print("\nMissing values (top 15):\n", raw.isna().sum().sort_values(ascending=False).head(15))
print("\nDuplicate URLs in raw data:", raw["URL"].duplicated().sum())
print("Unique URLs after cleaning:", clean["URL"].nunique())
print("\nColumns:", list(raw.columns))
