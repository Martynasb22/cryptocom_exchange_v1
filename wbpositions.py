from CryptoComWebsocket import CryptoComWebsocket


class CryptoComUser:
    def __init__(self, api_key, api_secret):
        self.ws = CryptoComWebsocket(api_key, api_secret)

    def subscribe(self, channels):
        return self.ws.subscribe('wss://stream.crypto.com/exchange/v1/user', channels, 1)

    def get_balance(self):
        return self.ws.subscribe("wss://stream.crypto.com/exchange/v1/user", ['balance'], 1)

    def get_positions(self):
        return self.ws.subscribe("wss://stream.crypto.com/exchange/v1/user", ['user.positions'], 1)

    def get_account_risk(self):
        return self.ws.subscribe("wss://stream.crypto.com/exchange/v1/user", ['user.account_risk'], 1)

    def get_position_balance(self):
        return self.ws.subscribe("wss://stream.crypto.com/v1/user", ['user.position_balance'], 1)
