"""Saves and finds customers."""
from yowd.constants import CUSTOMER_PREFIX
from yowd.models.customer import Customer
from yowd.services.ids import IdGenerator
from yowd.storage.json_store import JsonStore
from yowd.validation import ValidationError

_NAME = "customers"


class CustomerRepository:
    """Customer persistence (added in Assignment 3, see change log)."""

    def __init__(self, store: JsonStore, ids: IdGenerator) -> None:
        """Bind to a store and an ID generator."""
        self._store = store
        self._ids = ids

    def all(self) -> list[Customer]:
        """Return every stored customer."""
        return [Customer.from_dict(d) for d in self._store.load_list(_NAME)]

    def find_by_phone(self, phone: str) -> Customer | None:
        """Return the customer with this phone number, if any."""
        for customer in self.all():
            if customer.phone == phone:
                return customer
        return None

    def get(self, customer_id: str) -> Customer | None:
        """Return the customer with this ID, if any."""
        for customer in self.all():
            if customer.person_id == customer_id:
                return customer
        return None

    def register(
        self, name: str, phone: str, email: str, is_account: bool = False
    ) -> Customer:
        """Create and save a new customer; phone numbers must be unique."""
        customer = Customer(
            self._ids.next_id(CUSTOMER_PREFIX), name, phone, email, is_account
        )
        if self.find_by_phone(customer.phone):
            raise ValidationError("A customer with that phone already exists.")
        records = self._store.load_list(_NAME)
        records.append(customer.to_dict())
        self._store.save(_NAME, records)
        return customer
