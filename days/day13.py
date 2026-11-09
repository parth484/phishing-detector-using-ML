"""Day 13: Precision, recall and F1 metrics."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from pathlib import Path
p=Path("artifacts/metrics_v3.json")
if not p.exists(): raise SystemExit("Run V3 training first: python train_model.py")
m=json.loads(p.read_text())
print("Accuracy:",round(m["accuracy"],4))
print("Label 0 precision:",round(m["precision_label_0"],4))
print("Label 0 recall:",round(m["recall_label_0"],4))
print("Label 0 F1:",round(m["f1_label_0"],4))
print("Confusion matrix (labels order 0,1):",m["confusion_matrix"])
print("Per-class report:",json.dumps(m["classification_report"],indent=2))
