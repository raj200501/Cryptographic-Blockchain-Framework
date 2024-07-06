from web3 import Web3
import json

def deploy_contract(private_key, compiled_contract):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    from_address = w3.eth.account.privateKeyToAccount(private_key).address
    bytecode = compiled_contract['contracts']['Contract.sol']['SimpleStorage']['evm']['bytecode']['object']
    abi = compiled_contract['contracts']['Contract.sol']['SimpleStorage']['abi']
    
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(from_address)
    transaction = SimpleStorage.constructor().buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

def main():
    with open('compiled_contract.json', 'r') as file:
        compiled_contract = json.load(file)
    
    private_key = '0xYourPrivateKey'
    contract_address = deploy_contract(private_key, compiled_contract)
    print(f"Contract deployed at address: {contract_address}")

if __name__ == "__main__":
    main()
