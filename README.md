# Python Automation Starter

A practical, dependency-free Python project demonstrating **API monitoring, reliable HTTP requests, automated testing, JSON reporting, and GitHub Actions CI**.

中文简介：面向 Python 自动化工程师 / 测试开发岗位的可运行作品示例。包含 HTTP 接口检查、超时与重试、自动化测试和 CI，适合作为继续扩展的基础，而不是声称已有生产部署经验。

## Features

- Monitor multiple HTTP endpoints configured in JSON.
- Validate expected HTTP status codes with timeouts and bounded retries.
- Export machine-readable JSON results for scheduled jobs and CI.
- Use an optional bearer token from the `AUTOMATION_API_TOKEN` environment variable, never from committed configuration.
- Automated tests with Python's built-in `unittest`; no third-party runtime dependencies.

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/xiaowang1688/python-automation-starter.git
cd python-automation-starter
python -m automation.healthcheck --config examples/endpoints.json --output report.json
python -m unittest discover -s tests -v
```

On Windows PowerShell, set an optional token only if your endpoint requires it:

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

Never commit API keys, passwords, access tokens, `.env` files, or generated reports. Set credentials in environment variables or GitHub Actions secrets. Prefer HTTPS endpoints for bearer-token authentication. This project deliberately does not log credentials.

## Roadmap

Add concurrent checks, alert integrations, structured logging, and additional API regression test cases.

## License

This repository is a public learning/portfolio example; see `LICENSE` if one is added later. No claim of professional deployments or third-party affiliation is implied.
