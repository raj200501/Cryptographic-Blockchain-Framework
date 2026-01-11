# API Reference

All endpoints return JSON and use UTF-8 encoding. The API is hosted by default
at `http://127.0.0.1:5000` when you run `./scripts/run.sh`.

## Health Check

**GET** `/health`

Response:

```json
{
  "status": "ok",
  "chain_id": "acbf-local"
}
```

## Create Wallet

**POST** `/wallet`

Response:

```json
{
  "address": "e3b0c44298fc1c14e3b0c44298fc1c14",
  "secret": "5f2c8e14d0c6401e" 
}
```

## Submit Transaction

**POST** `/transaction`

Request:

```json
{
  "sender": "alice",
  "recipient": "bob",
  "amount": 10,
  "metadata": {
    "note": "demo"
  }
}
```

Response:

```json
{
  "transaction": {
    "sender": "alice",
    "recipient": "bob",
    "amount": 10,
    "timestamp": 1690000000.123,
    "metadata": {
      "note": "demo"
    }
  },
  "pending_transactions": 1
}
```

## Mine Transactions

**POST** `/mine`

Request:

```json
{
  "miner_address": "miner-01"
}
```

Response:

```json
{
  "block_hash": "000abc...",
  "block_index": 1,
  "transactions": 2
}
```

## Balance

**GET** `/balance?address=<address>`

Response:

```json
{
  "address": "alice",
  "balance": 5
}
```

## Chain

**GET** `/chain`

Response:

```json
{
  "difficulty": 3,
  "mining_reward": 50,
  "length": 2,
  "pending_transactions": [],
  "chain": [
    {
      "index": 0,
      "timestamp": 1690000000.123,
      "transactions": [],
      "previous_hash": "0",
      "nonce": 0,
      "hash": "f9b1..."
    }
  ]
}
```

## Metrics

**GET** `/metrics`

Response:

```json
{
  "block_count": 2,
  "transaction_count": 4,
  "pending_transactions": 0,
  "unique_addresses": 3,
  "total_supply": 50,
  "mining_rewards": 50,
  "average_transactions_per_block": 2,
  "chain_valid": true
}
```

## Deploy Contract

**POST** `/contracts/deploy`

Request:

```json
{
  "contract_type": "token",
  "params": {
    "symbol": "ACBF",
    "decimals": 2
  }
}
```

Response:

```json
{
  "contract": {
    "address": "b3e1c9...",
    "type": "TokenContract",
    "symbol": "ACBF",
    "decimals": 2
  }
}
```

## Call Contract

**POST** `/contracts/call`

Request:

```json
{
  "address": "b3e1c9...",
  "sender": "alice",
  "method": "mint",
  "args": ["alice", 25]
}
```

Response:

```json
{
  "result": {
    "recipient": "alice",
    "amount": 25
  }
}
```

## List Contracts

**GET** `/contracts`

Response:

```json
{
  "b3e1c9...": {
    "address": "b3e1c9...",
    "type": "TokenContract",
    "symbol": "ACBF",
    "decimals": 2
  }
}
```
