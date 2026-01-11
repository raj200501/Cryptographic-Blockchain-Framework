import pytest

from acbf.validation import normalize_address, normalize_amount


def test_normalize_address_accepts_valid_names():
    assert normalize_address("Alice") == "alice"
    assert normalize_address("miner-01") == "miner-01"


def test_normalize_address_rejects_invalid():
    with pytest.raises(ValueError):
        normalize_address("")
    with pytest.raises(ValueError):
        normalize_address("??")


def test_normalize_amount():
    assert normalize_amount("10") == 10.0
    with pytest.raises(ValueError):
        normalize_amount(0)
