import pytest

from yowd.models.person import Person
from yowd.validation import ValidationError


def test_person_is_abstract():
    with pytest.raises(TypeError):
        Person("P-1", "A", "0412345678", "a@b.com")  # type: ignore[abstract]
