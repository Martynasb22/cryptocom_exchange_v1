# signature.py

import hmac
import hashlib
import time
from dotenv import load_dotenv
import os

load_dotenv()


class SignatureGenerator:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def generate_signature(self, method, request_path, query_string='', body=''):
        api_secret_encoded = self.api_secret.encode('utf-8')
        timestamp = str(int(time.time() * 1000))
        what = timestamp + method + request_path + query_string + body
        signature = hmac.new(api_secret_encoded, what.encode('utf-8'), hashlib.sha256).hexdigest()
        return {
            'api_key': self.api_key,
            'sig': signature,
            'timestamp': timestamp
        }


if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    # Create an instance of the SignatureGenerator class
    sig_gen = SignatureGenerator(api_key, api_secret)

    # Generate a signature for a sample request
    method = "GET"
    request_path = "/v1/private/user-balance"
    query_string = ""
    body = ""

    signature_data = sig_gen.generate_signature(method, request_path, query_string, body)
    print("Generated Signature:", signature_data['sig'])
