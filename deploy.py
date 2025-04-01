from solcx import compile_standard, install_solc
from web3 import Web3
import json

install_solc("0.8.0")

# Read the Solidity file
with open("Voting.sol", "r") as file:
    voting_file = file.read()

# Compile the Solidity file
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"Voting.sol": {"content": voting_file}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
},
solc_version="0.8.0"
)

# Save the compiled contract
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider("http://ganache:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# Get bytecode
bytecode = compiled_sol["contracts"]["Voting.sol"]["Voting"]["evm"]["bytecode"]["object"]

# Get ABI
abi = json.loads(compiled_sol["contracts"]["Voting.sol"]["Voting"]["metadata"])["output"]["abi"]

# Deploy the contract
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Voting.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print("Contract deployed at address:", contract_address)

# Save the contract address to a file
with open("contract_address.txt", "w") as file:
    file.write(contract_address)