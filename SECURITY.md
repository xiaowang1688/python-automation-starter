# Security Policy

This educational repository intentionally avoids committed API credentials.

- Never commit credentials, personal access tokens, passwords, or service account keys.
- Use `AUTOMATION_API_TOKEN` for optional bearer authentication over HTTPS.
- Do not add bearer credentials to the URL query string or JSON configuration.
- Share vulnerability reports privately with the repository owner rather than posting secrets in issues.
- For real deployments, pin CI action versions to reviewed commit SHAs and review dependency updates.

This project does not guarantee vulnerability-free operation or suitability for production.
