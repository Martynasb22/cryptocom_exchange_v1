# balance.py

import requests

from private_api import PrivateAPI
from dotenv import load_dotenv
import os
from colorama import Fore, Style

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


class Balance:
    def __init__(self, api_key, api_secret):
        self.api = PrivateAPI(api_key, api_secret)
        self.user_balance = {}
        self.usd_balance = 0.0  # Jau pridėtas

    def fetch_balance(self):
        method = "private/user-balance"
        params = {}
        request_id = 12
        request_data = self.api.prepare_request_data(method, params)
        base_url = self.api.BASE_URL

        try:
            response = requests.post(base_url + "/" + method, json=request_data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            print(f"Network Error: {e}")
            return None

        if response.ok:
            data = response.json()
            if "code" in data and data["code"] == 0:
                print("Successfully fetched balance")
                self.user_balance = round(float(data["result"]["data"][0]["total_available_balance"]), 2)

                # Atnaujiname USD balansą
                for position in data["result"]["data"][0]["position_balances"]:
                    if position["instrument_name"] == "USD":
                        self.usd_balance = round(float(position["quantity"]), 2)

                return data
            else:
                print(f"Error: {data['code'] if 'code' in data else 'Unknown error'}")
                return None
        else:
            print(f"Received Error Response: Status Code {response.status_code}")
            return None


if __name__ == "__main__":
    API_KEY = api_key
    API_SECRET = api_secret

    balance = Balance(API_KEY, API_SECRET)
    balance.fetch_balance()

    print(Fore.BLUE + "Available Balance:".ljust(25) + Style.RESET_ALL, Fore.RED + str(balance.user_balance).rjust(25)
          + Style.RESET_ALL)
    print(Fore.BLUE + "USD Balance:".ljust(25) + Style.RESET_ALL, Fore.RED + str(balance.usd_balance).rjust(25)
          + Style.RESET_ALL)
