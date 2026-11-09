"""Day 15: final review checklist and report generation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

checks = [
    ("Feature extractor", "src/phishing_ml/features.py"),
    ("Dataset utilities", "src/phishing_ml/data.py"),
    ("Training pipeline", "src/phishing_ml/model.py"),
    ("Prediction engine", "src/phishing_ml/engine.py"),
    ("V2 model", "artifacts/rf_model_v2.joblib"),
    ("V3 model", "artifacts/rf_model_v3.joblib"),
    ("V3 medians", "artifacts/url_medians_v3.joblib"),
    ("V3 feature list", "artifacts/url_features_v3.joblib"),
    ("V3 metrics", "artifacts/metrics_v3.json"),
    ("50 URL holdout", "artifacts/holdout_50_v3.csv"),
    ("Feature importance", "artifacts/feature_importance_v3.csv"),
    ("20-row benchmark smoke test", "artifacts/benchmark_smoke_20_v3.csv"),
]

lines = [
    "# Day 15 — Final ML Pipeline Review",
    "",
    "| Component | Status |",
    "|---|---|",
]
missing = []
for label, rel in checks:
    ok = Path(rel).exists()
    lines.append(f"| {label} | {'PASS' if ok else 'PENDING'} |")
    if not ok:
        missing.append(rel)

lines += [
    "",
    "## External / manual completion",
    "",
    "- Day 11 independent benchmark requires 20 independently verified URLs (10 phishing label 0 and 10 legitimate label 1) with source notes.",
    "- Confirm the dataset's numeric label mapping from the dataset documentation.",
    "- Repeat tests on a newly collected independent dataset before claiming real-world performance.",
    "- Streamlit UI, vision, threat-intelligence heuristics and fusion belong to other team roles and are intentionally excluded.",
    "",
]
if missing:
    lines += ["## Missing generated artifacts", ""] + [f"- {item}" for item in missing]
else:
    lines += ["Core ML source files and V2/V3 training artifacts are present."]

Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/final_review.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
