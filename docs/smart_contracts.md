# Smart Contract Simulation

## Overview

ACBF provides a lightweight smart contract simulation in Python. Contracts are
stored in-memory and executed deterministically by the backend service. This is
ideal for demos, tests, and local learning without deploying on-chain.

## Included Contracts

### TokenContract

The token contract implements basic functionality:

- `mint(recipient, amount)`
- `transfer(recipient, amount)`
- `balance_of(address)`

### SimpleStorageContract

Simple key/value storage with:

- `set(key, value)`
- `get(key)`

## Deployment Flow

Contracts are deployed through `ContractRegistry.deploy`, which generates a
random address and stores the contract instance. Example:

```python
from acbf.contracts import ContractRegistry

registry = ContractRegistry()
contract = registry.deploy("token", symbol="ACBF", decimals=2)
```

## Calling Contracts

Contract calls are represented by `ContractCall`:

```python
from acbf.contracts import ContractCall

call = ContractCall(sender="alice", method="mint", args=["alice", 50])
registry.call(contract.address, call)
```

## API Endpoints

The backend exposes:

- `POST /contracts/deploy`
- `POST /contracts/call`
- `GET /contracts`

These endpoints map to the contract registry and return JSON payloads.

## Solidity Artifacts

Sample Solidity contracts are included under `smart_contracts/contracts/` for
reference. The `smart_contracts/compile.py` script simulates a compilation step
without requiring `solc`.
