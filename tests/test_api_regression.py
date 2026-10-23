"""Offline tests: no public API required."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from automation.api_regression import Case, SuiteError, load_suite, run_case, write_junit


class FakeResponse:
    def __init__(self, status=200, data=b"{}"):
        self.status, self.data = status, data

    def getcode(self):
        return self.status

    def read(self, size):
        return self.data[:size]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class APITests(unittest.TestCase):
    def test_example_suite_valid(self):
        self.assertEqual(len(load_suite("examples/api_cases.json")), 2)

    def test_nested_json_success(self):
        opener = Mock(return_value=FakeResponse(data=b'{"data":{"ready":true}}'))
        result = run_case(Case("ok", "https://example.com", json_contains={"data.ready": True}), opener)
        self.assertTrue(result.passed)
        opener.assert_called_once()

    def test_status_and_json_mismatch(self):
        result = run_case(
            Case("bad", "https://example.com", json_contains={"ok": True}),
            lambda request, timeout: FakeResponse(503, b'{"ok":false}'),
        )
        self.assertFalse(result.passed)
        self.assertEqual(len(result.failures), 2)

    def test_post_payload(self):
        captured = []
        def opener(request, timeout):
            captured.append(request)
            return FakeResponse(201, b'{"id":42}')
        case = Case("post", "https://example.com", "POST", 201, {"id": 42}, {"name": "example"})
        self.assertTrue(run_case(case, opener).passed)
        self.assertEqual(json.loads(captured[0].data), {"name": "example"})
        self.assertEqual(captured[0].get_method(), "POST")

    def test_reject_embedded_credentials(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "suite.json"
            path.write_text(json.dumps({"cases": [{"name": "bad", "url": "https://a:b@example.com"}]}))
            with self.assertRaises(SuiteError):
                load_suite(path)

    def test_junit_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "results.xml"
            write_junit(path, [run_case(Case("bad", "https://example.com"),
                                        lambda request, timeout: FakeResponse(503))])
            self.assertIn('failures="1"', path.read_text())


if __name__ == "__main__":
    unittest.main()
