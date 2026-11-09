"""Day 7: Input validation and error handling."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.phishing_ml.features import extract_features
cases=["", "   ", None, 123, "https://", "https://example.com/", "example.com"]
for value in cases:
 try: print(repr(value), "->", extract_features(value))
 except (TypeError,ValueError) as exc: print(repr(value), "-> handled:",exc)
