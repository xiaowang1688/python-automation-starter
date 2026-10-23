# Engineering Case Study — Automated HTTP Health Checks

## Problem

Checking several HTTP endpoints by hand does not provide repeatable verification, useful process exit codes, or structured results for scheduled tasks. A small automation service can make the check consistent.

## Scope and implementation

- JSON configuration supports independent `name`, `url`, `expected_status`, `timeout_seconds`, `retries`, and `auth` settings.
- Input validation rejects invalid URLs, embedded URL credentials, duplicate names, and invalid retry/timeout values.
- Each endpoint uses a bounded retry loop and distinguishes expected from unexpected status codes.
- The CLI writes a structured JSON report with `checked_at`, `total`, `passed` and detailed `results`. Nonzero exit codes allow schedulers and CI jobs to detect failures.
- Authenticated calls require opt-in `"auth": "bearer"`, an HTTPS URL, and the `AUTOMATION_API_TOKEN` environment variable. Authenticated requests do not follow redirects.
- Offline tests inject mock HTTP openers to validate behavior without live network dependencies.

## Architecture

```text
JSON config
    |
    v
Input validation -> Endpoint objects
    |
    v
HTTP check loop -> expected status? -> CheckResult
    |                                  (status, attempts, error)
    v
JSON report + console summary + process exit code
```

## How to verify

```bash
python -m unittest discover -s tests -v
python -m automation.healthcheck --config examples/endpoints.json --output report.json
```

The first command requires no live network. The second demonstrates an actual HTTP check of the configured URL, subject to network connectivity. A successful CI run proves the offline tests ran successfully; it does not promise uptime of external services.

CI workflow: [Python CI](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml), configured for Python 3.10, 3.12, and 3.13.

## Key engineering decisions

| Decision | Reason |
| --- | --- |
| Standard library `unittest` | Deterministic tests without additional test dependencies |
| Bounded retries and timeouts | Avoid hanging indefinitely |
| Explicit exit codes | Allow use from scripts, schedulers, and build pipelines |
| JSON report | Machine-readable diagnostics for subsequent automation |
| Per-endpoint token opt-in and HTTPS | Avoid accidental transmission to unrelated HTTP endpoints |
| No redirects with bearer tokens | Prevent credential forwarding to another URL |
| No committed secrets | Separate code/configuration from access credentials |

## Limitations / Next steps

This is a focused **portfolio/reference implementation**, not a deployed monitoring service or a production SLO platform. Future work could include parallel requests, alerting, rate-limit handling, an optional dry-run, richer HTTP assertions, and monitored examples that do not depend on third-party uptime.
