# DApp

## Backend

The backend is a standard-library HTTP server defined in `acbf.api` and exposed
via `dapp/backend/app.py`. It provides:

- Wallet creation
- Transaction submission
- Mining
- Chain inspection
- Metrics reporting
- Contract deployment and execution

### Key Endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Health check and chain ID |
| `/wallet` | POST | Create a new wallet |
| `/transaction` | POST | Submit a transaction |
| `/mine` | POST | Mine pending transactions |
| `/balance` | GET | Balance for a wallet |
| `/chain` | GET | Full chain dump |
| `/metrics` | GET | Chain metrics report |
| `/contracts/deploy` | POST | Deploy a simulated contract |
| `/contracts/call` | POST | Execute a contract method |
| `/contracts` | GET | List deployed contracts |

## Frontend

The React demo in `dapp/frontend` calls the backend API and provides a simple
wallet + mining workflow. It is optional and meant as a lightweight UI for
verifying the backend behavior.

### Environment Variable

Set `REACT_APP_BACKEND_URL` to point to the backend (defaults to
`http://127.0.0.1:5000`).

## Docker Compose

`deployment/docker/docker-compose.yaml` can run both services locally:

```sh
docker-compose up --build
```

The backend is available at `http://localhost:5000` and the frontend at
`http://localhost:3000`.
