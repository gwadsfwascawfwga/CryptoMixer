import requests
import json


def update_data_about_wallets(crypto_type):
    with open("data/crypto_adresses.json", "r", encoding="UTF-8") as file:
        crypto_adresses = json.load(file)
        print(crypto_adresses)
    with open("data/crypto_adresses.json", "w", encoding="UTF-8") as file:
        if crypto_type == "Etherium":
            for address in crypto_adresses[f"{crypto_type}"]:
                # Адрес кошелька пользователя

                api_key = "BQXSS9VCJ9EDY95GIDHES5VM11UA7IZJUZ"

                url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
                response = requests.get(url)
                data = response.json()
                balance = int(data['result']) # Umrechnen von Wei in Ether
                crypto_adresses[f"{crypto_type}"][address]["balance"] = balance
            json.dump(crypto_adresses, file)
        elif crypto_type == "Bitcoin":
            for address in crypto_adresses[f"{crypto_type}"]:
                header = {'Authorization': 'Bearer dsFtweYssMuXDETdeh6PRXeewVyi5HRzB4jzGLWKkD4', "Content-Type": "application/json"}
                balance = requests.get(f"https://www.blockonomics.co/api/balance?addr={address}", headers=header).json()["response"][0]["confirmed"]
                crypto_adresses[f"{crypto_type}"][address]["balance"] = balance
            json.dump(crypto_adresses, file)

