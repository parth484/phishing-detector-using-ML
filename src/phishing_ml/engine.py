"""Cached inference engine shared by scripts and any future application layer."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from .features import extract_features


@lru_cache(maxsize=4)
def _load_bundle(model_path: str, medians_path: str, features_path: str):
    """Load artifacts once per process; subsequent calls reuse them."""
    model = joblib.load(model_path)
    medians = joblib.load(medians_path)
    feature_names = joblib.load(features_path)
    return model, medians, feature_names


def clear_model_cache():
    _load_bundle.cache_clear()


def predict_url(url: str, artifact_dir: str | Path = "artifacts",
                version: str = "v3") -> dict:
    base = Path(artifact_dir)
    model_path = str((base / f"rf_model_{version}.joblib").resolve())
    medians_path = str((base / f"url_medians_{version}.joblib").resolve())
    features_path = str((base / f"url_features_{version}.joblib").resolve())

    for path in (model_path, medians_path, features_path):
        if not Path(path).exists():
            raise FileNotFoundError(
                f"Missing model artifact: {path}. Run the training step first."
            )

    model, medians, feature_names = _load_bundle(
        model_path, medians_path, features_path
    )
    values = extract_features(url)
    missing = set(feature_names) - set(values)
    if missing:
        raise ValueError(f"Feature extractor missing model features: {sorted(missing)}")

    row = pd.DataFrame([values])[feature_names]
    row = row.replace([np.inf, -np.inf], np.nan).fillna(medians)
    predicted = int(model.predict(row)[0])
    class_scores = {
        str(int(cls)): float(score)
        for cls, score in zip(model.classes_, model.predict_proba(row)[0])
    }
    return {
        "url": url,
        "prediction": predicted,
        "class_scores": class_scores,
        "score_interpretation": (
            "Random Forest vote proportions, not calibrated probabilities "
            "and not a guarantee that a URL is safe."
        ),
    }
