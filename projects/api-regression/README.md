# Case study: API regression test automation

**Role focus:** Python automation engineer / QA automation / API testing.

## Business scenario

Release teams often re-check the same API responses manually. A declarative test runner turns those checks into a repeatable, reportable pipeline.

## Implementation

- JSON test suite: HTTP GET/POST, expected status, nested JSON field assertions, timeout.
- Request execution via Python standard-library urllib.
- Machine-readable JSON results and **JUnit XML**, useful for CI integration.
- Validation rejects malformed suites and credentials embedded in URLs.
- HTTP response reads are capped at 1 MiB; reports do not include response bodies, URLs, or headers.
- Deterministic offline unit tests mock HTTP calls; no live service dependency in CI.

## Run (repository root)

~~~bash
python -m unittest tests.test_api_regression -v
python -m automation.api_regression --suite examples/api_cases.json --json-report api-results.json --junit-report api-junit.xml
~~~

The provided suite calls public demo APIs and is intended for optional interactive demonstration. The demo services' uptime is not guaranteed. The *offline tests* establish repeatability.

Exit status: 0 = success, 1 = assertion failure, 2 = invalid config/output path.

[Source](../../automation/api_regression.py) · [Tests](../../tests/test_api_regression.py) · [CI](../../.github/workflows/ci.yml)

**Scope:** Demonstration implementation, not a production OpenAPI conformance platform or a claim of commercial deployments.
