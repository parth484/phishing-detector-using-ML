"""Run evaluation against a user-curated, independently labelled URL benchmark."""
from pathlib import Path
import pandas as pd
from .evaluation import evaluate_urls


def create_template(path="benchmark_urls.csv"):
    frame = pd.DataFrame({
        "URL": [""] * 20,
        "label": [""] * 20,
        "source": [""] * 20,
        "notes": [""] * 20,
    })
    frame.to_csv(path, index=False)
    return Path(path)


def run_benchmark(csv_path="benchmark_urls.csv", artifact_dir="artifacts", version="v3"):
    path = Path(csv_path)
    if not path.exists():
        create_template(path)
        raise FileNotFoundError(
            f"Created {path}. Fill 20 independently verified URLs and labels "
            "(10 legitimate label 1, 10 phishing label 0), then rerun."
        )
    frame = pd.read_csv(path)
    frame = frame.dropna(subset=["URL", "label"]).copy()
    frame["URL"] = frame["URL"].astype(str).str.strip()
    frame = frame[frame["URL"].ne("") & frame["label"].astype(str).str.strip().ne("")]
    if len(frame) != 20:
        raise ValueError(f"Benchmark must contain exactly 20 labelled rows; found {len(frame)}.")
    frame["label"] = pd.to_numeric(frame["label"], errors="raise").astype(int)
    counts = frame["label"].value_counts().to_dict()
    if counts.get(0, 0) != 10 or counts.get(1, 0) != 10:
        raise ValueError(f"Expected 10 examples per class (0 and 1); found {counts}.")
    return evaluate_urls(frame, artifact_dir=artifact_dir, version=version)
