import json
import os
import random

from dotenv import load_dotenv
import requests
from time import sleep
from web3 import Web3, exceptions

def mix_main(from_account, key_to_account, coin, amount):

    # Проверка системы криптовалют

    system = "Etherium" if "eth" in coin else "Bitcoin" if "btc" in coin else "USDT"

    balance = 0

    # Проверка на изменение баланса, дальшейшего перевода

    while balance == 0:
        api_key = "BQXSS9VCJ9EDY95GIDHES5VM11UA7IZJUZ"
        try:
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={key_to_account}&tag=latest&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            balance = int(data['result'])
            sleep(2)
        except Exception:
            pass

    previos_wallet = ""
    array_indexes_is_used = []

    # Процесс перевода из кошелька в случайные кошельки

    for i in range(1, random.randint(3, 5)):
        load_dotenv()

        if i == 1:

            infura_url = "https://sepolia.infura.io/v3/9c86063c110e490fab51894fa23149da"
            with open("data/crypto_adresses.json", "r", encoding="UTF8") as file:
                keys_wallets = list(json.load(file)[f"{system}"].keys())
                private_key = json.load(file)["Etherium"][key_to_account]["secret_key"]

            from_account = from_account
            to_account = keys_wallets[random.randint(0, len(keys_wallets)-1)]

            web3 = Web3(Web3.HTTPProvider(infura_url))

            try:
                from_account = web3.to_checksum_address(from_account)
            except exceptions.InvalidAddress:
                print(f"Invalid 'from_account' address: {from_account}")

            try:
                to_account = web3.to_checksum_address(to_account)
            except exceptions.InvalidAddress:
                print(f"Invalid 'to_account' address: {to_account}")

            previos_wallet = to_account

        else:
            key_from_account = previos_wallet
            infura_url = "https://sepolia.infura.io/v3/9c86063c110e490fab51894fa23149da"

            with open("data/crypto_adresses.json", "r", encoding="UTF8") as file:
                keys_wallets = list(json.load(file)[f"{system}"].keys())
                private_key = json.load(file)["Etherium"][key_from_account]["secret_key"]

            from_account = key_from_account
            index_random = random.randint(0, len(keys_wallets) - 1)
            while index_random in array_indexes_is_used:
                index_random = random.randint(0, len(keys_wallets) - 1)

            to_account = keys_wallets[index_random]
            array_indexes_is_used.append(index_random)
            web3 = Web3(Web3.HTTPProvider(infura_url))

            try:
                from_account = web3.to_checksum_address(from_account)
            except exceptions.InvalidAddress:
                print(f"Invalid 'from_account' address: {from_account}")

            try:
                to_account = web3.to_checksum_address(to_account)
            except exceptions.InvalidAddress:
                print(f"Invalid 'to_account' address: {to_account}")

            previos_wallet = to_account

        nonce = web3.eth.get_transaction_count(from_account)
        tx = {
            "type": "0x2",
            "nonce": nonce,
            "from": from_account,
            "to": to_account,
            "value": web3.to_wei(amount, "ether" if coin == "eth" else "btc" if "btc" == coin else "usdt"),
            "maxFeePerGas": web3.to_wei("250", "gwei"),
            "maxPriorityFeePerGas": web3.to_wei("3", "gwei"),
            "chainId": 11155111
        }
        gas = web3.eth.estimate_gas(tx)
        tx["gas"] = gas
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Transaction hash: " + str(web3.to_hex(tx_hash)))

