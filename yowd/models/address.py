"""Address data class (drop-off location)."""
from dataclasses import dataclass
from typing import Any

from yowd import validation


@dataclass(frozen=True)
class Address:
    """A Victorian street address. Validated when created."""

    street: str
    suburb: str
    postcode: str

    def __post_init__(self) -> None:
        """Clean and validate every field."""
        object.__setattr__(
            self, "street", validation.non_blank(self.street, "Street")
        )
        object.__setattr__(
            self, "suburb", validation.non_blank(self.suburb, "Suburb")
        )
        object.__setattr__(
            self, "postcode", validation.postcode(self.postcode)
        )

    def __str__(self) -> str:
        """Return a one-line display form."""
        return f"{self.street}, {self.suburb} VIC {self.postcode}"

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a dictionary."""
        return {
            "street": self.street,
            "suburb": self.suburb,
            "postcode": self.postcode,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Address":
        """Rebuild an Address from stored data."""
        return cls(data["street"], data["suburb"], data["postcode"])
