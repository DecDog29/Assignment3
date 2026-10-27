import pytest

from yowd import validation as v


def test_non_blank_rejects_empty():
    with pytest.raises(v.ValidationError):
        v.non_blank("   ", "Name")


def test_positive_float_rejects_text_and_zero():
    with pytest.raises(v.ValidationError):
        v.positive_float("abc")
    with pytest.raises(v.ValidationError):
        v.positive_float("0")
    assert v.positive_float("2.5") == 2.5


def test_phone_and_email():
    assert v.phone("0412 345 678") == "0412345678"
    with pytest.raises(v.ValidationError):
        v.phone("12")
    with pytest.raises(v.ValidationError):
        v.email("not-an-email")
