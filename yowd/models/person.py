"""Abstract Person base class for all human actors."""
from abc import ABC, abstractmethod
from typing import Any

from yowd import validation
from yowd.models.enums import Role


class Person(ABC):
    """Common contact details for Customer, OfficeStaff and DeliveryStaff.

    Person is never instantiated directly (Assignment 2 UML).
    """

    def __init__(
        self, person_id: str, name: str, phone: str, email: str
    ) -> None:
        """Validate and store the shared contact details."""
        self._person_id = person_id
        self._name = validation.non_blank(name, "Name")
        self._phone = validation.phone(phone)
        self._email = validation.email(email)

    @property
    def person_id(self) -> str:
        """Return the unique identifier."""
        return self._person_id

    @property
    def name(self) -> str:
        """Return the person's name."""
        return self._name

    @property
    def phone(self) -> str:
        """Return the contact phone number."""
        return self._phone

    @property
    def email(self) -> str:
        """Return the contact email address."""
        return self._email

    @property
    @abstractmethod
    def role(self) -> Role:
        """Return the system role of this person."""

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly dictionary."""
        return {
            "person_id": self._person_id,
            "name": self._name,
            "phone": self._phone,
            "email": self._email,
            "role": self.role.value,
        }
