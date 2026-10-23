"""Audit-friendly reconciliation of order and settlement CSV files."""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
import sys


class LedgerError(ValueError):
    """Input rows are malformed or cannot be compared safely."""


@dataclass(frozen=True)
class Entry:
    order_id: str
    currency: str
    amount: Decimal


@dataclass(frozen=True)
class Difference:
    order_id: str
    category: str
    expected: str | None
    actual: str | None


def _parse_amount(raw: str | None, line: int) -> Decimal:
    try:
        value = Decimal(raw)
    except (InvalidOperation, TypeError):
        raise LedgerError(f"Row {line}: invalid amount") from None
    if not value.is_finite() or value < 0 or value != value.quantize(Decimal("0.01")):
        raise LedgerError(f"Row {line}: amount must have 0-2 decimal places and be nonnegative")
    return value


def load_ledger(path: str | Path, amount_column: str) -> dict[str, Entry]:
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            required = {"order_id", "currency", amount_column}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise LedgerError(f"Expected columns: {', '.join(sorted(required))}")
            entries: dict[str, Entry] = {}
            for line, record in enumerate(reader, 2):
                identifier = (record.get("order_id") or "").strip()
                currency = (record.get("currency") or "").strip()
                if not identifier or not re.fullmatch(r"[A-Z]{3}", currency):
                    raise LedgerError(f"Row {line}: invalid order ID or currency")
                if identifier in entries:
                    raise LedgerError(f"Row {line}: duplicate order ID {identifier}")
                entries[identifier] = Entry(
                    identifier, currency, _parse_amount(record.get(amount_column), line)
                )
            if not entries:
                raise LedgerError("Ledger is empty")
            return entries
    except (OSError, UnicodeError, csv.Error) as exc:
        raise LedgerError(f"Cannot read ledger: {type(exc).__name__}") from exc


def reconcile(orders: dict[str, Entry], settlements: dict[str, Entry]) -> list[Difference]:
    result = []
    for identifier in sorted(orders.keys() | settlements.keys()):
        expected, actual = orders.get(identifier), settlements.get(identifier)
        if expected is None:
            result.append(Difference(identifier, "unexpected_settlement", None, str(actual.amount)))
        elif actual is None:
            result.append(Difference(identifier, "missing_settlement", str(expected.amount), None))
        elif expected.currency != actual.currency:
            result.append(Difference(identifier, "currency_mismatch", expected.currency, actual.currency))
        elif expected.amount != actual.amount:
            result.append(Difference(identifier, "amount_mismatch", str(expected.amount), str(actual.amount)))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orders", default="examples/orders.csv")
    parser.add_argument("--settlements", default="examples/settlements.csv")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        orders = load_ledger(args.orders, "amount")
        settlements = load_ledger(args.settlements, "settled_amount")
        differences = reconcile(orders, settlements)
        report = {
            "total_orders": len(orders),
            "total_settlements": len(settlements),
            "difference_count": len(differences),
            "differences": [asdict(difference) for difference in differences],
        }
        content = json.dumps(report, indent=2) + "\n"
        if args.output:
            Path(args.output).write_text(content, encoding="utf-8")
        print(content, end="")
        return 1 if differences else 0
    except (LedgerError, OSError) as exc:
        print(f"Invalid ledger/output: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
