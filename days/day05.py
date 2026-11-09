"""Day 5: Shannon entropy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.phishing_ml.features import shannon_entropy
for value in ["aaaaaaaa","a8x#p2q!","", "https://example.com"]:
 print(repr(value), "entropy =", round(shannon_entropy(value),4))
assert shannon_entropy("aaaaaaaa")==0
assert abs(shannon_entropy("a8x#p2q!")-3.0)<1e-9
print("Entropy checks passed.")
