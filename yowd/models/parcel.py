"""Parcel data class."""
from dataclasses import dataclass
from typing import Any

from yowd import validation
from yowd.constants import MAX_PARCEL_WEIGHT_KG


@dataclass(frozen=True)
class Parcel:
    """One item being delivered."""

    description: str
    weight_kg: float

    def __post_init__(self) -> None:
        """Validate the description and weight."""
        object.__setattr__(
            self,
            "description",
            validation.non_blank(self.description, "Description"),
        )
        if not 0 < self.weight_kg <= MAX_PARCEL_WEIGHT_KG:
            raise validation.ValidationError(
                f"Weight must be between 0 and {MAX_PARCEL_WEIGHT_KG} kg."
            )

    def __str__(self) -> str:
        """Return a one-line display form."""
        return f"{self.description} ({self.weight_kg} kg)"

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a dictionary."""
        return {"description": self.description, "weight_kg": self.weight_kg}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Parcel":
        """Rebuild a Parcel from stored data."""
        return cls(data["description"], float(data["weight_kg"]))
