# CI/CD Pipeline Enhancement Design

## Goal
Update and stabilize the existing GitHub Actions CI pipeline (`.github/workflows/ci.yml`) to ensure formatting, linting, security scanning, and unit testing run reliably on every PR and push to `main`.

## Scope
Modify `.github/workflows/ci.yml` to:
1.  Run `ruff format --check` to enforce code formatting.
2.  Run `ruff check` to enforce linting rules.
3.  Run `bandit -r src/` for security vulnerability scanning.
4.  Run `pytest` with coverage reporting.

## Architecture

To prevent "command not found" errors in the GitHub Actions runner (which can happen when relying on pip-installed CLI tools not being on the `$PATH`), we will invoke all tools via the Python module runner: `python -m <tool>`.

### Workflow Steps Structure
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Set up Python 3.10 with pip caching
      - Install dependencies: pip install -e ".[dev]"
      - Run Formatting Check: python -m ruff format --check .
      - Run Linter: python -m ruff check .
      - Run Security Scan: python -m bandit -r src/
      - Run Tests: python -m pytest --cov=src/tuleap_mcp --cov-report=xml tests/
```

## Error Handling
Each step will fail the CI run if its respective tool returns a non-zero exit code, ensuring bad code, unformatted code, or failing tests cannot be merged.
