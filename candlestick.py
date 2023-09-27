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
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        plt.show(block=False)

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

    def print_candlestick_data(self, symbol_name, signal=None):
        # Paruošti duomenis
        open_prices = [float(candle.get('o', 0)) for candle in self.candles]
        high_prices = [float(candle.get('h', 0)) for candle in self.candles]
        low_prices = [float(candle.get('l', 0)) for candle in self.candles]
        close_prices = [float(candle.get('c', 0)) for candle in self.candles]
        timestamps = [candle.get('t', 0) for candle in self.candles]

        # Išvalyti esamus grafikus
        self.ax1.clear()
        self.ax2.clear()

        # Pirmas plot'as su žvakidėm
        self.ax1.plot(timestamps, open_prices, label='Open Prices')
        self.ax1.plot(timestamps, high_prices, label='High Prices')
        self.ax1.plot(timestamps, low_prices, label='Low Prices')
        self.ax1.plot(timestamps, close_prices, label='Close Prices')
        self.ax1.set_xlabel('Timestamps')
        self.ax1.set_ylabel('Prices')
        self.ax1.set_title(f'Candlestick Data for {symbol_name}', color='black')
        self.ax1.legend()

        # Antras plot'as su signalu
        if signal == 'SHORT':
            signal_color = 'red'
        elif signal == 'LONG':
            signal_color = 'green'
        else:
            signal_color = 'black'
        signal_data = [open_prices[-1]] * len(close_prices)
        self.ax2.plot(timestamps, close_prices, label='Close Prices')
        self.ax2.plot(timestamps, signal_data, label='Signal', color=signal_color)
        self.ax2.set_xlabel('Timestamps')
        self.ax2.set_ylabel('Prices')
        self.ax2.set_title(f'Signal for {symbol_name}', color='black')
        self.ax2.legend()

        # Atvaizduoti atnaujintą grafiką
        plt.tight_layout()
        plt.draw()
        plt.pause(1)

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
