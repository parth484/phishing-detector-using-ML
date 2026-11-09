"""Feature extraction and full inference latency profiling."""
from __future__ import annotations
import statistics
import time
from .features import extract_features
from .engine import predict_url, clear_model_cache


def _summary(samples_ms):
    values = sorted(samples_ms)
    if not values:
        return {}
    p95_index = min(len(values) - 1, int(0.95 * (len(values) - 1)))
    return {
        "count": len(values),
        "mean_ms": statistics.fmean(values),
        "median_ms": statistics.median(values),
        "p95_ms": values[p95_index],
        "max_ms": max(values),
        "min_ms": min(values),
    }


def profile_extractor(urls):
    samples = []
    for url in urls:
        start = time.perf_counter()
        extract_features(url)
        samples.append((time.perf_counter() - start) * 1000)
    return _summary(samples)


def profile_inference(urls, artifact_dir="artifacts", version="v3"):
    urls = list(urls)
    if not urls:
        return {"cold_start_ms": None, "warm_inference": {}}

    clear_model_cache()
    start = time.perf_counter()
    predict_url(urls[0], artifact_dir=artifact_dir, version=version)
    cold_start_ms = (time.perf_counter() - start) * 1000

    warm_samples = []
    for url in urls:
        start = time.perf_counter()
        predict_url(url, artifact_dir=artifact_dir, version=version)
        warm_samples.append((time.perf_counter() - start) * 1000)

    return {
        "cold_start_ms": cold_start_ms,
        "warm_inference": _summary(warm_samples),
    }
