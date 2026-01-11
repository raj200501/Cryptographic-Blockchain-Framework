# 🚀 Advanced Cryptographic Blockchain Framework (ACBF)

ACBF is a local-first, educational blockchain framework that bundles:

- A deterministic blockchain simulation with proof-of-work mining.
- Pure-Python AES/RSA/SHA-256 helpers for learning purposes.
- A lightweight HTTP backend API with wallet, transaction, mining, and contract endpoints.
- A React demo DApp (optional).
- CI-ready verification scripts and documentation.

> **Note:** This project is intentionally self-contained and does not connect to
> public chains. All blockchain interactions are simulated locally to keep the
> developer experience reproducible.

## 🌟 Features

- **Cryptography Toolkit**: AES-128 CBC, RSA (toy implementation), and SHA-256 utilities.
- **Blockchain Simulation**: Mine blocks, submit transactions, and inspect chain state.
- **Metrics Reporting**: Chain metrics via CLI or API.
- **Smart Contract Simulation**: Deploy and call in-memory token + storage contracts.
- **Backend API**: Standard-library HTTP service exposing JSON endpoints.
- **CLI**: Run blockchain + crypto workflows from the command line.
- **Optional DApp**: React frontend that exercises the backend API.
- **CI/CD Ready**: Deterministic verification script and GitHub Actions workflow.

## 🔧 Prerequisites

- Python 3.8+
- Node.js 16+ (only required for the optional frontend)
- Docker (optional for containerized runs)

## ✅ Verified Quickstart (commands executed)

```sh
python -m acbf.cli crypto "hello ACBF"
```

## 📦 Installation

ACBF has no runtime dependencies outside the Python standard library. To run
verification tests, install the test requirements:

```sh
python -m pip install -r requirements.txt
```

## ▶️ Running the Backend API

```sh
./scripts/run.sh
```

The API starts on `http://127.0.0.1:5000` by default. Example requests:

```sh
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/wallet
curl -X POST http://127.0.0.1:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"alice","recipient":"bob","amount":10}'
curl http://127.0.0.1:5000/metrics
```

## 🧰 CLI Usage

```sh
python -m acbf.cli wallet
python -m acbf.cli transfer alice bob 5
python -m acbf.cli mine miner-1
python -m acbf.cli metrics
python -m acbf.cli chain
```

## 🧪 Verification (CI Entry Point)

```sh
./scripts/verify.sh
```

The script installs `pytest` if needed, runs unit tests, and executes API
integration checks. GitHub Actions runs the same command on `push` and
`pull_request`.

## 🔗 Smart Contracts

Contracts are simulated locally (no EVM). You can deploy and call contracts via
API or CLI. Solidity samples are included under `smart_contracts/contracts/`.
The `smart_contracts/compile.py` script simulates compilation without requiring
`solc`.

## 🖥️ Optional React DApp

```sh
cd dapp/frontend
npm install
npm start
```

The UI expects the backend at `http://127.0.0.1:5000`. Override with
`REACT_APP_BACKEND_URL` if needed.

## 🐳 Docker

```sh
docker-compose -f deployment/docker/docker-compose.yaml up --build
```

## ☸️ Kubernetes

```sh
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
```

## 📚 Documentation

- [Architecture](docs/architecture.md)
- [Cryptography](docs/cryptography.md)
- [Blockchain Simulation](docs/blockchain.md)
- [Smart Contracts](docs/smart_contracts.md)
- [DApp](docs/dapp.md)
- [CLI Guide](docs/cli.md)
- [API Reference](docs/api.md)
- [Testing](docs/testing.md)
- [Troubleshooting](docs/troubleshooting.md)

## 📦 Examples

```sh
python examples/demo_workflow.py
python examples/metrics_report.py
```

## ✅ Verified Verification (commands executed)

```sh
./scripts/verify.sh
```

---

Made with ❤️ by the ACBF Team.
