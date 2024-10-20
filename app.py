
from flask import Flask, request, jsonify, render_template
from web3 import Web3

import json



app = Flask(__name__)

# Connect to Alchemy Sepolia endpoint
web3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/_UNLzKrWzgQXg7fCXaZLj5OroEcqKCn3' ))
web3.eth.default_account = '0x81e8ae30bAa3872c65b1726952B9931581456f44'

if web3.is_connected():
    print("Connected to Sepolia")
else:
    print("Failed to connect to Sepolia")
    
abi=[
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "_temperature",
				"type": "int256"
			},
			{
				"internalType": "int256",
				"name": "_humidity",
				"type": "int256"
			}
		],
		"name": "logData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "dataLog",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "int256",
				"name": "temperature",
				"type": "int256"
			},
			{
				"internalType": "int256",
				"name": "humidity",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getData",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			},
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getDataLength",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract_address = '0x557A2cBbA09911F28FBed7713F68eAE672443945'
contract = web3.eth.contract(address=contract_address, abi=abi)

PRIVATE_KEY = 'private key'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/log_data', methods=['POST'])
def log_data():
    try:
        
        temperature = int(request.form['temperature'])
        humidity = int(request.form['humidity'])

        # Build the transaction
        txn = contract.functions.logData(temperature, humidity).build_transaction({
            'from': web3.eth.default_account,
            'gas': 200000,
            'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
        })

        # Sign the transaction with the private key
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
		
        # Send the signed transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return f'Transaction successful with hash: {tx_hash.hex()}', 200
    except Exception as e:
        return f'Error: {str(e)}', 500
@app.route('/get_data_length', methods=['GET'])
def get_data_length():
    try:
        length = contract.functions.getDataLength().call()
        return jsonify({'data_length': length}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f'Error: {str(e)}', 500
@app.route('/get_data/<int:index>', methods=['GET'])
def get_data(index):
    try:
        data = contract.functions.getData(index).call()
        return jsonify({
            'timestamp': data[0],
            'temperature': data[1],
            'humidity': data[2]
        }), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
