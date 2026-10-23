# Xiaowang | Python Automation & QA Engineering

**Python Automation · API Testing · CI/CD · Reliability Checks · Security Automation**

Based in Mainland China (UTC+8) · Interested in international remote Python automation, QA automation, and scripting projects

[![Python Automation CI](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml)
[![Security Scanner CI](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner/actions/workflows/ci.yml)

**[LinkedIn](https://www.linkedin.com/in/%E6%B6%9B-%E5%BC%A0-30116924a/)** · **[English Technical Resume / 英文技术简历](RESUME.md)** · [Live CI evidence](https://github.com/xiaowang1688/python-automation-starter/actions)

## About me / 关于我

I focus on **practical Python automation**: repeatable API checks, testable scripts, CI workflows, and small security tools. My GitHub projects include real source code, runnable instructions, offline regression tests, and GitHub Actions results—so reviewers can verify the implementation rather than relying on skill claims alone.

我专注于 **Python 自动化开发与测试开发**：通过可配置的 API 检查、异常与超时处理、自动化单元测试、GitHub Actions，以及安全扫描工具，将重复操作变为可复现、可检查的工程流程。仓库中的代码、使用说明、测试和 CI 记录可以直接核验。

I am looking for remote opportunities involving **Python automation, QA / test development, API validation, CI pipeline maintenance, and script-driven workflows**.

我希望承接或应聘 Python 自动化、接口测试、测试开发和脚本工具相关的远程工作。日常沟通以中文为主，可借助翻译工具进行英文书面协作；偏好需求清晰、文档齐全的异步远程工作。

## Selected projects / 重点作品

### 1) [Python Automation Starter](https://github.com/xiaowang1688/python-automation-starter) — API monitoring and CI

**Situation:** Repeatable endpoint checks should not depend on ad-hoc manual browser checks.

**Implementation:** A JSON-configured Python CLI checks multiple HTTP endpoints, validates status codes, applies bounded retries and timeouts, produces JSON reports, and returns explicit exit codes for CI or scheduled execution. Optional bearer credentials must be explicitly enabled per HTTPS endpoint; authenticated requests do not follow redirects.

**Verification:** Offline `unittest` cases cover success, unexpected statuses, retry behavior, invalid configuration, and credential opt-in. GitHub Actions runs the tests on Python 3.10, 3.12, and 3.13.

- [Source code](https://github.com/xiaowang1688/python-automation-starter/blob/main/automation/healthcheck.py)
- [Automated tests](https://github.com/xiaowang1688/python-automation-starter/blob/main/tests/test_healthcheck.py)
- [GitHub Actions](https://github.com/xiaowang1688/python-automation-starter/actions/workflows/ci.yml)
- [Engineering case study](https://github.com/xiaowang1688/python-automation-starter/blob/main/docs/ENGINEERING_CASE_STUDY.md)

### 2) [Smart Contract Vulnerability Scanner](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner) — Python security tooling

**Situation:** Manually invoking external analysis commands is error-prone.

**Implementation:** A Python CLI enumerates Solidity files and wraps Mythril analysis with configurable timeouts, explicit subprocess arguments (no shell), captured output, and exit statuses.

**Verification:** CI uses mocked CLI execution to check Python orchestration. Actual Mythril analysis requires installation of Mythril and Solidity dependencies; **a passing CI run is not an audited smart contract**.

- [Scanner implementation](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner/blob/main/contracts/scan_vulnerabilities.py)
- [Offline tests](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner/blob/main/tests/test_scanner.py)
- [GitHub Actions](https://github.com/xiaowang1688/smart-contract-vulnerability-scanner/actions/workflows/ci.yml)

### 3) [GDP Dashboard](https://github.com/xiaowang1688/gdp-dashboard) — additional Python / data visualization example

A Streamlit/Pandas GDP dashboard example for loading CSV data, filtering dates/countries, and charting results. This is a **dashboard template/example**, not evidence of an original production platform.

## More verifiable practice projects / 新增实践案例

| Portfolio project | Engineering scenario | Evidence |
| --- | --- | --- |
| [API Regression Runner](projects/api-regression/README.md) | Automate release/API smoke checks | Python HTTP runner, JSON assertions, JUnit XML, offline tests |
| [Order / Settlement Reconciliation](projects/finance-reconciliation/README.md) | Audit order-to-payment mismatches | CSV input validation, Decimal comparison, JSON discrepancy report |
| [HTTP Log Anomaly Triage](projects/log-observability/README.md) | Diagnose 5xx bursts and latency spikes | p95 latency by minute, error-rate thresholds, test fixtures |
| [Playwright Chromium Browser E2E](projects/browser-e2e/README.md) | Regression-test form validation and order confirmation | Real Chromium UI interactions, offline HTML fixture, browser CI, screenshot artifacts |

These examples use controlled synthetic browser/business fixtures or optional public demo endpoints. They show source code and tests; they are **not claims of paid client delivery**.

## International collaboration / 国际远程协作

I am interested in international teams that value testable Python scripts, reproducible issues, written requirements, pull request reviews, and asynchronous delivery. I am based in Mainland China (UTC+8). I use Chinese for primary communication and can work with English written technical material **with translation assistance**. I do not claim fluent spoken English.

工作方式：异步文字沟通、GitHub Issues/PR、可复现的问题描述、自动化测试结果、英文优先文档。没有公开验证的雇主、工作年限、生产客户或商业交付记录，不会在此虚构。

[Remote collaboration notes](docs/INTERNATIONAL_REMOTE.md) · [Live GitHub profile README](https://github.com/xiaowang1688/xiaowang1688#readme)

## What you can verify / 可核验的技能

| Area | Evidence |
| --- | --- |
| Python scripting | Runnable CLI scripts in the two highlighted projects |
| API checking | HTTP status validation, bounded retries and timeouts |
| Automated testing | `unittest` with deterministic HTTP / subprocess mocks |
| CI/CD | GitHub Actions matrix tests across Python 3.10 / 3.12 / 3.13 |
| Security-minded scripting | HTTPS-only opt-in bearer tokens, explicit subprocess parameters, no secrets in examples |
| Documentation | Readable English/Chinese summaries, setup steps and limitations |

**Approach:** Small reproducible examples, explicit error handling, observable outputs, version-controlled changes, and tests before claiming functionality.

## Collaboration / 合作

- **Role interests:** Python Automation Engineer · QA Automation / Test Development · API Testing · Scripting
- **Location:** Mainland China · Remote-first opportunities
- **Communication:** Chinese-first; translation-assisted English writing and asynchronous documentation
- **Contact:** [LinkedIn profile](https://www.linkedin.com/in/%E6%B6%9B-%E5%BC%A0-30116924a/) · Public GitHub issues for non-sensitive technical discussion only

> These repositories demonstrate **hands-on project implementations and CI evidence**, not an unverified number of years in a production role, employer names, or client outcomes.
