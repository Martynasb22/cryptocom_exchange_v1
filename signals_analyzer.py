# signals_analyzer.py
from market_data import MarketDataAPI
import numpy as np
import pandas as pd


# Moving Average (MA)
def moving_average(data, window):
    return data['c'].rolling(window=window).mean()


# Relative Strength Index (RSI)
def rsi(data, window):
    delta = data['c'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# Bollinger Bands
def bollinger_bands(data, window, num_std_dev):
    rolling_mean = data['c'].rolling(window=window).mean()
    rolling_std = data['c'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return lower_band, rolling_mean, upper_band


# MACD
def macd(data, short_window, long_window, signal_window):
    short_ema = data['c'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['c'].ewm(span=long_window, adjust=False).mean()
    MACD = short_ema - long_ema
    signal_line = MACD.ewm(span=signal_window, adjust=False).mean()
    return MACD, signal_line


# Fibonacci Retracement Levels
def fibonacci_retracement(high, low):
    diff = high - low
    level1 = high - 0.236 * diff
    level2 = high - 0.382 * diff
    level3 = high - 0.618 * diff
    return level1, level2, level3


# Volume
def volume_signal(data):
    return data['v']


# Stochastic Oscillator
def stochastic_oscillator(data, window):
    high = data['h'].rolling(window=window).max()
    low = data['l'].rolling(window=window).min()
    k = 100 * ((data['c'] - low) / (high - low))
    return k


# Sample DataFrame
data = pd.DataFrame({'h': np.random.rand(100),
                     'l': np.random.rand(100),
                     'c': np.random.rand(100),
                     'v': np.random.rand(100)})

# Use Functions
print("Moving Average:", moving_average(data, 5).tail())
print("RSI:", rsi(data, 14).tail())
print("Bollinger Bands:", bollinger_bands(data, 20, 2))
print("MACD:", macd(data, 12, 26, 9))
print("Fibonacci Retracement:", fibonacci_retracement(data['h'].max(), data['l'].min()))
print("Volume:", volume_signal(data).tail())
print("Stochastic Oscillator:", stochastic_oscillator(data, 14).tail())


def get_all_signals(symbol):
    # Sukurkite CryptoComAPI objektą ir gaukite duomenis
    market_data = MarketDataAPI(symbol)
    market_data.get_candlestick()
    candlestick_data = market_data.candlestick_data

    # Konvertuokite duomenis į DataFrame
    data = pd.DataFrame(candlestick_data)

    # Konvertuokite tekstines eilutes į skaičius
    for col in ['o', 'h', 'l', 'c', 'v']:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Panaudokite funkcijas su naujais duomenimis
    ma = moving_average(data, 5).tail()
    rsi_values = rsi(data, 14).tail()
    lower_band, rolling_mean, upper_band = bollinger_bands(data, 20, 2)
    MACD, signal_line = macd(data, 12, 26, 9)
    level1, level2, level3 = fibonacci_retracement(data['h'].max(), data['l'].min())
    volume = volume_signal(data).tail()
    stochastic = stochastic_oscillator(data, 14).tail()

    return {
        'Moving Average': ma,
        'RSI': rsi_values,
        'Bollinger Bands': (lower_band, rolling_mean, upper_band),
        'MACD': (MACD, signal_line),
        'Fibonacci Retracement': (level1, level2, level3),
        'Volume': volume,
        'Stochastic Oscillator': stochastic
    }

# Pavyzdys naudojant funkciją
# signals = get_all_signals("SANDUSD-PERP")
# for key, value in signals.items():
#     print(f"{key}: {value}")
