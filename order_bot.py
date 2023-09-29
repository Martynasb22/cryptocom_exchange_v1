# order_bot.py

from typing import Optional
from private_api import PrivateAPI


class OrderBot(PrivateAPI):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)

    def open_order(self, instrument_name: str, side: str, order_type: str, price: str,
                   quantity: str, client_oid: Optional[str] = None, exec_inst: Optional[list] = None,
                   time_in_force: Optional[str] = None):
        method = "private/create-order"
        params = {
            "instrument_name": instrument_name,
            "side": side,
            "type": order_type,
            "price": price,
            "quantity": quantity,
            "client_oid": client_oid,
            "exec_inst": exec_inst,
            "time_in_force": time_in_force
        }

        response = self.make_request("POST", method, params)
        return response

    def close_order(self, instrument_name: str, order_type: str, price: Optional[str] = None):
        method = "private/close-position"
        params = {
            "instrument_name": instrument_name,
            "type": order_type,
            "price": price
        }

        response = self.make_request("POST", method, params)
        return response


