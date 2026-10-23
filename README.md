# Python Automation Engineering | API, QA & Operations Projects

[![Python CI](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.12%20%7C%203.13-blue)](https://github.com/xiaowang1688/python-automation-starter/blob/main/.github/workflows/ci.yml)

**Maintained by [Xiaowang](https://github.com/xiaowang1688) · Python Automation / QA Automation · Open to international remote opportunities**

**For hiring reviewers:** [About me and selected projects](PORTFOLIO.md) · [Engineering case study](docs/ENGINEERING_CASE_STUDY.md) · [Actual source](automation/healthcheck.py) · [Offline tests](tests/test_healthcheck.py) · [CI evidence](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml)

**中文**：本项目展示 Python 自动化开发的可运行实践：批量 HTTP 接口检查、JSON 配置、超时与有限次重试、状态码验证、结构化结果、单元测试和 GitHub Actions CI。可从上面的代码与测试链接核验实现，不宣称未验证的线上业务成果。

A practical, dependency-free Python project demonstrating **API monitoring, reliable HTTP requests, automated testing, JSON reporting, and GitHub Actions CI**.

中文简介：面向 Python 自动化工程师 / 测试开发岗位的可运行作品示例。包含 HTTP 接口检查、超时与重试、自动化测试和 CI，适合作为继续扩展的基础，而不是声称已有生产部署经验。

## Features

- Monitor multiple HTTP endpoints configured in JSON.
- Validate expected HTTP status codes with timeouts and bounded retries.
- Export machine-readable JSON results for scheduled jobs and CI.
- Use optional bearer tokens **only for explicitly opted-in HTTPS endpoints** via `AUTOMATION_API_TOKEN`, never from committed configuration.
- Automated tests with Python's built-in `unittest`; no third-party runtime dependencies.

## Additional hands-on automation projects

The repository now includes four more practical Python projects, each with **real implementation code, offline unit tests, synthetic/public test fixtures, and an English case study**.

| Scenario | Engineering deliverable | Code & explanation |
| --- | --- | --- |
| API regression testing | Declarative GET/POST checks, status/JSON assertions, JSON and JUnit reports | [API Regression Runner](projects/api-regression/README.md) |
| Order/settlement reconciliation | Decimal-safe CSV comparisons and exception reports | [Data Reconciliation](projects/finance-reconciliation/README.md) |
| Service log observability | UTC-minute 5xx error rate, p95 latency and threshold alerts | [Log Anomaly Triage](projects/log-observability/README.md) |
| Browser UI automation | Real Playwright Chromium tests of a local order portal | [Playwright E2E](projects/browser-e2e/README.md) |

**Evidence:** Run the [Python CI workflow](.github/workflows/ci.yml) for offline tests on Python 3.10, 3.12 and 3.13. The [separate Playwright workflow](.github/workflows/browser-e2e.yml) runs real Chromium end-to-end browser tests. The sample data is synthetic; external APIs appear only in optional demos, never in the offline CI tests.

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/xiaowang1688/python-automation-starter.git
cd python-automation-starter
python -m automation.healthcheck --config examples/endpoints.json --output report.json
python -m unittest discover -s tests -v
```

For an authenticated HTTPS endpoint, add `"auth": "bearer"` to its endpoint configuration. The default is `"auth": "none"`, which never forwards your token. Redirects are disabled for authenticated requests to prevent credential forwarding. On Windows PowerShell, set the required token:

```powershell
$env:AUTOMATION_API_TOKEN = "your-token"
python -m automation.healthcheck --config examples/endpoints.json
Remove-Item Env:\AUTOMATION_API_TOKEN
```

The CLI returns exit code 0 when every endpoint passes, 1 when any check fails, and 2 for configuration errors. An HTTP endpoint's status is checked against `expected_status` (default: 200).

## Example configuration

```json
{
  "endpoints": [
    {
      "name": "example",
      "url": "https://example.com/",
      "expected_status": 200,
      "timeout_seconds": 5,
      "retries": 1
    }
  ]
}
```

## Repository structure

- `automation/healthcheck.py` — command-line monitor and structured results
- `examples/endpoints.json` — sample non-secret configuration
- `tests/test_healthcheck.py` — unit tests with HTTP mocks
- `.github/workflows/ci.yml` — CI checks on pushes and pull requests

## Security notes

Never commit API keys, passwords, access tokens, `.env` files, or generated reports. Set credentials in environment variables or GitHub Actions secrets. Bearer-token requests require HTTPS and an explicit `"auth": "bearer"` setting. Authenticated requests do not follow redirects. This project deliberately does not log credentials.

## Roadmap

Add concurrent checks, alert integrations, structured logging, and additional API regression test cases.

## License

This repository is a public learning/portfolio example; see `LICENSE` if one is added later. No claim of professional deployments or third-party affiliation is implied.
