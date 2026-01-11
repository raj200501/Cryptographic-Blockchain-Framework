# CLI Guide

ACBF ships with a lightweight CLI to exercise the local blockchain without
starting the API server.

## Installation

```sh
python -m pip install -r requirements.txt
```

## Commands

### Create a Wallet

```sh
python -m acbf.cli wallet
```

### Submit a Transaction

```sh
python -m acbf.cli transfer <sender> <recipient> <amount>
```

### Mine Pending Transactions

```sh
python -m acbf.cli mine <miner_address>
```

### Inspect Chain

```sh
python -m acbf.cli chain
```

### Chain Metrics

```sh
python -m acbf.cli metrics
```

### Deploy Contracts

```sh
python -m acbf.cli deploy token --symbol ACBF --decimals 2
```

### Call Contracts

```sh
python -m acbf.cli call <address> <sender> balance_of <address>
```

### Crypto Demo

```sh
python -m acbf.cli crypto "hello"
```
