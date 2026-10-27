from datetime import datetime

import pytest

from yowd.models.address import Address
from yowd.models.customer import Customer
from yowd.models.enums import QuoteStatus
from yowd.models.parcel import Parcel
from yowd.models.quote import Quote, QuoteError
from yowd.services.ids import IdGenerator
from yowd.storage.customer_repository import CustomerRepository
from yowd.storage.json_store import JsonStore
from yowd.storage.quote_repository import QuoteRepository
from yowd.validation import ValidationError

NOW = datetime(2026, 10, 30, 9, 0)


def make_quote():
    return Quote.create(
        "QT-0001", "CU-0001", Address("1 High St", "Carlton", "3053"),
        [Parcel("Books", 2.0), Parcel("Shoes", 1.0)], NOW,
    )


def test_address_rejects_bad_postcode_and_blank_street():
    with pytest.raises(ValidationError):
        Address("1 High St", "Carlton", "9999")
    with pytest.raises(ValidationError):
        Address("  ", "Carlton", "3053")


def test_parcel_rejects_bad_weight():
    with pytest.raises(ValidationError):
        Parcel("Box", 0)
    with pytest.raises(ValidationError):
        Parcel("Box", 99)


def test_quote_price_and_times():
    quote = make_quote()
    # 10 base + 2*4 parcels + 3kg*1.5 + 8 zone (postcode 53 from depot)
    assert quote.price == 30.5
    assert quote.est_pickup == datetime(2026, 10, 30, 11, 0)
    assert quote.est_delivery == datetime(2026, 10, 30, 14, 0)


def test_quote_needs_a_parcel():
    with pytest.raises(ValidationError):
        Quote.create("QT-1", "CU-1", Address("1 A St", "X", "3000"), [], NOW)


def test_accept_then_reject_is_blocked():
    quote = make_quote()
    quote.accept()
    assert quote.status is QuoteStatus.ACCEPTED
    with pytest.raises(QuoteError):
        quote.reject()


def test_office_override():
    quote = make_quote()
    quote.override_price(25)
    assert quote.price == 25 and quote.prepared_by_office
    with pytest.raises(ValidationError):
        quote.override_price(-1)


def test_revision_leaves_original_alone():
    quote = make_quote()
    revised = quote.revise(
        "QT-0002", drop_off=Address("9 Far Rd", "Geelong", "3220"), now=NOW
    )
    assert revised.price > quote.price
    assert quote.drop_off.suburb == "Carlton"
    assert revised.status is QuoteStatus.PENDING


def test_overdue():
    quote = make_quote()
    assert not quote.is_overdue(NOW)
    assert quote.is_overdue(datetime(2026, 10, 31))


def test_quote_roundtrip(tmp_path):
    repo = QuoteRepository(JsonStore(tmp_path))
    quote = make_quote()
    quote.reject()
    repo.save(quote)
    loaded = repo.get("QT-0001")
    assert loaded.status is QuoteStatus.REJECTED
    assert loaded.price == quote.price
    assert len(repo.for_customer("CU-0001")) == 1


def test_customer_register_and_duplicate_phone(tmp_path):
    store = JsonStore(tmp_path)
    repo = CustomerRepository(store, IdGenerator(store))
    customer = repo.register("Sam Lee", "0412345678", "sam@example.com")
    assert isinstance(customer, Customer)
    assert repo.find_by_phone("0412345678").name == "Sam Lee"
    with pytest.raises(ValidationError):
        repo.register("Other", "0412345678", "o@example.com")
