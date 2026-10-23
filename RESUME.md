# Xiaowang — Python Automation / QA Automation Engineer

**Based in Mainland China (UTC+8) | Open to international remote employment or contract work**

## Professional summary

Python automation developer focused on reproducible, test-driven workflows for API checks, browser QA, structured logs, business-data validation and command-line operations. Current public work demonstrates executable Python implementations, failure handling, deterministic tests, GitHub Actions and written handover documentation.

**International communication:** Chinese-first; translation-assisted English technical writing and asynchronous collaboration. Spoken English fluency is not claimed.

## Relevant engineering experience — demonstrable projects

These points summarize **implemented portfolio work**. They are not attributed to fictional employers, paying clients, or unverified years of employment.

**API monitoring and fault handling**
- Built a configurable HTTP monitor for multiple endpoints with bounded retries, explicit timeouts, expected-status checking and JSON reports.
- Added opt-in HTTPS bearer-token support while preventing authenticated redirects and avoiding logged credentials.
- Evidence: [code](automation/healthcheck.py) / [tests](tests/test_healthcheck.py)

**API test automation**
- Implemented declarative GET/POST regression cases, nested JSON assertions and actionable failures.
- Generated JSON and JUnit XML result formats for QA review and CI integration.
- Evidence: [code](automation/api_regression.py) / [tests](tests/test_api_regression.py)

**Business-process automation**
- Developed a CSV order-to-settlement comparison workflow using decimal-safe calculations, strict schema validation and four discrepancy categories.
- Produced structured reports to support exception review and automated pipelines using synthetic transaction-like examples.
- Evidence: [code](automation/reconcile.py) / [case study](projects/finance-reconciliation/README.md)

**Observability and log analysis**
- Built a structured NDJSON log processor that buckets records by UTC service-minute and identifies high HTTP 5xx rates and p95 latency.
- Added threshold-based alerts, input checks and offline regression tests.
- Evidence: [code](automation/log_triage.py) / [tests](tests/test_log_triage.py)

**Browser QA automation**
- Wrote Playwright tests executing against real headless Chromium, covering successful order form submissions and input validation failures.
- Added a separate browser CI workflow with screenshot artifacts as reviewable proof of execution.
- Evidence: [browser tests](browser_tests/test_order_portal.py) / [CI](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/browser-e2e.yml)

**Additional Python security tooling**
- Built a wrapper around Mythril's CLI that scans Solidity examples with timeouts, stdout/stderr capture and process status handling.
- Added offline mocked unit tests; the code does not claim to certify or audit deployed smart contracts.
- Evidence: [scanner repository](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner)

## Technical skills with source-code evidence

Python 3, unittest, API/HTTP testing, JSON, CSV, Decimal, file processing, Playwright, Chromium, structured log analysis, Git/GitHub, GitHub Actions CI, command-line automation, subprocess management, Streamlit/Pandas (additional example).

## Preferred opportunities

- Python Automation Engineer / Python Scripting Engineer
- QA Automation / API Testing Engineer
- Browser Test Automation Engineer
- Remote contractor for well-scoped Python and data-processing workflows

## Validation and communication

View [published GitHub profile](https://github.com/xiaowang1688), [complete portfolio](PORTFOLIO.md) and [CI runs](https://github.com/xiaowang1688/python-automation-starter/actions). Projects include runnable instructions, examples, implementation code and passing automated tests. A potential employer can review these directly.

Open a GitHub repository issue for an initial **non-sensitive** technical inquiry; do not post contracts, access keys, or contact details publicly. Establish a private communication channel before sharing confidential information.

---

**中文说明**：这是面向国际远程岗位的、基于真实公开代码的技术经历摘要。所有项目可以核验源代码、自动化测试和 CI。未凭空声明 4–6 年正式工作经历、具体雇主、生产环境规模或付费客户交付记录。如有真实的任职时间与项目背景，可在核实后补充。
