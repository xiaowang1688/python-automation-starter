# Case study: Payment settlement reconciliation automation

**Role focus:** Python data automation / QA / backend scripting.

## Business problem
Compare an order export against a settlement export and automatically identify incomplete, unexpected, or incorrect settlement data.

## Implementation
- Two CSV inputs joined by order ID with strict field and duplicate validation.
- Decimal money arithmetic (never binary floating point for currency).
- Stable sorted exceptions: missing settlement, unexpected settlement, amount mismatch, or currency mismatch.
- Machine-readable JSON audit report; failure exit code signals inconsistencies to CI/schedulers.
- Offline regression tests and **synthetic data only**; no customer data or payment credentials.

## Reproduce
Run from repository root:

~~~bash
python -m unittest tests.test_reconcile -v
python -m automation.reconcile --orders examples/orders.csv --settlements examples/settlements.csv --output reconciliation-report.json
~~~

The synthetic fixtures **intentionally contain 3 discrepancies** and return exit code 1. This demonstrates exception detection, not a broken script.

Return codes: 0 = fully matched, 1 = discrepancies found, 2 = invalid input.

[Python source](../../automation/reconcile.py) · [Unit tests](../../tests/test_reconcile.py) · [CI](../../.github/workflows/ci.yml)

**Limitations:** This example assumes one settlement row per order, uppercase 3-letter currencies and 2-decimal amounts. Production work would need fee rules, partial refunds, many-to-one settlements and access controls.
