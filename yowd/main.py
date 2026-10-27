from collections.abc import Callable

from yowd.models.quote import Quote
from yowd.services.ids import IdGenerator
from yowd.storage.customer_repository import CustomerRepository
from yowd.storage.json_store import JsonStore
from yowd.storage.quote_repository import QuoteRepository
from yowd.ui.console import run_menu
from yowd.ui.quote_screens import request_quote_screen


def _not_implemented(area: str) -> Callable[[], None]:
    def handler() -> None:
        print(f"  [{area}] not implemented yet.")

    return handler


def main() -> None:
    """Start the YOWD console application."""
    store = JsonStore()
    ids = IdGenerator(store)
    customers = CustomerRepository(store, ids)
    quotes = QuoteRepository(store)

    def on_quote_accepted(quote: Quote) -> None:
        # Area 2 (Nhat Long) replaces this to create the Delivery.
        print(f"  [Area 2] Delivery for quote {quote.quote_id} pending.")

    def request_quote() -> None:
        request_quote_screen(customers, quotes, ids, on_quote_accepted)

    print("Your Order We Deliver (YOWD)")
    run_menu(
        "Main Menu - choose your role",
        [
            ("Customer: request a quote", request_quote),
            ("Customer/Office: track or modify a delivery",
             _not_implemented("Area 2")),
            ("Office Staff: allocate delivery staff",
             _not_implemented("Area 3")),
            ("Delivery Staff: update status and record payment",
             _not_implemented("Area 4")),
        ],
    )
    print("Goodbye.")


if __name__ == "__main__":
    main()
