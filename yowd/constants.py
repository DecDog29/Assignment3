from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Assignment 2 design: all pickups happen at the YOWD warehouse, so only
# the drop-off address is stored on a Delivery (change log item C2).
WAREHOUSE_ADDRESS = "1 Depot Road, Melbourne VIC 3000"

# Prefixes for generated identifiers (see services/ids.py).
TRACKING_PREFIX = "YD"
CUSTOMER_PREFIX = "CU"
STAFF_PREFIX = "ST"
QUOTE_PREFIX = "QT"
PAYMENT_PREFIX = "PY"
ISSUE_PREFIX = "IS"

# Area 1 pricing (Quote works out its own price, simplification S2)
WAREHOUSE_POSTCODE = 3000
BASE_FEE = 10.0
FEE_PER_PARCEL = 4.0
FEE_PER_KG = 1.5
MAX_PARCEL_WEIGHT_KG = 25.0
