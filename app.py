from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
import json
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
import logging
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to use Flask flash messages

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Connect to Ganache
ganache_url = os.getenv("GANACHE_URL", "http://localhost:8545")
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Read contract address from file
with open("contract_address.txt", "r") as file:
    contract_address = file.read().strip()

with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)
abi = json.loads(compiled_sol["contracts"]["Voting.sol"]["Voting"]["metadata"])["output"]["abi"]

contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route('/')
def index():
    candidates = []
    try:
        for i in range(1, contract.functions.candidatesCount().call() + 1):
            candidate = contract.functions.candidates(i).call()
            candidates.append({'id': candidate[0], 'name': candidate[1], 'voteCount': candidate[2]})
    except BadFunctionCallOutput as e:
        logging.error(f"BadFunctionCallOutput: {e}")
        flash("Could not fetch candidates. Is the contract deployed correctly?", 'danger')
    return render_template('index.html', candidates=candidates)

@app.route('/vote', methods=['POST'])
def vote():
    candidate_id = request.form['candidate']
    logging.debug(f"Received vote request for candidate_id: {candidate_id}")
    account = w3.eth.accounts[0]  # Use the first account for simplicity
    logging.debug(f"Using account: {account}")
    try:
        tx_hash = contract.functions.vote(int(candidate_id)).transact({'from': account})
        logging.debug(f"Transaction hash: {tx_hash}")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        flash("Vote cast successfully.", 'success')
    except ContractLogicError as e:
        logging.error(f"ContractLogicError: {e}")
        if "You have already voted" in str(e):
            flash("You have already voted. Each address can only vote once.", 'warning')
        else:
            flash("An error occurred while processing your vote.", 'danger')
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        flash(f"An unexpected error occurred: {e}", 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)