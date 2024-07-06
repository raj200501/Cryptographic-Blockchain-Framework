from web3 import Web3
import json

def interact_with_contract(contract_address, abi, private_key):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    from_address = w3.eth.account.privateKeyToAccount(private_key).address
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # Call a function (read-only)
    stored_data = contract.functions.get().call()
    print(f"Stored Data: {stored_data}")

    # Send a transaction (modifies state)
    nonce = w3.eth.get_transaction_count(from_address)
    transaction = contract.functions.set(123).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction Hash: {w3.toHex(tx_hash)}")

def main():
    contract_address = '0xYourContractAddress'
    with open('compiled_contract.json', 'r') as file:
        compiled_contract = json.load(file)
    abi = compiled_contract['contracts']['Contract.sol']['SimpleStorage']['abi']
    private_key = '0xYourPrivateKey'
    interact_with_contract(contract_address, abi, private_key)

if __name__ == "__main__":
    main()
