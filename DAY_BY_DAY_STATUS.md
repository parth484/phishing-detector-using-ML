# Day-by-day ML pipeline guide and completion criteria

This file separates code availability from work that still requires execution or external evidence.

| Day | Deliverable | Completion evidence |
|---|---|---|
| 1 | Dataset audit | Save terminal output or dataset audit report |
| 2 | Feature extractor | 22-feature dictionary for sample URLs |
| 3 | Baseline V2 model | V2 model files and metrics JSON |
| 4 | Standalone prediction | Successful `predict_url` call using V2 |
| 5 | Entropy | Constant-string entropy 0; uniform 8-symbol string entropy 3 |
| 6 | Optimization | Benchmark output; mean under 15 ms/URL on target machine |
| 7 | Error handling | Invalid-input tests pass |
| 8 | 50-URL holdout | Holdout evaluation JSON and confusion matrix |
| 9 | Engine integration | Same extractor and model artifacts used by inference |
| 10 | Model cache | Cache info shows repeated artifact loads are reused |
| 11 | 20-case benchmark | User-provided 10+10 independently labelled benchmark completed |
| 12 | Latency profile | Extractor and full inference mean/P95/max reported |
| 13 | Final metrics | Precision, recall, F1 and confusion matrix saved |
| 14 | Architecture | `architecture.mmd` reviewed/rendered |
| 15 | Final review | Required artifact checklist passes; limitations documented |

Days 10 and 11 are adapted for the ML-only scope: Streamlit's `st.cache_resource` belongs to the UI integration layer, so this package uses a process-level cached loader. The independent 20-case benchmark cannot be honestly completed without a user-supplied, verified set of current URLs and labels.
