from web3 import Web3

def get_balance(address):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    balance = w3.eth.get_balance(address)
    return w3.fromWei(balance, 'ether')

def main():
    address = '0xYourEthereumAddress'
    balance = get_balance(address)
    print(f"Balance: {balance} ETH")

if __name__ == "__main__":
    main()
