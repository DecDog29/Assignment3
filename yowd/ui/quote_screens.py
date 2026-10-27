"""Area 1 screens: identify the customer, enter details, get a quote."""
from collections.abc import Callable

from yowd import validation
from yowd.constants import MAX_PARCEL_WEIGHT_KG, QUOTE_PREFIX
from yowd.models.address import Address
from yowd.models.customer import Customer
from yowd.models.parcel import Parcel
from yowd.models.quote import Quote
from yowd.services.ids import IdGenerator
from yowd.storage.customer_repository import CustomerRepository
from yowd.storage.quote_repository import QuoteRepository
from yowd.ui.console import ask, confirm

# Area 2 plugs in here: called with the accepted quote to create a Delivery.
AcceptHandler = Callable[[Quote], None]


def identify_customer(customers: CustomerRepository) -> Customer:
    """Find a customer by phone number, or register a new one."""
    phone = ask("Your phone number", validation.phone)
    customer = customers.find_by_phone(phone)
    if customer:
        print(f"Welcome back, {customer.name}.")
        return customer
    print("No account found for that number. Let's register you.")
    name = ask("Full name", lambda s: validation.non_blank(s, "Name"))
    email = ask("Email", validation.email)
    is_account = confirm("Do you have an invoice (account) arrangement")
    customer = customers.register(name, phone, email, is_account)
    print(f"Registered. Your customer ID is {customer.person_id}.")
    return customer


def enter_address() -> Address:
    """Prompt for each part of the drop-off address."""
    while True:
        street = ask(
            "Street address", lambda s: validation.non_blank(s, "Street")
        )
        suburb = ask("Suburb", lambda s: validation.non_blank(s, "Suburb"))
        code = ask("Postcode", validation.postcode)
        try:
            return Address(street, suburb, code)
        except validation.ValidationError as error:
            print(f"  ! {error}")


def enter_parcel() -> Parcel:
    """Prompt for one parcel."""
    description = ask(
        "Parcel description", lambda s: validation.non_blank(s, "Description")
    )
    weight = ask(
        f"Weight in kg (max {MAX_PARCEL_WEIGHT_KG})",
        lambda s: validation.bounded_float(
            s, 0.1, MAX_PARCEL_WEIGHT_KG, "Weight"
        ),
    )
    return Parcel(description, weight)


def _show_details(address: Address | None, parcels: list[Parcel]) -> None:
    print("\n--- Delivery request so far ---")
    print("Pickup:   YOWD warehouse")
    print(f"Drop-off: {address if address else '(not entered)'}")
    if parcels:
        for number, parcel in enumerate(parcels, start=1):
            print(f"  Parcel {number}: {parcel}")
    else:
        print("  Parcels:  (none yet)")


def _remove_parcel(parcels: list[Parcel]) -> None:
    if not parcels:
        print("  ! There are no parcels to remove.")
        return
    number = ask(
        "Parcel number to remove",
        lambda s: validation.positive_int(s, "Parcel number"),
    )
    if number > len(parcels):
        print("  ! No parcel with that number.")
        return
    removed = parcels.pop(number - 1)
    print(f"Removed: {removed}")


def build_request() -> tuple[Address, list[Parcel]] | None:
    """Let the customer build up (and change) the request.

    Returns None if they cancel.
    """
    address: Address | None = None
    parcels: list[Parcel] = []
    while True:
        _show_details(address, parcels)
        print("\n1. Enter or change drop-off address")
        print("2. Add a parcel")
        print("3. Remove a parcel")
        print("4. Get my quote")
        print("0. Cancel request")
        choice = input("Select an option: ").strip()
        if choice == "1":
            address = enter_address()
        elif choice == "2":
            parcels.append(enter_parcel())
        elif choice == "3":
            _remove_parcel(parcels)
        elif choice == "4":
            if address is None:
                print("  ! Enter a drop-off address first.")
            elif not parcels:
                print("  ! Add at least one parcel first.")
            else:
                return address, parcels
        elif choice == "0":
            return None
        else:
            print("  ! Invalid option, please enter a number from the menu.")


def show_quote(quote: Quote) -> None:
    """Print a quote."""
    print("\n=== Your quote ===")
    print(f"Quote ID:           {quote.quote_id}")
    print(f"Drop-off:           {quote.drop_off}")
    print(f"Parcels:            {len(quote.parcels)}")
    print(f"Price:              ${quote.price:.2f}")
    print(f"Estimated pickup:   {quote.est_pickup:%d %b %Y %I:%M %p}")
    print(f"Estimated delivery: {quote.est_delivery:%d %b %Y %I:%M %p}")


def request_quote_screen(
    customers: CustomerRepository,
    quotes: QuoteRepository,
    ids: IdGenerator,
    on_accept: AcceptHandler,
) -> None:
    """Full Area 1 flow: identify, build request, quote, accept or reject."""
    print("\n--- Request a delivery quote ---")
    customer = identify_customer(customers)
    request = build_request()
    if request is None:
        print("Request cancelled. Nothing was saved.")
        return
    address, parcels = request
    quote = Quote.create(
        ids.next_id(QUOTE_PREFIX), customer.person_id, address, parcels
    )
    show_quote(quote)
    if confirm("Do you accept this quote"):
        quote.accept()
        quotes.save(quote)
        print("Quote accepted.")
        on_accept(quote)
    else:
        quote.reject()
        quotes.save(quote)
        print("Quote rejected. No delivery has been created.")
