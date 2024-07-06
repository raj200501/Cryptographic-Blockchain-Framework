from solcx import compile_standard
import json

def compile_contract(contract_file):
    with open(contract_file, 'r') as file:
        contract_source_code = file.read()
    
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "Contract.sol": {
                "content": contract_source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    })
    
    with open('compiled_contract.json', 'w') as file:
        json.dump(compiled_sol, file)
    
    return compiled_sol

def main():
    contract_file = 'contracts/SimpleStorage.sol'
    compile_contract(contract_file)
    print("Contract compiled successfully")

if __name__ == "__main__":
    main()
