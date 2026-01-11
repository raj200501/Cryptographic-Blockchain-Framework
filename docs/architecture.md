# ACBF Architecture

## Overview

ACBF is an educational, local-first blockchain framework. It provides:

- A deterministic blockchain simulation implemented in Python.
- A small cryptography toolkit implemented in pure Python.
- A standard-library HTTP API used by both the CLI and the optional React frontend.
- A contract registry that simulates smart contracts without external chains.

The framework is designed to run without Internet access or external chain
providers, which keeps the developer experience deterministic.

## High-level Components

### Configuration

Configuration is loaded from `config/blockchain_config.yaml` and
`config/dapp_config.yaml` by `acbf.config.load_config`. Values can be overridden
by environment variables (see `.env.example`).

### Blockchain Core

The blockchain simulation lives in `acbf.blockchain.core` and exposes:

- `Transaction` objects with sender/recipient/amount metadata.
- `Block` objects containing a list of transactions and proof-of-work hash.
- `Blockchain` class that stores the chain, pending transactions, and mining
  logic.

The chain uses a simple proof-of-work algorithm (hash prefix matching) that is
fast enough for demos but still validates block integrity.

### Contract Simulation

The contract subsystem (`acbf.contracts`) simulates deployment and execution
without an external EVM. Contracts are stored in-memory in
`ContractRegistry` and invoked through structured `ContractCall` objects.

Two contracts are included:

- `TokenContract` (mint/transfer/balance_of)
- `SimpleStorageContract` (set/get)

### Backend API

`acbf.api` exposes a standard-library HTTP server (built on
`http.server.ThreadingHTTPServer`). It injects the `BlockchainService` and
exposes endpoints for wallet creation, transactions, mining, chain inspection,
metrics, and contract execution.

### CLI

`acbf.cli` provides a convenient way to exercise the same APIs locally.
It shares the same configuration and service layer as the API.

### Frontend (Optional)

The React demo lives in `dapp/frontend`. It calls the API endpoints and
verifies that the local chain responds as expected.

## Data Flow

1. A request hits the HTTP API.
2. API validates input and delegates to `BlockchainService`.
3. Service mutates blockchain state, mines blocks, or calls contracts.
4. API returns structured JSON responses.

## Deployment Artifacts

- `deployment/docker/Dockerfile` builds the backend container.
- `deployment/docker/docker-compose.yaml` runs backend + frontend locally.
- `deployment/kubernetes/*` contains example manifests for Kubernetes.
- `.github/workflows/ci.yml` runs `./scripts/verify.sh` in CI.
