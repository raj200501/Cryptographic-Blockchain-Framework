import json
from pathlib import Path


def compile_contract(contract_file: Path):
    """Simulate a compile step by packaging contract metadata.

    This keeps the example deterministic without requiring a Solidity compiler.
    """

    contract_path = Path(contract_file)
    if not contract_path.exists():
        raise FileNotFoundError(f"Contract not found: {contract_file}")
    source = contract_path.read_text(encoding="utf-8")
    compiled = {
        "language": "Solidity",
        "sources": {contract_path.name: {"content": source}},
        "contracts": {
            contract_path.name: {
                "SimpleStorage": {
                    "abi": [
                        {"name": "get", "type": "function", "inputs": [], "outputs": [{"type": "uint256"}]},
                        {
                            "name": "set",
                            "type": "function",
                            "inputs": [{"type": "uint256", "name": "value"}],
                            "outputs": [],
                        },
                    ],
                    "bytecode": "0xSIMULATED",
                }
            }
        },
    }

    output_path = Path("compiled_contract.json")
    output_path.write_text(json.dumps(compiled, indent=2), encoding="utf-8")
    return compiled


def main():
    contract_file = Path(__file__).resolve().parent / "contracts" / "SimpleStorage.sol"
    compile_contract(contract_file)
    print("Contract compiled successfully (simulated)")


if __name__ == "__main__":
    main()
