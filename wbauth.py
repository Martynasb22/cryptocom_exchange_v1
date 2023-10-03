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

        response = ws.recv()
        print(f"Received: {response}")

        # Handle Heartbeats
        response_data = json.loads(response)
        if response_data.get("method") == "public/heartbeat":
            heartbeat_response = {
                "id": response_data.get("id"),
                "method": "public/respond-heartbeat"
            }
            ws.send(json.dumps(heartbeat_response))
            print("Sent heartbeat response")


if __name__ == "__main__":
    user_api = CryptoComWebsocket(api_key, api_secret)

    # For User API and Subscriptions
    user_api.connect("wss://stream.crypto.com/exchange/v1/user", "public/auth", 1)
    user_api.connect("wss://stream.crypto.com/exchange/v1/user", "user.balance", 2)
    # For Market Data Subscriptions
    # user_api.connect("wss://stream.crypto.com/exchange/v1/market", "public/auth", 1)
