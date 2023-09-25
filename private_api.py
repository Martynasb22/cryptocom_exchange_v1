# private_api.py

import requests
from signature import SignatureGenerator


class PrivateAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def make_request(self, method, endpoint):
        sig_gen = SignatureGenerator(self.api_key, self.api_secret)
        signature_data = sig_gen.generate_signature(method, endpoint)

        headers = {
            'api_key': signature_data['api_key'],
            'sig': signature_data['sig'],
            'timestamp': signature_data['timestamp']
        }

        url = f"https://api.crypto.com/exchange/v1{endpoint}"
        response = requests.request(method, url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP Error: {response.status_code}")
            return None
        