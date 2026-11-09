"""Evaluation helpers for holdout and benchmark datasets."""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_recall_fscore_support
)
from .engine import predict_url


def evaluate_urls(frame: pd.DataFrame, artifact_dir="artifacts", version="v3"):
    required = {"URL", "label"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Input must contain columns: {sorted(required)}")
    actual, predicted = [], []
    for row in frame.itertuples(index=False):
        result = predict_url(str(row.URL), artifact_dir=artifact_dir, version=version)
        actual.append(int(row.label))
        predicted.append(int(result["prediction"]))
    report = classification_report(actual, predicted, output_dict=True, zero_division=0)
    cm = confusion_matrix(actual, predicted, labels=[0, 1])
    precision, recall, f1, _ = precision_recall_fscore_support(
        actual, predicted, average="binary", pos_label=0, zero_division=0
    )
    return {
        "count": len(actual),
        "accuracy": float(accuracy_score(actual, predicted)),
        "precision_label_0": float(precision),
        "recall_label_0": float(recall),
        "f1_label_0": float(f1),
        "confusion_matrix_labels_0_1": cm.tolist(),
        "classification_report": report,
    }


def write_report(metrics: dict, output_path: str | Path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
