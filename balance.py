from private_api import PrivateAPI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


class Balance:
    def __init__(self, api_key, api_secret):
        self.api = PrivateAPI(api_key, api_secret)
        self.user_balance = {}
        self.usd_balance = 0.0

    def fetch_balance(self):
        data = self.api.make_request("GET", "/v1/private/user-balance")

        if data and data["code"] == 0:
            self.user_balance = data["result"]["accounts"]
            for account in self.user_balance:
                if account["currency"] == "USD":
                    self.usd_balance = float(account["balance"])
        else:
            print(f"Error: {data['code'] if data else 'Unknown error'}")


if __name__ == "__main__":
    API_KEY = api_key
    API_SECRET = api_secret

    balance = Balance(API_KEY, API_SECRET)
    balance.fetch_balance()

    print("User Balance:", balance.user_balance)
    print("USD Balance:", balance.usd_balance)