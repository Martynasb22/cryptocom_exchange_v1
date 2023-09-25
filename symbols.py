# symbols.py

import requests
import json


class CryptoComAPI:
    def __init__(self):
        self.base_url = "https://api.crypto.com/exchange/v1/public/get-instruments"
        self.perpetuals = []

    def fetch_instruments(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 0:
                instruments = data["result"]["data"]
                self.filter_perpetuals(instruments)
            else:
                print(f"Error: {data['code']}")
        else:
            print(f"HTTP Error: {response.status_code}")

    def filter_perpetuals(self, instruments):
        self.perpetuals = [inst for inst in instruments if inst["inst_type"] == "PERPETUAL_SWAP"]
        self.save_to_json()

    def save_to_json(self):
        with open("symbols.json", "w") as f:
            json.dump(self.perpetuals, f, indent=4)


if __name__ == "__main__":
    api = CryptoComAPI()
    api.fetch_instruments()
