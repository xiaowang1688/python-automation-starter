"""Offline tests: never depend on an external network."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from automation.healthcheck import (
    ConfigError,
    Endpoint,
    check_endpoint,
    load_config,
    parse_endpoint,
)


class FakeResponse:
    def __init__(self, status: int):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def getcode(self):
        return self.status


class ConfigTests(unittest.TestCase):
    def test_example_configuration(self):
        endpoints = load_config(Path("examples/endpoints.json"))
        self.assertEqual(len(endpoints), 1)
        self.assertEqual(endpoints[0].expected_status, 200)

    def test_missing_and_invalid_values(self):
        with self.assertRaises(ConfigError):
            parse_endpoint({"name": "bad", "url": "ftp://example.com"})
        with self.assertRaises(ConfigError):
            parse_endpoint({"name": "bad", "url": "https://user:pass@example.com"})
        with self.assertRaises(ConfigError):
            parse_endpoint({"name": "bad", "url": "https://example.com", "retries": -1})

    def test_duplicate_name_rejected(self):
        item = {"name": "duplicate", "url": "https://example.com"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"endpoints": [item, item]}), encoding="utf-8")
            with self.assertRaises(ConfigError):
                load_config(path)


class HealthCheckTests(unittest.TestCase):
    def test_success(self):
        endpoint = Endpoint("ready", "https://example.com", retries=0)
        result = check_endpoint(endpoint, opener=lambda request, timeout: FakeResponse(200))
        self.assertTrue(result.ok)
        self.assertEqual(result.attempts, 1)

    def test_retry_then_success(self):
        opener = Mock(side_effect=[TimeoutError(), FakeResponse(200)])
        sleeper = Mock()
        result = check_endpoint(Endpoint("retry", "https://example.com", retries=1),
                                opener=opener, sleeper=sleeper)
        self.assertTrue(result.ok)
        self.assertEqual(result.attempts, 2)
        sleeper.assert_called_once_with(1)

    def test_bad_status(self):
        result = check_endpoint(Endpoint("bad", "https://example.com", retries=0),
                                opener=lambda request, timeout: FakeResponse(503))
        self.assertFalse(result.ok)
        self.assertEqual(result.status, 503)

    def test_token_is_not_sent_without_explicit_opt_in(self):
        captured = []

        def opener(request, timeout):
            captured.append(request)
            return FakeResponse(200)

        result = check_endpoint(
            Endpoint("public", "https://example.com", retries=0),
            token="sample-token",
            opener=opener,
        )
        self.assertTrue(result.ok)
        self.assertIsNone(captured[0].get_header("Authorization"))

    def test_token_only_in_https_request_header(self):
        requests = []

        def opener(request, timeout):
            requests.append(request)
            return FakeResponse(200)

        result = check_endpoint(Endpoint("private", "https://example.com", retries=0, auth="bearer"),
                                token="sample-token", opener=opener)
        self.assertTrue(result.ok)
        self.assertEqual(requests[0].get_header("Authorization"), "Bearer sample-token")
        self.assertNotIn("sample-token", repr(result))
        with self.assertRaises(ConfigError):
            check_endpoint(Endpoint("insecure", "http://example.com", auth="bearer"), token="sample-token")


if __name__ == "__main__":
    unittest.main()
