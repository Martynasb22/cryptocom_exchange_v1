# positions.py

import requests
import time
import os
from colorama import Fore, Style
from dotenv import load_dotenv
from private_api import PrivateAPI

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


class PositionAPI:
    def __init__(self, api_key, api_secret):
        self.api = PrivateAPI(api_key, api_secret)
        self.user_positions = {}
        self.usd_balance = 0.0  # Already added

    def fetch_position(self):
        """Fetch the current positions."""
        method = "private/get-positions"
        params = {}
        request_data = self.api.prepare_request_data(method, params)
        base_url = self.api.BASE_URL

        try:
            response = requests.post(f"{base_url}/{method}", json=request_data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Network Error: {e}")
            return None

        if response.ok:
            data = response.json()
            if data.get("code") == 0:
                print("Successfully fetched balance")
                self.user_positions = data["result"]["data"]
                return data
            else:
                print(f"Error: {data.get('code', 'Unknown error')}")
                return None
        else:
            print(f"Received Error Response: Status Code {response.status_code}")
            return None


def format_position(position):
    """Format the position data."""
    symbol = position['instrument_name']

    try:
        quantity = float(position['quantity'])  # Konvertuojame į float
        session_pnl = float(position['session_pnl'])
        open_position_pnl = float(position['open_position_pnl'])
        cost = float(position['cost'])
    except ValueError as e:
        print(f"ValueError: {e}")
        return None

    position_type = Fore.LIGHTGREEN_EX + "LONG" if quantity > 0 else Fore.LIGHTRED_EX + "SHORT"
    session_pnl_color = Fore.LIGHTGREEN_EX if session_pnl > 0 else Fore.LIGHTRED_EX
    open_position_pnl_color = Fore.LIGHTGREEN_EX if open_position_pnl > 0 else Fore.LIGHTRED_EX

    return (f"{Fore.CYAN}{symbol}{Style.RESET_ALL}: {position_type + Style.RESET_ALL}, "
            f"Session PnL: {session_pnl_color}{session_pnl}{Style.RESET_ALL}, "
            f"Open Position PnL: {open_position_pnl_color}{open_position_pnl}{Style.RESET_ALL}, "
            f"Cost: {Fore.LIGHTBLUE_EX}{cost}{Style.RESET_ALL}")


if __name__ == "__main__":
    position_api = PositionAPI(api_key, api_secret)

    while True:
        position_api.fetch_position()
        formatted_positions = [format_position(pos) for pos in position_api.user_positions]

        print(Fore.BLUE + "Formatted Positions:".rjust(25) + Style.RESET_ALL)
        for fp in formatted_positions:
            print(fp)

        time.sleep(1)
