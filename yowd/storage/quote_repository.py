"""Saves and finds quotes (including rejected ones)."""
from yowd.models.quote import Quote
from yowd.storage.json_store import JsonStore

_NAME = "quotes"


class QuoteRepository:
    """Quote persistence."""

    def __init__(self, store: JsonStore) -> None:
        """Bind to a store."""
        self._store = store

    def save(self, quote: Quote) -> None:
        """Insert the quote, or replace it if the ID already exists."""
        records = [
            r for r in self._store.load_list(_NAME)
            if r["quote_id"] != quote.quote_id
        ]
        records.append(quote.to_dict())
        self._store.save(_NAME, records)

    def get(self, quote_id: str) -> Quote | None:
        """Return the quote with this ID, if any."""
        for record in self._store.load_list(_NAME):
            if record["quote_id"] == quote_id:
                return Quote.from_dict(record)
        return None

    def for_customer(self, customer_id: str) -> list[Quote]:
        """Return all quotes belonging to a customer."""
        return [
            Quote.from_dict(r) for r in self._store.load_list(_NAME)
            if r["customer_id"] == customer_id
        ]
