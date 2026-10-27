"""Customer class (extends Person)."""
from typing import Any

from yowd.models.enums import Role
from yowd.models.person import Person


class Customer(Person):
    """A person or business that wants a parcel delivered."""

    def __init__(
        self,
        person_id: str,
        name: str,
        phone: str,
        email: str,
        is_account: bool = False,
    ) -> None:
        """Create a customer; account customers are invoiced later."""
        super().__init__(person_id, name, phone, email)
        self._is_account = is_account

    @property
    def role(self) -> Role:
        """Return the customer role."""
        return Role.CUSTOMER

    @property
    def is_account(self) -> bool:
        """Return True if this customer is invoiced later."""
        return self._is_account

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a dictionary."""
        data = super().to_dict()
        data["is_account"] = self._is_account
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Customer":
        """Rebuild a Customer from stored data."""
        return cls(
            data["person_id"],
            data["name"],
            data["phone"],
            data["email"],
            data.get("is_account", False),
        )
