"""Training and artifact persistence."""
from __future__ import annotations
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_recall_fscore_support
)
from sklearn.model_selection import train_test_split

from .data import load_dataset, balanced_sample
from .features import extract_features


def build_feature_frame(urls: list[str]) -> pd.DataFrame:
    rows = []
    for i, url in enumerate(urls, start=1):
        try:
            rows.append(extract_features(url))
        except Exception as exc:
            raise ValueError(f"Feature extraction failed at row {i}, URL={url!r}: {exc}") from exc
    return pd.DataFrame(rows)


def train(csv_path: str | Path, artifact_dir: str | Path = "artifacts",
          per_class: int = 5000, include_https: bool = False, seed: int = 42):
    df = load_dataset(csv_path)
    sample = balanced_sample(df, per_class=per_class, seed=seed)
    X = build_feature_frame(sample["URL"].tolist())
    y = sample["label"].reset_index(drop=True)

    if not include_https:
        X = X.drop(columns=["IsHTTPS"])

    feature_names = X.columns.tolist()
    X_train, X_test, y_train, y_test, url_train, url_test = train_test_split(
        X, y, sample["URL"], test_size=0.2, random_state=seed, stratify=y
    )

    X_train = X_train.replace([np.inf, -np.inf], np.nan)
    X_test = X_test.replace([np.inf, -np.inf], np.nan)
    medians = X_train.median()
    X_train = X_train.fillna(medians)
    X_test = X_test.fillna(medians)

    model = RandomForestClassifier(
        n_estimators=100, random_state=seed, n_jobs=-1, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)

    labels = sorted(model.classes_.tolist())
    report = classification_report(
        y_test, pred, labels=labels, output_dict=True, zero_division=0
    )
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, pred, labels=labels, average="binary", pos_label=0, zero_division=0
    )
    cm = confusion_matrix(y_test, pred, labels=labels)

    version = "v2" if include_https else "v3"
    out = Path(artifact_dir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / f"rf_model_{version}.joblib")
    joblib.dump(medians, out / f"url_medians_{version}.joblib")
    joblib.dump(feature_names, out / f"url_features_{version}.joblib")

    holdout = pd.DataFrame({
        "URL": list(url_test),
        "label": y_test.to_numpy(),
        "predicted_label": pred,
        "class_0_score": proba[:, list(model.classes_).index(0)],
        "class_1_score": proba[:, list(model.classes_).index(1)],
    })
    # Save a deterministic 50-URL subset for Day 8.
    holdout_50 = (
        holdout.groupby("label", group_keys=False)
        .sample(n=25, random_state=seed)
        .reset_index(drop=True)
    )
    holdout_50.to_csv(out / f"holdout_50_{version}.csv", index=False)
    holdout.to_csv(out / f"holdout_all_{version}.csv", index=False)

    # A 20-row smoke-test sample from the supplied dataset. This validates
    # benchmark execution only; it is NOT an independent/live benchmark.
    smoke = (
        df.groupby("label", group_keys=False)
        .sample(n=10, random_state=seed + 100)
        [["URL", "label"]]
        .copy()
    )
    smoke["source"] = "PhiUSIIL dataset (dataset-derived smoke test; not independent)"
    smoke["notes"] = "Use only to verify benchmark script; replace with independently verified URLs for final external evaluation."
    smoke.to_csv(out / f"benchmark_smoke_20_{version}.csv", index=False)

    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)
    importance.to_csv(out / f"feature_importance_{version}.csv", index=False)

    metrics = {
        "version": version,
        "dataset_rows_after_cleaning": int(len(df)),
        "sample_rows": int(len(sample)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "feature_count": len(feature_names),
        "features": feature_names,
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_label_0": float(precision),
        "recall_label_0": float(recall),
        "f1_label_0": float(f1),
        "confusion_matrix_labels_sorted": labels,
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
        "label_mapping_assumption": {
            "0": "phishing (project assumption; verify against dataset documentation)",
            "1": "legitimate (project assumption; verify against dataset documentation)"
        },
        "https_included": bool(include_https),
        "random_state": seed,
    }
    with (out / f"metrics_{version}.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return model, metrics, holdout_50
