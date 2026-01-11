# Testing & Verification

## Quick Verification

The canonical verification entrypoint is:

```sh
./scripts/verify.sh
```

This script installs `pytest` if needed, then runs unit and integration tests.
The integration tests start the local HTTP server on an ephemeral port and
validate that API endpoints behave as documented.

## Manual Setup

If you prefer to install test dependencies manually:

```sh
python -m pip install -r requirements.txt
```

## Pytest Layout

- `tests/unit` contains fast unit tests.
- `tests/integration` contains API integration tests.

## Adding Tests

When adding tests, prefer small deterministic fixtures. Avoid relying on
external services or network calls so CI remains stable.
