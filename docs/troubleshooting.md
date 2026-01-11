# Troubleshooting

## Backend server fails to start

- Ensure you have Python 3.8+ installed.
- Check that port 5000 is available or set `ACBF_BACKEND_PORT`.
- If you want to bind externally (Docker/Kubernetes), set `ACBF_BACKEND_HOST=0.0.0.0`.

## Frontend cannot reach backend

- Confirm the backend is running on `http://127.0.0.1:5000`.
- Set `REACT_APP_BACKEND_URL` in `dapp/frontend/.env` if you use a different port.

## Tests fail locally

- Install test requirements:
  ```sh
  python -m pip install -r requirements.txt
  ```
- Run tests with more verbosity:
  ```sh
  python -m pytest -vv
  ```
