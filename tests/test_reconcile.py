"""Reconciliation tests with synthetic data, no financial accounts."""
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest
from automation.reconcile import Entry, LedgerError, load_ledger, reconcile


def item(name, amount, currency="USD"):
    return Entry(name, currency, Decimal(amount))


class ReconciliationTests(unittest.TestCase):
    def test_synthetic_examples(self):
        left = load_ledger("examples/orders.csv", "amount")
        right = load_ledger("examples/settlements.csv", "settled_amount")
        self.assertEqual([d.category for d in reconcile(left, right)], [
            "amount_mismatch", "missing_settlement", "unexpected_settlement"
        ])

    def test_balanced_payment(self):
        self.assertEqual(reconcile({"A": item("A", "2.00")}, {"A": item("A", "2.00")}), [])

    def test_currency_mismatch(self):
        result = reconcile({"A": item("A", "5.00")}, {"A": item("A", "5.00", "EUR")})
        self.assertEqual(result[0].category, "currency_mismatch")

    def test_duplicate_order_id_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "orders.csv"
            path.write_text("order_id,currency,amount\nX,USD,1.00\nX,USD,2.00\n")
            with self.assertRaises(LedgerError):
                load_ledger(path, "amount")

    def test_rejects_more_than_two_decimal_places(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "orders.csv"
            path.write_text("order_id,currency,amount\nX,USD,1.001\n")
            with self.assertRaises(LedgerError):
                load_ledger(path, "amount")


if __name__ == "__main__":
    unittest.main()
