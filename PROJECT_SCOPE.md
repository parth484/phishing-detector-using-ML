# Project scope — Parth's ML & Feature Pipeline Lead work

Included:
- Dataset ingestion, audit, cleaning and balanced sampling
- URL lexical/domain feature extraction
- Shannon entropy
- Feature extractor input validation and error handling
- Feature extraction benchmark
- Random Forest training and versioned artifacts
- Holdout evaluation and prediction engine
- In-process cached model loading
- Dataset-derived benchmark smoke test and independent benchmark template
- Latency profiling
- Precision, recall, F1, confusion matrix and feature importance
- Architecture flowchart and final review report

Intentionally excluded because they belong to other team roles:
- Streamlit UI, dashboard layout, risk gauges and report UI
- Screenshot/image upload and Gemini Vision analysis
- Threat-intelligence TLD lists and brand-typosquatting heuristics
- Threat-fusion scoring and end-to-end UI integration

The prediction engine is designed as a reusable ML subsystem that the rest of the team can call.\n