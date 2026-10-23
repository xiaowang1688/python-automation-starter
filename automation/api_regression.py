"""Declarative API regression checks with JSON/JUnit reports (stdlib only)."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from xml.etree.ElementTree import Element, ElementTree, SubElement


class SuiteError(ValueError):
    pass


@dataclass(frozen=True)
class Case:
    name: str
    url: str
    method: str = "GET"
    expected_status: int = 200
    json_contains: dict[str, Any] | None = None
    json_body: dict[str, Any] | None = None
    timeout_seconds: float = 5.0


@dataclass(frozen=True)
class Result:
    name: str
    passed: bool
    status: int | None
    failures: list[str]


def load_suite(path: str | Path) -> list[Case]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SuiteError(f"Cannot read suite: {type(exc).__name__}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list) or not document["cases"]:
        raise SuiteError("Suite needs a nonempty cases array")
    cases = []
    for raw in document["cases"]:
        if not isinstance(raw, dict):
            raise SuiteError("Each case must be an object")
        name, url = raw.get("name"), raw.get("url")
        if not isinstance(name, str) or not name.strip() or not isinstance(url, str):
            raise SuiteError("Each case needs a name and URL")
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise SuiteError(f"{name}: URL must use HTTP(S)")
        if parsed.username or parsed.password:
            raise SuiteError(f"{name}: URL credentials are forbidden")
        method = raw.get("method", "GET")
        status = raw.get("expected_status", 200)
        timeout = raw.get("timeout_seconds", 5)
        expected = raw.get("json_contains", {})
        body = raw.get("json_body")
        if method not in ("GET", "POST"):
            raise SuiteError(f"{name}: only GET/POST are supported")
        if type(status) is not int or not 100 <= status <= 599:
            raise SuiteError(f"{name}: invalid status")
        if type(timeout) not in (int, float) or not 0.1 <= timeout <= 60:
            raise SuiteError(f"{name}: invalid timeout")
        if not isinstance(expected, dict) or not all(isinstance(k, str) and k for k in expected):
            raise SuiteError(f"{name}: json_contains needs string keys")
        if body is not None and (method != "POST" or not isinstance(body, dict)):
            raise SuiteError(f"{name}: json_body requires POST and object")
        cases.append(Case(name.strip(), url, method, status, expected, body, float(timeout)))
    if len({case.name for case in cases}) != len(cases):
        raise SuiteError("Case names must be unique")
    return cases


def _field(document: Any, path: str) -> Any:
    current = document
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            raise KeyError(path)
        current = current[key]
    return current


def run_case(case: Case, opener: Callable = urlopen) -> Result:
    headers = {"Accept": "application/json", "User-Agent": "python-automation-starter/1.0"}
    body = None
    if case.json_body is not None:
        body = json.dumps(case.json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(case.url, data=body, headers=headers, method=case.method)
    status: int | None = None
    response_body = b""
    try:
        with opener(request, timeout=case.timeout_seconds) as response:
            status = response.getcode()
            response_body = response.read(1_048_577)
    except HTTPError as exc:
        status = exc.code
        try:
            response_body = exc.read(1_048_577)
        finally:
            exc.close()
    except (URLError, TimeoutError, OSError) as exc:
        # Never include exception strings, URLs, headers, or response bodies in reports.
        return Result(case.name, False, status, [f"Transport failure: {type(exc).__name__}"])
    failures = []
    if status != case.expected_status:
        failures.append(f"Expected HTTP {case.expected_status}; received {status}")
    if len(response_body) > 1_048_576:
        failures.append("Response exceeds 1 MiB limit")
    elif case.json_contains:
        try:
            document = json.loads(response_body)
        except (UnicodeError, json.JSONDecodeError):
            failures.append("Response is not valid JSON")
        else:
            for path, expected in case.json_contains.items():
                try:
                    actual = _field(document, path)
                except KeyError:
                    failures.append(f"Missing JSON field: {path}")
                    continue
                if actual != expected:
                    failures.append(f"JSON field mismatch: {path}")
    return Result(case.name, not failures, status, failures)


def write_junit(path: str | Path, results: list[Result]) -> None:
    root = Element("testsuite", {
        "name": "api-regression",
        "tests": str(len(results)),
        "failures": str(sum(not result.passed for result in results)),
    })
    for result in results:
        testcase = SubElement(root, "testcase", {"name": result.name, "classname": "api"})
        if not result.passed:
            SubElement(testcase, "failure", {"message": "API check failed"}).text = "; ".join(result.failures)
    ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", default="examples/api_cases.json")
    parser.add_argument("--json-report")
    parser.add_argument("--junit-report")
    args = parser.parse_args(argv)
    try:
        cases = load_suite(args.suite)
        results = [run_case(case) for case in cases]
        report = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "passed": sum(result.passed for result in results),
            "total": len(results),
            "results": [asdict(result) for result in results],
        }
        if args.json_report:
            Path(args.json_report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if args.junit_report:
            write_junit(args.junit_report, results)
        for result in results:
            print(f"{'PASS' if result.passed else 'FAIL'} {result.name}")
        return 0 if all(result.passed for result in results) else 1
    except (SuiteError, OSError) as exc:
        print(f"Suite/report error: {type(exc).__name__}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
