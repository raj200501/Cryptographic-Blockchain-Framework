from web3 import Web3

def send_transaction(private_key, to_address, amount):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    from_address = w3.eth.account.privateKeyToAccount(private_key).address
    nonce = w3.eth.get_transaction_count(from_address)
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.toHex(tx_hash)

def main():
    private_key = '0xYourPrivateKey'
    to_address = '0xRecipientAddress'
    amount = 0.1
    tx_hash = send_transaction(private_key, to_address, amount)
    print(f"Transaction Hash: {tx_hash}")

if __name__ == "__main__":
    main()
