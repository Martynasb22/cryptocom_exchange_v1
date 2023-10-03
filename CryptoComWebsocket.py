# CryptoComWebsocket.py

from dotenv import load_dotenv
import os
import json
import time
import hmac
import hashlib
from websocket import create_connection

# Įkelti .env failą
load_dotenv()

# Nuskaityti API raktus
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


class CryptoComWebsocket:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.ws = None

    def generate_signature(self, method, id, params=None, nonce=None):
        if params:
            sorted_params = sorted(params.items())
            param_str = "".join(f"{k}{v}" for k, v in sorted_params)
        else:
            param_str = ""

        nonce = nonce or int(time.time() * 1000)
        payload = f"{method}{id}{self.api_key}{param_str}{nonce}"
        h = hmac.new(self.api_secret, payload.encode(), hashlib.sha256)
        return h.hexdigest(), nonce

    def public_auth(self, url):
        request_data = {
            "id": 1,
            "method": "public/auth"
        }
        self.ws = create_connection(url)
        self.ws.send(json.dumps(request_data))
        while True:
            response = self.ws.recv()
            response_data = json.loads(response)
            if response_data.get('method') == 'public/heartbeat':
                self.heartbeat_response(response_data)

    def heartbeat_response(self, response_data):
        if self.ws:
            heartbeat_response = {
                "id": response_data.get('id'),
                "method": "public/respond-heartbeat"
            }
            self.ws.send(json.dumps(heartbeat_response))
            print("Sent heartbeat response")

    def connect(self, url, method, id, params=None):
        sig, nonce = self.generate_signature(method, id, params)
        request_data = {
            "id": id,
            "method": method,
            "api_key": self.api_key,
            "sig": sig,
            "nonce": nonce
        }
        if params:
            request_data["params"] = params

        ws = create_connection(url)
        ws.send(json.dumps(request_data))

    def subscribe(self, url, channels, id):
        method = 'subscribe'
        params = {'channels': channels}
        sig, nonce = self.generate_signature(method, id, params)
        request_data = {
            "id": id,
            "method": method,
            "api_key": self.api_key,
            "sig": sig,
            "nonce": nonce,
            "params": params
        }
        ws = create_connection(url)
        ws.send(json.dumps(request_data))

        while True:
            response = ws.recv()
            print(f"Received: {response}")
            response_data = json.loads(response)
            if response_data.get("method") == "public/heartbeat":
                heartbeat_response = {
                    "id": response_data.get("id"),
                    "method": "public/respond-heartbeat"
                }
                ws.send(json.dumps(heartbeat_response))
                print("Sent heartbeat response")
