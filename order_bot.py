# order_bot.py


import requests

from private_api import PrivateAPI
from helpers import SymbolInfo
import uuid
from tickers import Tickers


class OrderBot:
    def __init__(self, api_key, api_secret, json_file_path):
        self.api = PrivateAPI(api_key, api_secret)
        self.symbol_info = SymbolInfo(json_file_path)
        self.tickers = Tickers()

    def open_order(self, instrument_name, side, order_type, qty):
        client_oid = str(uuid.uuid4())
        method = "private/create-order"
        params = {
            "instrument_name": instrument_name,
            "side": side,
            "type": order_type,
            "quantity": str(qty),
            "client_oid": str(client_oid),
        }
        print(params)
        request_data = self.api.prepare_request_data(method, params)
        print(request_data)
        base_url = self.api.BASE_URL

        try:
            response = requests.post(base_url + "/" + method, json=request_data)
            print(response.json())
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Network Error: {e}")
            return None

        if response.ok:
            data = response.json()
            if "code" in data and data["code"] == 0:
                print("Successfully opened position")
                return data
            else:
                print(f"Error: {data['code'] if 'code' in data else 'Unknown error'}")
                return None

        if not response.ok:
            print(f"Error: {response.status_code}, {response.reason}")

    def close_order(self, instrument_name, order_type):
        method = "private/close-position"
        params = {
            "instrument_name": instrument_name,
            "type": order_type,
        }
        print(params)
        request_data = self.api.prepare_request_data(method, params)
        print(request_data)
        base_url = self.api.BASE_URL

        try:
            response = requests.post(base_url + "/" + method, json=request_data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Network Error: {e}")
            return None

        if response.ok:
            data = response.json()
            if "code" in data and data["code"] == 0:
                print("Successfully closed position")
                return data
            else:
                print(f"Error: {data['code'] if 'code' in data else 'Unknown error'}")
                return None

        if not response.ok:
            print(f"Error: {response.status_code}, {response.reason}")
