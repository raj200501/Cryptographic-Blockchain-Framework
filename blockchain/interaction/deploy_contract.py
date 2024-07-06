from web3 import Web3
from solcx import compile_source

def compile_contract(contract_source_code):
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:SimpleStorage']
    return contract_interface

def deploy_contract(private_key, contract_interface):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    from_address = w3.eth.account.privateKeyToAccount(private_key).address
    SimpleStorage = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
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
    contract_source_code = '''
    pragma solidity ^0.8.0;

    contract SimpleStorage {
        uint256 storedData;

        function set(uint256 x) public {
            storedData = x;
        }

        function get() public view returns (uint256) {
            return storedData;
        }
    }
    '''
    private_key = '0xYourPrivateKey'
    contract_interface = compile_contract(contract_source_code)
    contract_address = deploy_contract(private_key, contract_interface)
    print(f"Contract deployed at address: {contract_address}")

if __name__ == "__main__":
    main()
