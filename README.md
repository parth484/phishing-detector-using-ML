# URL Phishing Detection — ML & Feature Pipeline (Days 1–15)

This package contains **Parth's ML & Feature Pipeline work only**. It excludes the Streamlit UI, image/vision module, threat-intelligence heuristics, and team integration owned by other roles.

## Scope from the team roadmap

- Dataset sourcing and exploration
- URL lexical feature extraction
- Scikit-learn Random Forest training
- Shannon entropy
- Feature extractor optimization
- Input validation and error handling
- Holdout inference testing
- `predict_proba`-style class scores and shared inference engine
- Cached model loading
- Benchmark dataset workflow
- Latency profiling
- Precision, Recall and F1 evaluation
- Architecture flowchart
- Final review checklist

## Folder structure

```text
phishing_ml_day1_to_day15/
├── src/phishing_ml/
│   ├── features.py
│   ├── data.py
│   ├── model.py
│   ├── engine.py
│   ├── evaluation.py
│   ├── latency.py
│   └── benchmark.py
├── days/day01.py ... days/day15.py
├── tests/
├── artifacts/                  # created by training
├── train_model.py
├── predict.py
├── evaluate_holdout.py
├── profile_latency.py
├── feature_importance.py
├── run_benchmark.py
├── architecture.mmd
├── benchmark_urls_template.csv
├── requirements.txt
└── README.md
```

## 1. Setup

Use Python 3.11+. The tested dependency versions are pinned in `requirements.txt`.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:
```cmd
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Put the Kaggle PhiUSIIL CSV in the project root as `urllinks.csv`. The dataset is intentionally not copied into this ZIP.

## 2. Run the 15 days

Each day script can be run separately from the project root:

```bash
python days/day01.py
python days/day02.py
...
python days/day15.py
```

Some days require outputs from previous days. The order below is recommended.

| Day | Script | Work |
|---|---|---|
| 1 | `days/day01.py` | Dataset shape, labels, missing values, duplicates, columns |
| 2 | `days/day02.py` | Extract lexical/domain URL features |
| 3 | `days/day03.py` | Train 18-feature baseline including HTTPS (V2) |
| 4 | `days/day04.py` | Load saved V2 artifacts and run standalone prediction |
| 5 | `days/day05.py` | Shannon entropy and known-value tests |
| 6 | `days/day06.py` | Benchmark feature extraction speed; report mean/median/P95/max |
| 7 | `days/day07.py` | Validate empty, malformed, non-string and normal URLs |
| 8 | `days/day08.py` | Evaluate 50 held-out URLs using the extractor and saved model |
| 9 | `days/day09.py` | Integrate feature extractor with the prediction engine |
| 10 | `days/day10.py` | Confirm cached model loading is reused in-process |
| 11 | `days/day11.py` | Create/prepare 20-case independently labelled benchmark |
| 12 | `days/day12.py` | Profile full inference and feature extraction latency |
| 13 | `days/day13.py` | Report precision, recall, F1, accuracy and confusion matrix |
| 14 | `days/day14.py` | Print architecture flowchart source (`architecture.mmd`) |
| 15 | `days/day15.py` | Verify required scripts and artifacts exist |

## 3. Train the final V3 model

The V3 experiment excludes `IsHTTPS` from training because the supplied dataset showed a very strong label association for HTTPS. The extractor still calculates it, so it remains available for diagnostics. V3 also includes Shannon entropy.

```bash
python train_model.py
```

Defaults:
- 5,000 rows per class (10,000 total)
- duplicate URL removal and conflicting-label removal
- 80/20 stratified train/test split
- `random_state=42`
- Random Forest, 100 trees, `n_jobs=-1`
- Median imputation fitted on training data only
- V3 excludes HTTPS; V2 comparison includes it

To train the V2 baseline:
```bash
python train_model.py --include-https
```

To use fewer rows for a quick smoke test:
```bash
python train_model.py --per-class 100
```

Generated V3 artifacts:
- `artifacts/rf_model_v3.joblib`
- `artifacts/url_medians_v3.joblib`
- `artifacts/url_features_v3.joblib`
- `artifacts/metrics_v3.json`
- `artifacts/feature_importance_v3.csv`
- `artifacts/holdout_50_v3.csv`
- `artifacts/holdout_all_v3.csv`

V2 files use `_v2` names and do not overwrite V3.

## 4. Predict a URL

```bash
python predict.py https://example.com
```

Or:
```bash
python predict.py
```

Use V2:
```bash
python predict.py https://example.com --version v2
```

The `class_scores` are Random Forest vote proportions. They are not calibrated probabilities and are not proof that a URL is safe.

## 5. Holdout evaluation

```bash
python evaluate_holdout.py
```

This re-extracts features for the 50 saved holdout URLs and predicts them through the same inference engine. It evaluates the 50-case subset, not all 2,000 test rows.

## 6. Feature importance

```bash
python feature_importance.py
```

## 7. Latency profiling

```bash
python profile_latency.py
```

Day 6's target is an average extractor runtime below 15 ms/URL. The script reports observed mean, median, P95 and maximum. Hardware and environment affect timing; the target is measured, not guaranteed.

## 8. Day 11 independent benchmark

Run:
```bash
python run_benchmark.py
```

If `benchmark_urls.csv` is missing, the script creates a template and asks for 20 independently verified URLs: 10 phishing (label 0) and 10 legitimate (label 1). Fill source and notes columns. Do not treat the training dataset's held-out sample as an independent live benchmark. This project does not fabricate or ship active phishing URLs.

## 9. Run automated tests

```bash
pytest -q
```

## Feature definitions

The extractor returns 22 numeric features, using one shared implementation for training and prediction. These are **project-defined formulas**. They are not claimed to reproduce every undocumented PhiUSIIL feature formula.

- URL length, dots, hyphens, special-character count
- IP detection, HTTPS scheme indicator, Shannon entropy
- Domain length, suffix length, subdomain count
- Obfuscation flag/count/ratio
- Letter and digit counts/ratios
- Equals, question-mark, ampersand and other-special-character counts/ratios

A scheme-less input is parsed as HTTPS as a convenience; this does not mean the remote website supports HTTPS.

## Important limitations and interpretation

1. Confirm the dataset label mapping from its source documentation before presenting label 0 as phishing and label 1 as legitimate. The scripts retain numeric labels.
2. Random split metrics are internal dataset metrics, not proof of performance on newly collected URLs.
3. HTTPS showed a strong association with labels in the uploaded dataset. V3 excludes it from training as a bias investigation, but other dataset shortcuts may remain.
4. Feature importance is a model diagnostic, not causal evidence.
5. The 20-case benchmark must be filled with independently verified URLs and their provenance.
6. No model score guarantees safety. Use this as a research prototype and never automatically trust or block a URL solely from this classifier.

## Current known results from earlier experiments

The earlier conversation reported:
- Prior 18-feature extractor model: 99.15% on one balanced 10,000-row split.
- Prior 17-feature model without HTTPS: 97.45% on that experiment.
- The original dataset contained 235,795 rows and 56 columns; 425 duplicate URLs were reported before cleaning.

The current package changes the feature set to include entropy and explicit lexical counters, so those previous accuracy figures do **not** automatically apply. Run the scripts to generate fresh metrics for this version.
