# technical_indicators.py


import pandas as pd
import numpy as np

from market_data import MarketDataAPI

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class TechnicalIndicators:
    def __init__(self, candlestick_data, trades_data):
        self.candlestick_data = pd.DataFrame(candlestick_data)
        self.trades_data = pd.DataFrame(trades_data)

    def sma(self, window):
        return self.candlestick_data['close_price'].rolling(window=window).mean()

    def ema(self, window):
        return self.candlestick_data['close_price'].ewm(span=window, adjust=False).mean()

    def rsi(self, window):
        delta = self.trades_data['trade_price'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def bollinger_bands(self, window):
        sma = self.sma(window)
        rolling_std = self.candlestick_data['close_price'].rolling(window=window).std()
        upper_band = sma + (rolling_std * 2)
        lower_band = sma - (rolling_std * 2)
        return lower_band, sma, upper_band

    def macd(self):
        ema12 = self.ema(12)
        ema26 = self.ema(26)
        return ema12 - ema26

    def fibonacci_retracement(self):
        max_price = self.candlestick_data['high_price'].max()
        min_price = self.candlestick_data['low_price'].min()
        diff = max_price - min_price
        levels = [min_price, min_price + 0.236 * diff, min_price + 0.382 * diff, min_price + 0.618 * diff, max_price]
        return levels

    def volume_price_trend(self):
        vpt = 0
        for i in range(1, len(self.candlestick_data)):
            vpt += self.candlestick_data['volume'][i] * (
                        (self.candlestick_data['close_price'][i] - self.candlestick_data['close_price'][i - 1]) /
                        self.candlestick_data['close_price'][i - 1])
        return vpt

    def stochastic_oscillator(self, k_window, d_window):
        high = self.candlestick_data['high_price'].rolling(window=k_window).max()
        low = self.candlestick_data['low_price'].rolling(window=k_window).min()
        k = 100 * ((self.candlestick_data['close_price'] - low) / (high - low))
        d = k.rolling(window=d_window).mean()
        return k, d
