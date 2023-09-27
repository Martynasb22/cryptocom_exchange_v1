# expired_settlement.py

import requests
from colorama import Fore, Style
from pprint import pprint


class ExpiredSettlement:
    def __init__(self):
        self.base_url = "https://api.crypto.com/exchange/v1"
        self.instrument_name = None
        self.expired_timestamp = None
        self.expired_price = None
        self.expired_size = None

    def get_get_setlement_by_symbol(self, base_url, symbol):
        url = f"{base_url}/public/get-expired-settlement-price?instrument_type=FUTURE&page=1"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            if data["code"] == 0:
                # self.instrument_name = data["result"]["i"]
                # self.expired_timestamp = data["result"]["x"]
                # self.expired_price = data["result"]["v"]
                # self.expired_size = data["result"]["t"]
                return self
            else:
                print(f"Error: {data['code']}")
        else:
            print(f"{Fore.RED}Error: {response.status_code}{Style.RESET_ALL}")
            print("Response:", response.text)
            print("Endpoint:", url)

    def print_expired_settlement_data(self):
        print(f"Instrument Name: {self.instrument_name}")
        print(f"Expired Timestamp: {self.expired_timestamp}")
        print(f"Expired Price: {self.expired_price}")
        print(f"Expired Size: {self.expired_size}")
        return None


if __name__ == "__main__":
    expired_settlement = ExpiredSettlement()
    expired_settlement.get_get_setlement_by_symbol(expired_settlement.base_url, "BTC-USD")
    expired_settlement.print_expired_settlement_data()
    print("Done")
    print("----------------------------------------------------")
