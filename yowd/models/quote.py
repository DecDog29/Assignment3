"""Quote class: price, estimated times and the customer's decision."""
from datetime import datetime, timedelta
from typing import Any

from yowd import validation
from yowd.constants import (
    BASE_FEE,
    FEE_PER_KG,
    FEE_PER_PARCEL,
    WAREHOUSE_POSTCODE,
)
from yowd.models.address import Address
from yowd.models.enums import QuoteStatus
from yowd.models.parcel import Parcel


class QuoteError(Exception):
    """Raised when a quote action is not allowed in its current state."""


def _zone(drop_off: Address) -> int:
    """Return 0, 1 or 2 depending on how far the postcode is from the depot."""
    distance = abs(int(drop_off.postcode) - WAREHOUSE_POSTCODE)
    if distance <= 50:
        return 0
    if distance <= 150:
        return 1
    return 2


def calculate_price(drop_off: Address, parcels: list[Parcel]) -> float:
    """Work out the price from the parcels and the drop-off zone."""
    price = BASE_FEE
    price += FEE_PER_PARCEL * len(parcels)
    price += FEE_PER_KG * sum(p.weight_kg for p in parcels)
    price += (0, 8, 15)[_zone(drop_off)]
    return round(price, 2)


class Quote:
    """A proposed price and timeframe for a delivery.

    A quote is built from an address and parcels, not from a Delivery,
    because the Delivery only exists once the quote is accepted (A3).
    """

    def __init__(
        self,
        quote_id: str,
        customer_id: str,
        drop_off: Address,
        parcels: list[Parcel],
        price: float,
        est_pickup: datetime,
        est_delivery: datetime,
        prepared_by_office: bool = False,
        status: QuoteStatus = QuoteStatus.PENDING,
    ) -> None:
        """Store the quote details."""
        self.quote_id = quote_id
        self.customer_id = customer_id
        self.drop_off = drop_off
        self.parcels = parcels
        self.price = price
        self.est_pickup = est_pickup
        self.est_delivery = est_delivery
        self.prepared_by_office = prepared_by_office
        self.status = status

    @classmethod
    def create(
        cls,
        quote_id: str,
        customer_id: str,
        drop_off: Address,
        parcels: list[Parcel],
        now: datetime | None = None,
    ) -> "Quote":
        """Calculate a new pending quote automatically."""
        if not parcels:
            raise validation.ValidationError("Add at least one parcel.")
        now = now or datetime.now()
        pickup = now + timedelta(hours=2)
        delivery = pickup + timedelta(hours=2 + _zone(drop_off))
        price = calculate_price(drop_off, parcels)
        return cls(
            quote_id, customer_id, drop_off, list(parcels), price,
            pickup, delivery,
        )

    def override_price(self, new_price: float) -> None:
        """Let office staff replace the automatic price (A4)."""
        self._require_pending()
        if new_price <= 0:
            raise validation.ValidationError("Price must be above zero.")
        self.price = round(new_price, 2)
        self.prepared_by_office = True

    def accept(self) -> None:
        """Record that the customer accepted the quote."""
        self._require_pending()
        self.status = QuoteStatus.ACCEPTED

    def reject(self) -> None:
        """Record that the customer rejected the quote."""
        self._require_pending()
        self.status = QuoteStatus.REJECTED

    def revise(
        self,
        new_quote_id: str,
        drop_off: Address | None = None,
        parcels: list[Parcel] | None = None,
        now: datetime | None = None,
    ) -> "Quote":
        """Return a new pending quote for changed details.

        This quote is left untouched; the revision only replaces it if the
        customer accepts it (A5).
        """
        return Quote.create(
            new_quote_id,
            self.customer_id,
            drop_off or self.drop_off,
            parcels if parcels is not None else self.parcels,
            now,
        )

    def is_overdue(self, now: datetime | None = None) -> bool:
        """Return True once the estimated delivery time has passed."""
        return (now or datetime.now()) > self.est_delivery

    def _require_pending(self) -> None:
        if self.status is not QuoteStatus.PENDING:
            raise QuoteError(
                f"Quote {self.quote_id} is already {self.status.value}."
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a dictionary."""
        return {
            "quote_id": self.quote_id,
            "customer_id": self.customer_id,
            "drop_off": self.drop_off.to_dict(),
            "parcels": [p.to_dict() for p in self.parcels],
            "price": self.price,
            "est_pickup": self.est_pickup.isoformat(),
            "est_delivery": self.est_delivery.isoformat(),
            "prepared_by_office": self.prepared_by_office,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quote":
        """Rebuild a Quote from stored data."""
        return cls(
            data["quote_id"],
            data["customer_id"],
            Address.from_dict(data["drop_off"]),
            [Parcel.from_dict(p) for p in data["parcels"]],
            float(data["price"]),
            datetime.fromisoformat(data["est_pickup"]),
            datetime.fromisoformat(data["est_delivery"]),
            data["prepared_by_office"],
            QuoteStatus(data["status"]),
        )
