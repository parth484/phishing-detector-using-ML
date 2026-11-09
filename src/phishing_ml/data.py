"""Dataset loading, validation, cleaning, and deterministic sampling."""
from __future__ import annotations
from pathlib import Path
import pandas as pd


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Put urllinks.csv in the project root "
            "or pass --csv /path/to/urllinks.csv."
        )
    df = pd.read_csv(path, low_memory=False)
    required = {"URL", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    df = df.dropna(subset=["URL", "label"]).copy()
    df["URL"] = df["URL"].astype(str).str.strip()
    df = df[df["URL"].ne("")]
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])
    if not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError("Expected binary labels 0 and 1 in column 'label'.")
    df["label"] = df["label"].astype(int)

    # Remove URL records with contradictory labels before deduplicating.
    label_counts = df.groupby("URL")["label"].nunique()
    conflicting = label_counts[label_counts > 1].index
    df = df[~df["URL"].isin(conflicting)]
    df = df.drop_duplicates(subset=["URL"], keep="first").reset_index(drop=True)
    return df


def balanced_sample(df: pd.DataFrame, per_class: int = 5000, seed: int = 42) -> pd.DataFrame:
    counts = df["label"].value_counts()
    if not {0, 1}.issubset(set(counts.index)):
        raise ValueError(f"Both labels 0 and 1 are required. Found: {counts.to_dict()}")
    if (counts.loc[[0, 1]] < per_class).any():
        raise ValueError(
            f"Need {per_class} rows per class; available: "
            f"{counts.loc[[0, 1]].to_dict()}"
        )
    return (
        df.groupby("label", group_keys=False)
        .sample(n=per_class, random_state=seed)
        .sample(frac=1, random_state=seed)
        .reset_index(drop=True)
    )
