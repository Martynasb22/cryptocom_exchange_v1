# candlestick.py


from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from colorama import Fore, Style


class Candles:

    def __init__(self):
        self.base_url = "https://api.crypto.com/exchange/v1"
        self.candles = []  # Saugoti visus žvakidžių objektus

    def get_candles_by_symbol(self, base_url, symbol, time_interval=5) -> dict:
        url = (f"https://{base_url}/public/get-candlestick?instrument_name={symbol}"
               f"&timeframe={time_interval}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.candles = data.get("result", {}).get("data", [])
            return self.candles

        else:
            print(f"{Fore.RED}Error: {response.status_code}{Style.RESET_ALL}")
            print("Response:", response.text)
            print("Endpoint:", url)

            return None

    def print_candlestick_data(self):
        # Paruošti duomenis
        open_prices = [float(candle.get('o', 0)) for candle in self.candles]
        high_prices = [float(candle.get('h', 0)) for candle in self.candles]
        low_prices = [float(candle.get('l', 0)) for candle in self.candles]
        close_prices = [float(candle.get('c', 0)) for candle in self.candles]
        timestamps = [candle.get('t', 0) for candle in self.candles]

        # Atspausdinti duomenis
        for idx, candlestick in enumerate(self.candles):
            print(f"{Fore.BLUE}Candle {idx + 1}:{Style.RESET_ALL}")
            print(candlestick)

        # Nubrėžti kreivę
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, open_prices, label='Open Prices')
        plt.plot(timestamps, high_prices, label='High Prices')
        plt.plot(timestamps, low_prices, label='Low Prices')
        plt.plot(timestamps, close_prices, label='Close Prices')
        plt.xlabel('Timestamps')
        plt.ylabel('Prices')
        plt.title('Candlestick Data')
        plt.legend()
        plt.show()

    def calculate_bollinger_bands(self, period=20, deviation=2):
        close_prices = [float(candle.get('c', 0)) for candle in self.candles[-period:]]

        if len(close_prices) < period:
            return None, None, None

        sma = np.mean(close_prices)
        std_dev = np.std(close_prices)
        upper_band = sma + (std_dev * deviation)
        lower_band = sma - (std_dev * deviation)

        return sma, upper_band, lower_band

    def print_bollinger_bands(self, period=20, deviation=2):
        sma, upper_band, lower_band = self.calculate_bollinger_bands(period, deviation)
        if sma is None:
            print("Not enough data to calculate bollinger bands")
            return

        print(f"SMA: {sma}")
        print(f"Upper Band: {upper_band}")
        print(f"Lower Band: {lower_band}")
