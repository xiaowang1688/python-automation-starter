# QA Engineering Evidence — Reproducible Test Strategy

**Target roles:** Python Automation Engineer · API QA · SDET · Playwright QA · Remote Automation Contractor

This page is a technical-review index for recruiters and engineering hiring managers. Every capability listed below maps to code or a reproducible CI job. **These are demonstrable practice implementations using synthetic/offline fixtures**, not a claim of paid customer deliveries or a specific employment duration.

## End-to-end coverage map

| Concern | What is tested | Direct evidence | CI evidence |
| --- | --- | --- | --- |
| API availability | Expected HTTP statuses, timeouts, bounded retries | [Monitor](../automation/healthcheck.py) · [Unit tests](../tests/test_healthcheck.py) | [Python CI](../.github/workflows/ci.yml) |
| API regression | GET/POST requests, JSON field assertions, JUnit output | [API runner](../automation/api_regression.py) · [Tests](../tests/test_api_regression.py) | [Python CI](../.github/workflows/ci.yml) |
| Browser validation | Valid and invalid order form paths | [Playwright tests](../browser_tests/test_order_portal.py) · [UI fixture](../examples/demo_order_portal.html) | [Real Chromium E2E](../.github/workflows/browser-e2e.yml) |
| Data correctness | Missing/unexpected settlement, amount and currency mismatch | [Reconciliation](../automation/reconcile.py) · [Tests](../tests/test_reconcile.py) | [Python CI and JSON artifacts](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml) |
| Service reliability | Minute-level 5xx rate and nearest-rank p95 | [Log triage](../automation/log_triage.py) · [Tests](../tests/test_log_triage.py) | [Python CI and JSON artifacts](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml) |
| Security hygiene | Bearer token only with opt-in HTTPS, no redirect forwarding | [HTTP monitor](../automation/healthcheck.py) · [Security notes](../SECURITY.md) | [Python CI](../.github/workflows/ci.yml) |

## Example test plan: synthetic order workflow

**Business rule (demo fixture):** An order requires an ID matching \`ORD-\` plus four digits, an integer quantity between 1 and 100, and a shipping method.

**Happy path:**
1. Open the self-contained HTML page in Chromium.
2. Enter a valid ID, valid quantity and select Express shipping.
3. Submit once.
4. Assert a success status and the correct ID, quantity and shipping method in the confirmation.

**Negative paths:**
1. Enter a malformed order ID and submit: assert an error without success.
2. Enter quantity 0 and submit: assert range validation.
3. Reload into a fresh browser context for each test to avoid state leakage.

These cases run in a real headless Chromium browser in GitHub Actions and capture screenshots for inspection. They do not interact with a real commerce system.

## Example defect report

**Title:** Invalid order ID is incorrectly accepted during order submission

**Environment:** Local static HTML fixture, Chromium, Python Playwright

**Preconditions:** Form is loaded, quantity = 1, shipping = Standard

**Steps to reproduce:**
1. Enter \`BAD-77\` as Order ID.
2. Click \`Queue order\`.
3. Inspect the status region.

**Expected:** Status is \`error\`; message explains ID format; no order confirmation.

**Observed (hypothetical regression):** Status would be \`success\`, incorrectly confirming an invalid order.

**Verification:** The existing automated test [\`test_rejects_invalid_order_id\`](../browser_tests/test_order_portal.py) would fail if this regression were introduced.

*This is an illustrative bug-report format, not a claim that a customer encountered a live defect.*

## Risk-based testing approach

- **High priority:** authentication, permission boundaries, payment/settlement correctness, data integrity, irreversible actions.
- **Medium priority:** primary user workflows, failure recovery, retries/timeouts, error handling and observability.
- **Lower priority:** purely cosmetic, non-blocking UI inconsistencies.

Test every important failure mode alongside its happy path. Preserve reproducible fixtures and evidence in CI. For real organizations, extend this approach with actual acceptance criteria, environment setup, coverage review, access policies and release signoff.

## Engineering handover

- [Technical résumé](../RESUME.md)
- [International collaboration preferences](INTERNATIONAL_REMOTE.md)
- [Full portfolio](../PORTFOLIO.md)

Contact through the public repository only for nonsensitive discussion; never post customer datasets, keys, or personal information in issues.
