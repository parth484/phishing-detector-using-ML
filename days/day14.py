"""Day 14: Architecture flowchart."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pathlib import Path
p=Path("architecture.mmd")
if not p.exists(): raise SystemExit("architecture.mmd is included in the project root.")
print(p.read_text())
