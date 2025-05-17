import json

with open("data/crypto_adresses.json", "r", encoding="UTF8") as file:
    to_account_keys = list(json.load(file)[f"Etherium"].keys())
    print(to_account_keys)