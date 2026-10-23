# Case study: HTTP service log triage automation

**Role focus:** Python automation / reliability / QA diagnostics.

## Business scenario
Identify HTTP server-error bursts and high response latency without manually reading thousands of raw log lines.

## Implementation
- Reads NDJSON records with timestamp, service, HTTP status and request latency.
- Validates event format and normalizes timezone-aware timestamps to UTC.
- Groups by service + minute; computes 5xx error rate and nearest-rank p95 latency.
- Uses configurable error and latency thresholds plus a minimum event count.
- Outputs only aggregates, not original requests, IP addresses, cookies, or URLs.
- Offline tests cover healthy and anomalous windows, low traffic, grouping, invalid data.

## Reproduce

~~~bash
python -m unittest tests.test_log_triage -v
python -m automation.log_triage --input examples/http_logs.ndjson --output log-triage-report.json --min-requests 3
~~~

The synthetic fixture deliberately triggers alerts (exit code 1). Exit status: 0 = no alerts, 1 = alert(s), 2 = invalid log or report.

[Source](../../automation/log_triage.py) · [Tests](../../tests/test_log_triage.py) · [CI](../../.github/workflows/ci.yml)

**Limitations:** This is a small batch analytics demonstration, not a production monitoring or centralized log collection service. It computes an exact in-memory p95 per minute; higher throughput systems need streaming quantiles and alert deduplication.
