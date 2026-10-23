# Case study: Playwright browser UI automation

**Role focus:** International QA Automation / Test Development / Python Browser Automation.

## Business scenario
A fulfillment team needs confidence that a browser-based order portal accepts valid inputs, displays confirmations, and rejects invalid user submissions after a UI change.

## Implementation
- **Real Chromium browser** driven by Python Playwright, not a mock Page.
- Self-contained HTML/JavaScript fixture representing a demo operations form; no credentials, transactions or external sites.
- Page Object-style semantic selectors via labels and accessible roles.
- Automated checks for the happy path, invalid order IDs and invalid quantities.
- Browser screenshots saved to GitHub Actions artifacts as inspectable test evidence.

## Reproduce locally
Run from the repository root:

~~~bash
python -m pip install -r requirements-browser.txt
python -m playwright install chromium
python -m unittest discover -s browser_tests -v
~~~

The [separate browser CI workflow](../../.github/workflows/browser-e2e.yml) installs Chromium in GitHub Actions and runs the same test suite in a real headless browser.

[UI fixture](../../examples/demo_order_portal.html) · [Browser tests](../../browser_tests/test_order_portal.py) · [Browser CI](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/browser-e2e.yml)

**Scope:** An offline training/test fixture. It demonstrates automation technique but does **not** claim automation of a real client's system, e-commerce provider, or payment platform.
