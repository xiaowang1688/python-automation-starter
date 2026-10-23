"""Synthetic HTTP event tests for log anomaly triage."""
import json
from pathlib import Path
import unittest
from automation.log_triage import LogError, analyze


def event(service, status, latency, timestamp="2026-01-01T10:15:00Z"):
    return json.dumps({
        "service": service, "timestamp": timestamp,
        "status": status, "latency_ms": latency,
    })


class LogTriageTests(unittest.TestCase):
    def test_demo_fixture_has_alert(self):
        report = analyze(Path("examples/http_logs.ndjson").read_text().splitlines())
        self.assertGreater(report["alert_count"], 0)

    def test_healthy_events(self):
        self.assertEqual(analyze([event("api", 200, 12) for _ in range(4)])["alert_count"], 0)

    def test_two_alert_types(self):
        report = analyze([event("api", 503, 1200) for _ in range(3)])
        self.assertEqual(report["groups"][0]["alerts"], ["high_5xx_rate", "high_p95_latency"])

    def test_minimum_volume(self):
        self.assertEqual(analyze([event("api", 503, 1200)], min_requests=3)["alert_count"], 0)

    def test_groups_by_service_and_minute(self):
        report = analyze([
            event("api", 200, 10, "2026-01-01T10:15:00Z"),
            event("payments", 200, 10, "2026-01-01T10:15:00Z"),
            event("api", 200, 10, "2026-01-01T10:16:00Z"),
        ])
        self.assertEqual(report["minutes"], 3)

    def test_rejects_invalid_records(self):
        with self.assertRaises(LogError):
            analyze([event("api", 200, -1)])
        with self.assertRaises(LogError):
            analyze([event("api", 200, 10, "2026-01-01T10:15:00")])
        with self.assertRaises(LogError):
            analyze(["not-json"])


if __name__ == "__main__":
    unittest.main()
