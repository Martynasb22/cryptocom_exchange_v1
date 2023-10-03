# trading_signals.py
import numpy as np

from technical_indicators import TechnicalIndicators
from colorama import Fore


class TradingSignals(TechnicalIndicators):

    def __init__(self, candlestick_data, trades_data, symbol):
        super().__init__(candlestick_data, trades_data)
        self.symbol = symbol

    def gather_signals(self):
        signals = []
        signal_methods = [
            self.sma_signals,
            self.ema_signals,
            self.rsi_signals,
            self.bollinger_bands_signals,
            self.macd_signals,
            self.volume_price_trend_signals,
            self.stochastic_signals,
            self.fibonacci_signals,
        ]
        for method in signal_methods:
            signal = method()
            if "LONG" in signal:
                signals.append(1)
            elif "SHORT" in signal:
                signals.append(-1)
        return signals

    def sma_signals(self):
        sma_50 = self.sma(50)
        sma_200 = self.sma(200)
        if not np.isnan(sma_50.iloc[-1]) and not np.isnan(sma_200.iloc[-1]):
            if sma_50.iloc[-1] > sma_200.iloc[-1] and sma_50.iloc[-2] < sma_200.iloc[-2]:
                return Fore.GREEN + "LONG, SMA 50 Value: {}, SMA 200 Value: {}".format(sma_50.iloc[-1],
                                                                                       sma_200.iloc[-1]) + Fore.RESET
            elif sma_50.iloc[-1] < sma_200.iloc[-1] and sma_50.iloc[-2] > sma_200.iloc[-2]:
                return Fore.RED + "SHORT, SMA 50 Value: {}, SMA 200 Value: {}".format(sma_50.iloc[-1],
                                                                                      sma_200.iloc[-1]) + Fore.RESET

        return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def ema_signals(self):
        ema_12 = self.ema(12)
        ema_26 = self.ema(26)

        if ema_12.iloc[-1] > ema_26.iloc[-1] and ema_12.iloc[-2] < ema_26.iloc[-2]:
            return Fore.GREEN + "LONG, EMA 12 Value: {}, EMA 26 Value: {}".format(ema_12.iloc[-1],
                                                                                  ema_26.iloc[-1]) + Fore.RESET
        elif ema_12.iloc[-1] < ema_26.iloc[-1] and ema_12.iloc[-2] > ema_26.iloc[-2]:
            return Fore.RED + "SHORT, EMA 12 Value: {}, EMA 26 Value: {}".format(ema_12.iloc[-1],
                                                                                 ema_26.iloc[-1]) + Fore.RESET
        return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def rsi_signals(self):
        rsi = self.rsi(14)

        if rsi.iloc[-1] < 30:
            return Fore.GREEN + "LONG, RSI Value: {}".format(rsi.iloc[-1]) + Fore.RESET
        elif rsi.iloc[-1] > 70:
            return Fore.RED + "SHORT, RSI Value: {}".format(rsi.iloc[-1]) + Fore.RESET
        return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def bollinger_bands_signals(self):
        lower_band, middle_band, upper_band = self.bollinger_bands(20)

        if self.candlestick_data['close_price'].iloc[-1] < lower_band.iloc[-1]:
            return Fore.GREEN + "LONG, Lower Band Value: {}, Middle Band Value: {}, Upper Band Value: {}".format(
                lower_band.iloc[-1], middle_band.iloc[-1], upper_band.iloc[-1]) + Fore.RESET
        elif self.candlestick_data['close_price'].iloc[-1] > upper_band.iloc[-1]:
            return Fore.RED + "SHORT, Lower Band Value: {}, Middle Band Value: {}, Upper Band Value: {}".format(
                lower_band.iloc[-1], middle_band.iloc[-1], upper_band.iloc[-1]) + Fore.RESET
        return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def macd_signals(self):
        macd = self.macd()

        if macd.iloc[-1] > 0 and macd.iloc[-2] < 0:
            return Fore.GREEN + "LONG, MACD Value: {}".format(macd.iloc[-1]) + Fore.RESET
        elif macd.iloc[-1] < 0 and macd.iloc[-2] > 0:
            return Fore.RED + "SHORT, MACD Value: {}".format(macd.iloc[-1]) + Fore.RESET
        else:
            return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def volume_price_trend_signals(self):
        vpt = self.volume_price_trend()
        if vpt > 0:
            return Fore.GREEN + "LONG, Volume Price Trend Value: {}".format(vpt) + Fore.RESET
        else:
            return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def fibonacci_signals(self):
        levels = self.fibonacci_retracement()
        close_price = self.candlestick_data['close_price'].iloc[-1]

        if close_price < levels[1]:
            return Fore.GREEN + "LONG, Close Price: {}, Fibonacci Level: {}".format(close_price, levels[1]) + Fore.RESET
        elif close_price > levels[3]:
            return Fore.RED + "SHORT, Close Price: {}, Fibonacci Level: {}".format(close_price, levels[3]) + Fore.RESET
        return Fore.YELLOW + "NO SIGNAL" + Fore.RESET

    def stochastic_signals(self):
        k, d = self.stochastic_oscillator(14, 3)

        if k.iloc[-1] > d.iloc[-1] and k.iloc[-2] < d.iloc[-2]:
            return Fore.GREEN + "LONG, K Value: {}, D Value: {}".format(k.iloc[-1], d.iloc[-1]) + Fore.RESET
        elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] > d.iloc[-2]:
            return Fore.RED + "SHORT, K Value: {}, D Value: {}".format(k.iloc[-1], d.iloc[-1]) + Fore.RESET
        else:
            return Fore.YELLOW + "NO SIGNAL" + Fore.RESET
