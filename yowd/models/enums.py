"""Shared enumerations (agreed contracts between all four areas)."""
from enum import Enum


class DeliveryStatus(Enum):
    """Delivery lifecycle (Assignment 2, assumption A1, simplification S4)."""

    REQUESTED = "Requested"
    ACCEPTED = "Accepted"
    PICKED_UP = "Picked Up"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    ON_HOLD = "On Hold"
    PICKUP_FAILED = "Pickup Failed"


class PaymentStatus(Enum):
    """Payment progress (Payment CRC card)."""

    PENDING = "Pending"
    PAID = "Paid"
    DISPUTED = "Disputed"
    INVOICED = "Invoiced"


class PaymentMethod(Enum):
    """How a payment was made. Processing itself is simulated (A14)."""

    CASH = "Cash"
    CARD = "Card"
    PREPAID = "Pre-paid online"
    INVOICE = "Invoice"


class Role(Enum):
    """System user roles. The business owner is a viewer role (A16)."""

    CUSTOMER = "Customer"
    OFFICE_STAFF = "Office Staff"
    DELIVERY_STAFF = "Delivery Staff"
    OWNER = "Business Owner"


class QuoteStatus(Enum):
    """Quote decision state. Only an accepted quote creates a Delivery."""

    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
