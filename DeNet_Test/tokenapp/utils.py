# tokenapp/utils.py

import os
from web3 import Web3
from dotenv import load_dotenv
import requests

load_dotenv()

# Подключение к сети Polygon
POLYGON_RPC_URL = os.getenv('POLYGON_RPC_URL')
web3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

# Преобразование адреса контракта в формат checksum
TOKEN_ADDRESS = web3.to_checksum_address('0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0')

# ABI для ERC20 токена
TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Создание экземпляра контракта
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)


def get_token_name():
    return token_contract.functions.name().call()


def get_balance(address):
    address = web3.to_checksum_address(address)
    balance = token_contract.functions.balanceOf(address).call()
    decimals = token_contract.functions.decimals().call()
    return balance / (10 ** decimals)


def get_balances(addresses):
    balances = []
    for address in addresses:
        balances.append(get_balance(address))
    return balances


def get_token_info():
    name = token_contract.functions.name().call()
    symbol = token_contract.functions.symbol().call()
    total_supply = token_contract.functions.totalSupply().call()
    decimals = token_contract.functions.decimals().call()
    total_supply = total_supply / (10 ** decimals)
    return {'name': name, 'symbol': symbol, 'total_supply': total_supply}


def get_transaction_history(address, limit=10):
    API_KEY = os.getenv('POLYGONSCAN_API_KEY')
    url = f"https://api.polygonscan.com/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=desc&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        transactions = response.json().get('result', [])
        return transactions[:limit]
    else:
        return []


def get_top_addresses(limit=10):
    API_KEY = os.getenv('POLYGONSCAN_API_KEY')
    url = f"https://api.polygonscan.com/api?module=account&action=tokenholderlist&contractaddress={TOKEN_ADDRESS}&page=1&offset={limit}&sort=desc&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        holders = response.json().get('result', [])
        return [(holder['address'], int(holder['balance']) / (10 ** token_contract.functions.decimals().call())) for
                holder in holders]
    else:
        return []


def get_top_addresses_with_transactions(limit=10):
    holders = get_top_addresses(limit)
    top_addresses_with_transactions = []
    for address, balance in holders:
        transactions = get_transaction_history(address, limit=1)
        last_transaction_date = transactions[0]['timeStamp'] if transactions else None
        top_addresses_with_transactions.append((address, balance, last_transaction_date))
    return top_addresses_with_transactions
