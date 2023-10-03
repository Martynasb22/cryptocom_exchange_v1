
# candlestick.py

from pprint import pprint
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from colorama import Fore, Style

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4))


class Candles:

    def __init__(self):
        self.base_url = "https://api.crypto.com/exchange/v1"
        self.candles = []  # Saugoti visus žvakidžių objektus
        self.ax1 = ax1
        self.ax2 = ax2

    def get_candles_by_symbol(self, base_url, symbol, time_interval=5) -> Any | None:
        url = (f"https://{base_url}/public/get-candlestick?instrument_name={symbol}"
               f"&timeframe={time_interval}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 0:
                self.candles = data["result"]["data"]
                return self.candles
            self.candles = data.get("result", {}).get("data", [])
            return self.candles

        else:
            print(f"{Fore.RED}Error: {response.status_code}{Style.RESET_ALL}")
            print("Response:", response.text)
            print("Endpoint:", url)

            return None

    def calculate_rsi_list(self, periods=14):
        close_prices = np.array(
            [float(candle.get('c', 0)) for candle in self.candles]
        )
        rsi_list = []
        for i in range(periods, len(close_prices)):
            sub_prices = close_prices[i - periods:i]
            delta = sub_prices[1:] - sub_prices[:-1]
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, abs(delta), 0)
            avg_gain = np.mean(gain[-periods:])
            avg_loss = np.mean(loss[-periods:])
            rs = avg_gain / avg_loss if avg_loss != 0 else 0  # Relative Strength
            rsi = 100 - (100 / (1 + rs))
            rsi_list.append(rsi)
        return rsi_list

    def calculate_signal(self, upper_band, lower_band, close_price):
        # Calculate the mean if upper_band or lower_band is a list
        upper_band = np.mean(upper_band) if isinstance(upper_band, list) else upper_band
        lower_band = np.mean(lower_band) if isinstance(lower_band, list) else lower_band

        # Check if upper_band and lower_band are float or integer
        if not isinstance(upper_band, (float, int)) or not isinstance(lower_band, (float, int)):
            print(f"Error: upper_band or lower_band is not of type float or int.")
            return 'HOLD'

        rsi_list = self.calculate_rsi_list()
        last_rsi = rsi_list[-1] if rsi_list else None
        if last_rsi is None:
            return 'HOLD'

        if close_price > upper_band and last_rsi > 70:
            return 'SHORT'
        elif close_price < lower_band and last_rsi < 30:
            return 'LONG'
        else:
            return 'HOLD'

    def print_candlestick_data(self, symbol_name):
        # Prepare the data
        open_prices = [float(candle.get('o', 0)) for candle in self.candles]
        high_prices = [float(candle.get('h', 0)) for candle in self.candles]
        low_prices = [float(candle.get('l', 0)) for candle in self.candles]
        close_prices = [float(candle.get('c', 0)) for candle in self.candles]
        timestamps = [candle.get('t', 0) for candle in self.candles]

        # First plot with candles
        self.ax1.plot(timestamps, open_prices, label='Open Prices')
        self.ax1.plot(timestamps, high_prices, label='High Prices')
        self.ax1.plot(timestamps, low_prices, label='Low Prices')
        self.ax1.plot(timestamps, close_prices, label='Close Prices')
        self.ax1.set_xlabel('Timestamps')
        self.ax1.set_ylabel('Prices')
        self.ax1.set_title(f'Candlestick Data for {symbol_name}', color='black')
        self.ax1.legend()

        rsi_values = self.calculate_rsi_list()
        rsi_last = rsi_values[-1] if rsi_values else 0

        timestamps_for_rsi = timestamps[-len(rsi_values):]
        self.ax2.plot(timestamps_for_rsi, rsi_values, label='RSI')

        signal = self.calculate_signal(high_prices, low_prices, close_prices[-1])

        # Čia pridedame signalo tekstą prie antrąją grafiką
        self.ax2.text(0.5, 0.9, f'Signal: {signal}', horizontalalignment='center',
                      verticalalignment='center', transform=self.ax2.transAxes)

        if signal == 'SHORT':
            self.ax2.axhline(y=70, color='r', linestyle='--')
        elif signal == 'LONG':
            self.ax2.axhline(y=30, color='g', linestyle='--')
        else:
            self.ax2.axhline(y=50, color='b', linestyle='-')

        self.ax2.set_title('RSI Signal', color='black')

        # Display the updated plot
        plt.tight_layout()
        plt.draw()
        plt.pause(1)

        # Išvalyti grafikus
        self.ax1.clear()
        self.ax2.clear()

    def calculate_bollinger_bands(self, period=20, deviation=2):
        close_prices = [float(candle.get('c', 0)) for candle in self.candles[-period:]]

        if len(close_prices) < period:
            print(f"Not enough data to calculate Bollinger Bands. Need at least {period} time periods.")
            return None, None, None

        if not all(isinstance(price, (float, int)) for price in close_prices):
            print("All closing prices should be numeric.")
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