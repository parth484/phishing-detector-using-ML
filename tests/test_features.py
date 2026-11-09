import math
import pytest
from src.phishing_ml.features import extract_features, shannon_entropy

def test_entropy_known_values():
    assert shannon_entropy("") == 0
    assert shannon_entropy("aaaaaaaa") == 0
    assert math.isclose(shannon_entropy("a8x#p2q!"), 3.0)

def test_expected_feature_schema():
    result = extract_features("https://www.google.com/search?q=python")
    assert len(result) == 22
    assert all(isinstance(v, (int, float)) for v in result.values())

def test_ip_detection():
    assert extract_features("http://192.168.1.1/login")["IsDomainIP"] == 1

def test_https_detection():
    assert extract_features("http://example.com")["IsHTTPS"] == 0
    assert extract_features("https://example.com")["IsHTTPS"] == 1
    # Bare host uses documented HTTPS parsing assumption.
    assert extract_features("example.com")["IsHTTPS"] == 1

@pytest.mark.parametrize("value", ["", "  ", "https://"])
def test_invalid_empty_or_hostless_url(value):
    with pytest.raises(ValueError):
        extract_features(value)

@pytest.mark.parametrize("value", [None, 123, []])
def test_non_string_input(value):
    with pytest.raises(TypeError):
        extract_features(value)

def test_encoded_character_count():
    result = extract_features("https://example.com/%2F?q=1")
    assert result["NoOfObfuscatedChar"] == 1
    assert result["HasObfuscation"] == 1
