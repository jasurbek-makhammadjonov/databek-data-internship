"""Revenue per customer per month.

Reads orders.csv (order_id, customer_id, amount, created_at), skips invalid
rows (and reports them), then prints revenue per customer per month,
sorted by revenue (highest first).
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime

REQUIRED_COLUMNS = ["order_id", "customer_id", "amount", "created_at"]
DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]


def parse_date(value):
    """Return a datetime, or None if the value matches no known format."""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def validate_row(row, seen_order_ids):
    """Return (clean_values, None) if valid, or (None, reason) if invalid."""
    order_id = (row["order_id"] or "").strip()
    customer_id = (row["customer_id"] or "").strip()
    amount_raw = (row["amount"] or "").strip()
    created_raw = (row["created_at"] or "").strip()

    if not order_id:
        return None, "missing order_id"
    if not customer_id:
        return None, "missing customer_id"
    if order_id in seen_order_ids:
        return None, f"duplicate order_id '{order_id}'"

    try:
        amount = float(amount_raw)
    except ValueError:
        return None, f"amount is not a number: '{amount_raw}'"
    if amount <= 0:
        return None, f"amount must be positive: {amount_raw}"

    created = parse_date(created_raw)
    if created is None:
        return None, f"invalid created_at: '{created_raw}'"

    return (order_id, customer_id, amount, created.strftime("%Y-%m")), None


def main(path="orders.csv"):
    revenue = defaultdict(float)  # (customer_id, month) -> total
    invalid_rows = []
    seen_order_ids = set()

    try:
        f = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        sys.exit(f"Error: file '{path}' not found.")

    with f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"Error: missing columns in CSV: {', '.join(missing)}")

        for line_no, row in enumerate(reader, start=2):  # line 1 is the header
            clean, reason = validate_row(row, seen_order_ids)
            if reason:
                invalid_rows.append((line_no, reason))
                continue
            order_id, customer_id, amount, month = clean
            seen_order_ids.add(order_id)
            revenue[(customer_id, month)] += amount

    # Revenue report, highest revenue first
    print("Revenue per customer per month")
    print(f"{'customer_id':<14}{'month':<10}{'revenue':>12}")
    print("-" * 36)
    for (customer_id, month), total in sorted(
        revenue.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{customer_id:<14}{month:<10}{total:>12.2f}")

    # Invalid rows report
    print(f"\nSkipped {len(invalid_rows)} invalid row(s):")
    for line_no, reason in invalid_rows:
        print(f"  line {line_no}: {reason}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "orders.csv")