from solcx import compile_standard, install_solc
from web3 import Web3
import json

install_solc("0.8.0")

# read the solididty file
with open("Voting.sol", "r") as file:
    voting_file = file.read

# compile the solidity file
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources" : {"Voting.sol": {"content": voting_file}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    },
},
solc_version="0.8.0"
)

# save the compiled contract
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# connect to local ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# get bytecode
bytecode = compiled_sol["contracts"]["Voting.sol"]["Voting"]["evm"]["bytecode"]["object"]

# Get ABI
abi = json.loads(compiled_sol["contracts"]["Voting.sol"]["Voting"]["metadata"])["output"]["abi"]

# deploy the contract
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Voting.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("contract deployed at address:", tx_receipt.contractAddress)