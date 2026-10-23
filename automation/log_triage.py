"""Aggregate HTTP logs into UTC minute windows; flag 5xx and p95 spikes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys
from typing import Iterable


class LogError(ValueError):
    """Input log cannot be analyzed reliably."""


def analyze(
    lines: Iterable[str],
    *,
    error_rate_threshold: float = 0.2,
    p95_threshold_ms: float = 800,
    min_requests: int = 3,
) -> dict:
    if (not math.isfinite(error_rate_threshold) or
            not math.isfinite(p95_threshold_ms) or
            not 0 <= error_rate_threshold <= 1 or
            not p95_threshold_ms > 0 or min_requests < 1):
        raise LogError("Invalid alert thresholds")
    grouped: dict[tuple[str, str], dict] = {}
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            raise LogError(f"Line {number}: invalid JSON") from None
        if not isinstance(event, dict):
            raise LogError(f"Line {number}: expected object")
        service, stamp = event.get("service"), event.get("timestamp")
        status, latency = event.get("status"), event.get("latency_ms")
        if not isinstance(service, str) or not service.strip() or not isinstance(stamp, str):
            raise LogError(f"Line {number}: missing service/timestamp")
        if type(status) is not int or not 100 <= status <= 599:
            raise LogError(f"Line {number}: status outside HTTP range")
        if type(latency) not in (int, float) or not math.isfinite(latency) or latency < 0:
            raise LogError(f"Line {number}: invalid latency")
        try:
            timestamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            raise LogError(f"Line {number}: invalid timestamp") from None
        if timestamp.tzinfo is None:
            raise LogError(f"Line {number}: timestamp needs timezone")
        minute = timestamp.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        bucket = grouped.setdefault((service.strip(), minute), {"latencies": [], "errors_5xx": 0})
        bucket["latencies"].append(float(latency))
        bucket["errors_5xx"] += int(status >= 500)
    rows = []
    for (service, minute), bucket in sorted(grouped.items()):
        values = sorted(bucket["latencies"])
        count = len(values)
        rate = bucket["errors_5xx"] / count
        p95 = values[math.ceil(count * .95) - 1]
        alerts = []
        if count >= min_requests and rate >= error_rate_threshold:
            alerts.append("high_5xx_rate")
        if count >= min_requests and p95 >= p95_threshold_ms:
            alerts.append("high_p95_latency")
        rows.append({
            "service": service,
            "minute_utc": minute,
            "requests": count,
            "errors_5xx": bucket["errors_5xx"],
            "error_rate": round(rate, 4),
            "p95_latency_ms": round(p95, 2),
            "alerts": alerts,
        })
    return {"minutes": len(rows), "alert_count": sum(bool(r["alerts"]) for r in rows), "groups": rows}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="examples/http_logs.ndjson")
    parser.add_argument("--output")
    parser.add_argument("--error-rate-threshold", type=float, default=0.2)
    parser.add_argument("--p95-threshold-ms", type=float, default=800)
    parser.add_argument("--min-requests", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        with Path(args.input).open(encoding="utf-8") as stream:
            report = analyze(
                stream,
                error_rate_threshold=args.error_rate_threshold,
                p95_threshold_ms=args.p95_threshold_ms,
                min_requests=args.min_requests,
            )
        content = json.dumps(report, indent=2) + "\n"
        if args.output:
            Path(args.output).write_text(content, encoding="utf-8")
        print(content, end="")
        return 1 if report["alert_count"] else 0
    except (LogError, OSError, UnicodeError) as exc:
        print(f"Input/report error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
