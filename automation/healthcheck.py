"""CLI for checking HTTP endpoints with bounded retries and JSON reports."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class ConfigError(ValueError):
    """Configuration could not be safely interpreted."""


@dataclass(frozen=True)
class Endpoint:
    name: str
    url: str
    expected_status: int = 200
    timeout_seconds: float = 5.0
    retries: int = 1


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    status: int | None
    attempts: int
    error: str | None


def parse_endpoint(raw: object) -> Endpoint:
    if not isinstance(raw, dict):
        raise ConfigError("Each endpoint must be an object")
    name = raw.get("name")
    url = raw.get("url")
    if not isinstance(name, str) or not name.strip():
        raise ConfigError("Endpoint name must be a nonempty string")
    if not isinstance(url, str):
        raise ConfigError(f"{name}: URL must be a string")
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ConfigError(f"{name}: URL must use HTTP or HTTPS")
    if parsed.username or parsed.password:
        raise ConfigError(f"{name}: credentials in URLs are not allowed")
    status = raw.get("expected_status", 200)
    timeout = raw.get("timeout_seconds", 5)
    retries = raw.get("retries", 1)
    if type(status) is not int or not 100 <= status <= 599:
        raise ConfigError(f"{name}: expected_status must be 100..599")
    if type(timeout) not in (int, float) or not 0.1 <= timeout <= 60:
        raise ConfigError(f"{name}: timeout_seconds must be 0.1..60")
    if type(retries) is not int or not 0 <= retries <= 5:
        raise ConfigError(f"{name}: retries must be 0..5")
    return Endpoint(name.strip(), url, status, float(timeout), retries)


def load_config(path: str | Path) -> list[Endpoint]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Cannot read configuration: {type(exc).__name__}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("endpoints"), list):
        raise ConfigError("Config must have an endpoints array")
    endpoints = [parse_endpoint(item) for item in document["endpoints"]]
    if not endpoints:
        raise ConfigError("At least one endpoint is required")
    if len({item.name for item in endpoints}) != len(endpoints):
        raise ConfigError("Endpoint names must be unique")
    return endpoints


def check_endpoint(
    endpoint: Endpoint,
    token: str | None = None,
    opener: Callable = urlopen,
    sleeper: Callable = time.sleep,
) -> CheckResult:
    if token and urlsplit(endpoint.url).scheme != "https":
        raise ConfigError(f"{endpoint.name}: bearer token requires HTTPS")
    headers = {"User-Agent": "python-automation-starter/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    status = None
    error = None
    for attempt in range(1, endpoint.retries + 2):
        request = Request(endpoint.url, headers=headers, method="GET")
        try:
            with opener(request, timeout=endpoint.timeout_seconds) as response:
                status = response.getcode()
            if status == endpoint.expected_status:
                return CheckResult(endpoint.name, True, status, attempt, None)
            error = f"Unexpected HTTP status {status}"
        except HTTPError as exc:
            status = exc.code
            exc.close()
            if status == endpoint.expected_status:
                return CheckResult(endpoint.name, True, status, attempt, None)
            error = f"Unexpected HTTP status {status}"
        except (URLError, TimeoutError, OSError) as exc:
            status = None
            # Avoid writing request URLs or potentially sensitive exception strings.
            error = f"Request failed ({type(exc).__name__})"
        if attempt <= endpoint.retries:
            sleeper(min(2 ** (attempt - 1), 8))
    return CheckResult(endpoint.name, False, status, endpoint.retries + 1, error)


def run(endpoints: list[Endpoint], token: str | None = None) -> list[CheckResult]:
    return [check_endpoint(endpoint, token=token) for endpoint in endpoints]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="examples/endpoints.json")
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args(argv)
    try:
        endpoints = load_config(args.config)
        results = run(endpoints, token=os.environ.get("AUTOMATION_API_TOKEN"))
        report = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "total": len(results),
            "passed": sum(result.ok for result in results),
            "results": [asdict(result) for result in results],
        }
        if args.output:
            Path(args.output).write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        for result in results:
            print(f"{'PASS' if result.ok else 'FAIL'} {result.name} "
                  f"status={result.status} attempts={result.attempts}")
        return 0 if all(result.ok for result in results) else 1
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Output error: {type(exc).__name__}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
