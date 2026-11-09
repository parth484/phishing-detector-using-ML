"""Day 6: Feature extractor speed benchmark."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import time, statistics
from src.phishing_ml.features import extract_features
urls=["https://example.com","https://www.google.com/search?q=python","http://192.168.1.1/login","https://sub.domain.co.uk/a-b?id=12"]
samples=[]
for i in range(5000):
 u=urls[i%len(urls)]; t=time.perf_counter(); extract_features(u); samples.append((time.perf_counter()-t)*1000)
print("URLs:",len(samples))
print("Mean ms:",statistics.fmean(samples))
print("Median ms:",statistics.median(samples))
print("P95 ms:",sorted(samples)[int(.95*(len(samples)-1))])
print("Max ms:",max(samples))
print("Target <15ms/URL:",statistics.fmean(samples)<15)
