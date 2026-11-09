"""Day 2: URL feature extraction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.phishing_ml.features import extract_features
examples=["https://www.google.com/search?q=python","http://192.168.1.1/login","https://example.com/a-b?id=123"]
for url in examples:
 print("\nURL:",url)
 for key,value in extract_features(url).items(): print(f"{key}: {value}")
