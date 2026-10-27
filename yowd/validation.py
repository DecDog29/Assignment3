import re
from collections.abc import Sequence

_PHONE_RE = re.compile(r"^\+?\d{8,12}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def non_blank(value: str, field: str = "Value") -> str:
    """Return the stripped text, rejecting empty or whitespace-only input."""
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"{field} cannot be blank.")
    return cleaned


def positive_float(value: str, field: str = "Value") -> float:
    """Parse a number greater than zero."""
    try:
        number = float(value)
    except ValueError:
        raise ValidationError(f"{field} must be a number.") from None
    if number <= 0:
        raise ValidationError(f"{field} must be greater than zero.")
    return number


def positive_int(value: str, field: str = "Value") -> int:
    """Parse a whole number greater than zero."""
    try:
        number = int(value)
    except ValueError:
        raise ValidationError(f"{field} must be a whole number.") from None
    if number <= 0:
        raise ValidationError(f"{field} must be greater than zero.")
    return number


def phone(value: str, field: str = "Phone") -> str:
    """Accept 8-12 digits with an optional leading '+'; spaces ignored."""
    cleaned = value.replace(" ", "").replace("-", "")
    if not _PHONE_RE.match(cleaned):
        raise ValidationError(
            f"{field} must be 8-12 digits (e.g. 0412345678)."
        )
    return cleaned


def email(value: str, field: str = "Email") -> str:
    """Accept a basic name@domain.tld address."""
    cleaned = value.strip()
    if not _EMAIL_RE.match(cleaned):
        raise ValidationError(f"{field} must look like name@example.com.")
    return cleaned


def one_of(value: str, options: Sequence[str], field: str = "Choice") -> str:
    """Accept a value that matches one of ``options`` (case-insensitive)."""
    lookup = {opt.lower(): opt for opt in options}
    key = value.strip().lower()
    if key not in lookup:
        raise ValidationError(f"{field} must be one of: {', '.join(options)}.")
    return lookup[key]


def bounded_float(
    value: str, low: float, high: float, field: str = "Value"
) -> float:
    """Parse a number between ``low`` and ``high`` inclusive."""
    try:
        number = float(value)
    except ValueError:
        raise ValidationError(f"{field} must be a number.") from None
    if number < low or number > high:
        raise ValidationError(f"{field} must be between {low} and {high}.")
    return number


def postcode(value: str, field: str = "Postcode") -> str:
    """Accept a Greater Melbourne postcode (3000-3999)."""
    cleaned = value.strip()
    if not cleaned.isdigit() or len(cleaned) != 4:
        raise ValidationError(f"{field} must be 4 digits.")
    if not 3000 <= int(cleaned) <= 3999:
        raise ValidationError(
            f"{field} must be a Victorian postcode (3000-3999)."
        )
    return cleaned
