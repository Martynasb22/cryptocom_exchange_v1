# tickers.py

import requests
import json
from colorama import Fore, Style


class Tickers:
    def __init__(self):
        self.base_url = "https://api.crypto.com/exchange/v1"
        self.highest_trade_24h = None
        self.lowest_trade_24h = None
        self.latest_trade_price = None
        self.instrument_name = None
        self.total_volume_24h = None
        self.total_volume_value_24h = None
        self.open_interest = None
        self.price_change_24h = None
        self.best_bid_price = None
        self.best_ask_price = None
        self.timestamp = None

    def get_ticker_by_symbol(self, base_url, symbol):
        url = f"https://{base_url}/public/get-tickers?instrument_name={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ticker_data = data.get("result", {}).get("data", [{}])[0]
            self.highest_trade_24h = ticker_data.get("h")
            self.lowest_trade_24h = ticker_data.get("l")
            self.latest_trade_price = ticker_data.get("a")
            self.instrument_name = ticker_data.get("i")
            self.total_volume_24h = ticker_data.get("v")
            self.total_volume_value_24h = ticker_data.get("vv")
            self.open_interest = ticker_data.get("oi")
            self.price_change_24h = ticker_data.get("c")
            self.best_bid_price = ticker_data.get("b")
            self.best_ask_price = ticker_data.get("k")
            self.timestamp = ticker_data.get("t")
            return ticker_data
        else:
            print(f"Error: {response.status_code}")
            return None

    def print_ticker_data(self):
        print(
            Fore.BLUE + "Highest trade 24h:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.highest_trade_24h).rjust(
                25) + Style.RESET_ALL)
        print(Fore.BLUE + "Lowest trade 24h:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.lowest_trade_24h).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Latest trade price:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
            self.latest_trade_price).rjust(25) + Style.RESET_ALL)
        print(Fore.BLUE + "Instrument name:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.instrument_name).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Total volume 24h:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.total_volume_24h).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Total volume value 24h:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
            self.total_volume_value_24h).rjust(25) + Style.RESET_ALL)
        print(Fore.BLUE + "Open interest:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.open_interest).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Price change 24h:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.price_change_24h).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Best bid price:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.best_bid_price).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Best ask price:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.best_ask_price).rjust(
            25) + Style.RESET_ALL)
        print(Fore.BLUE + "Timestamp:".ljust(25) + Style.RESET_ALL + Fore.RED + str(self.timestamp).rjust(
            25) + Style.RESET_ALL)
