# private_api.py

import requests
import hmac
import hashlib
import time
from colorama import Fore, Style


class PrivateAPI:
    BASE_URL = "https://api.crypto.com/exchange/v1"
    TIME_MULTIPLIER = 1000  # Used to convert time to milliseconds

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_signature(self, req: dict) -> str:
        """Generate the signature for the request."""
        payload = ""
        if "params" in req and req['params'] is not None:
            for key in sorted(req['params']):
                payload += key
                value = req['params'][key]
                if value is None:
                    payload += 'null'
                elif isinstance(value, list):
                    payload += ','.join(value)
                else:
                    payload += str(value)

        sig_payload = req['method'] + str(req['id']) + req['api_key'] + payload + str(req['nonce'])
        signature = hmac.new(
            bytes(self.api_secret, 'utf-8'),
            msg=bytes(sig_payload, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        return signature

    def prepare_request_data(self, method: str, params: dict) -> dict:
        """Prepare the request payload."""
        data = {
            "id": 1,
            "method": method,
            "api_key": self.api_key,
            "params": params,
            "nonce": int(round(time.time() * self.TIME_MULTIPLIER)),
        }
        data["sig"] = self.get_signature(data)
        return data

    def make_request(self, method: str, endpoint: str, params: dict = {}) -> dict:
        """Make a request to the API."""
        data = self.prepare_request_data(method, params)
        headers = {
            'api_key': data['api_key'],
            'sig': data['sig'],
            'timestamp': str(data['nonce'])
        }
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = requests.request(method, url, headers=headers, json=data)
        except requests.RequestException as e:
            print(f"{Fore.RED}Network Error: {e}{Style.RESET_ALL}")
            return None

        print(f"{Fore.YELLOW}Sending Request:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{method} {url}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Headers: {headers}{Style.RESET_ALL}")

        if response.ok:
            print(f"{Fore.GREEN}Received Response:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Status Code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Response Body: {response.json()}{Style.RESET_ALL}")
            return response.json()
        else:
            print(f"{Fore.RED}Received Error Response:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Status Code: {response.status_code}{Style.RESET_ALL}")
            return None
