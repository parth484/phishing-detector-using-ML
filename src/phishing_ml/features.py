"""Consistent, deterministic URL feature extraction for training and inference."""
from __future__ import annotations

import ipaddress
import math
import re
from collections import Counter
from string import punctuation
from urllib.parse import urlparse

# A small fallback list for common compound public suffixes. Install tldextract
# for broader public-suffix coverage.
_COMPOUND_SUFFIXES = {
    "ac.in", "co.in", "com.au", "net.au", "org.au", "co.uk", "org.uk",
    "ac.uk", "gov.uk", "com.br", "com.cn", "com.sg", "co.nz", "com.mx",
    "co.jp", "co.za", "com.tr", "com.tw", "com.hk", "com.my",
}
_PERCENT_ESCAPE = re.compile(r"%[0-9a-fA-F]{2}")


def shannon_entropy(value: str) -> float:
    """Calculate Shannon entropy in bits per character; empty input -> 0."""
    if not value:
        return 0.0
    counts = Counter(value)
    total = len(value)
    return float(-sum((n / total) * math.log2(n / total) for n in counts.values()))


def _domain_parts(hostname: str) -> tuple[str, str, str]:
    """Return (subdomain, registrable domain, suffix), with offline fallback."""
    labels = hostname.lower().strip(".").split(".") if hostname else []
    if len(labels) <= 1:
        return "", labels[0] if labels else "", ""
    last_two = ".".join(labels[-2:])
    if last_two in _COMPOUND_SUFFIXES and len(labels) >= 3:
        return ".".join(labels[:-2]), labels[-3], last_two
    return ".".join(labels[:-2]), labels[-2], labels[-1]


def extract_features(url: str) -> dict[str, float | int]:
    """Extract 22 numeric features from a URL string.

    A scheme-less input is parsed as HTTPS for consistency with the previous
    project implementation. This is a parsing assumption, not evidence that
    the remote site actually supports HTTPS.
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    raw = url.strip()
    if not raw:
        raise ValueError("URL cannot be empty")
    if any(ord(ch) < 32 for ch in raw):
        raise ValueError("URL contains control characters")

    parse_input = raw if "://" in raw else "https://" + raw
    try:
        parsed = urlparse(parse_input)
        hostname = parsed.hostname or ""
    except ValueError as exc:
        raise ValueError(f"Malformed URL: {exc}") from exc

    if not hostname:
        raise ValueError("URL hostname is missing")

    # Validate malformed ports/bracketed host syntax without requiring a port.
    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError(f"Malformed URL port: {exc}") from exc

    length = len(raw)
    subdomain, registrable_domain, suffix = _domain_parts(hostname)
    domain_length = len(hostname)
    tld_length = len(suffix)
    subdomain_count = len(subdomain.split(".")) if subdomain else 0

    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    encoded_matches = _PERCENT_ESCAPE.findall(raw)
    obfuscated_count = len(encoded_matches)
    has_obfuscation = int(obfuscated_count > 0 or "@" in raw)

    letters = sum(ch.isalpha() for ch in raw)
    digits = sum(ch.isdigit() for ch in raw)
    equals_count = raw.count("=")
    qmark_count = raw.count("?")
    ampersand_count = raw.count("&")
    other_special = sum(ch in punctuation and ch not in "=?&" for ch in raw)
    special_count = sum(not ch.isalnum() for ch in raw)

    return {
        "URLLength": length,
        "NumberOfDots": raw.count("."),
        "NumberOfHyphens": raw.count("-"),
        "NumberOfSpecialCharacters": special_count,
        "IsDomainIP": is_ip,
        "IsHTTPS": int(parsed.scheme.lower() == "https"),
        "Entropy": shannon_entropy(raw),
        "DomainLength": domain_length,
        "TLDLength": tld_length,
        "NoOfSubDomain": subdomain_count,
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": obfuscated_count,
        "ObfuscationRatio": obfuscated_count / length,
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letters / length,
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digits / length,
        "NoOfEqualsInURL": equals_count,
        "NoOfQMarkInURL": qmark_count,
        "NoOfAmpersandInURL": ampersand_count,
        "NoOfOtherSpecialCharsInURL": other_special,
        "SpacialCharRatioInURL": special_count / length,
    }


FEATURE_NAMES = [
    "URLLength", "NumberOfDots", "NumberOfHyphens",
    "NumberOfSpecialCharacters", "IsDomainIP", "IsHTTPS", "Entropy",
    "DomainLength", "TLDLength", "NoOfSubDomain", "HasObfuscation",
    "NoOfObfuscatedChar", "ObfuscationRatio", "NoOfLettersInURL",
    "LetterRatioInURL", "NoOfDegitsInURL", "DegitRatioInURL",
    "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL", "SpacialCharRatioInURL",
]
