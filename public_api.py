# public_api.py

import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

from numpy import ma

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


# Funkcija, skirta gauti kainų duomenis
def get_prices(symbol):
    url = "https://api.crypto.com/v1/public/get-candlestick"
    params = {
        "symbol": symbol,
    }
    headers = {
        "X-CMC_PRO_API_KEY": api_key,
    }
    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.content)


# Funkcija, skirta apskaičiuoti RCI
def calculate_rci(prices, period=14):
    delta = prices['close'].diff()
    up_direction = delta.where(delta > 0, 0)
    down_direction = -delta.where(delta < 0, 0)
    relative_strength = up_direction.ewm(span=period, min_periods=period - 1).mean() / down_direction.ewm(span=period,
                                                                                                          min_periods=period - 1).mean()
    return 100 * relative_strength


# Funkcija, skirta apskaičiuoti Bollinger Bands
def calculate_bollinger_bands(prices, period=20, std=2):
    average = prices['close'].rolling(window=period).mean()
    standard_deviation = prices['close'].rolling(window=period).std()
    upper_band = average + std * 2
    lower_band = average - std * 2
    return upper_band, lower_band


# Funkcija, skirta apskaičiuoti MA
def calculate_ma(prices, period=20):
    return prices['close'].rolling(window=period).mean()


# Funkcija, skirta nustatyti signalą
def get_signal(prices):
    rci = calculate_rci(prices)
    bb_upper, bb_lower = calculate_bollinger_bands(prices)
    ma = calculate_ma(prices)

    # Pirkimo signalas
    if rci > 70 and prices['close'] < bb_lower:
        return "buy"

    # Pardavimo signalas
    if rci < 30 and prices['close'] > bb_upper:
        return "sell"

    # Jokio signalo
    return None


# Pagrindinė programos dalis
symbol = "BTC-USD"
prices = get_prices(symbol)
signal = get_signal(prices)

# Išvedama informacija
print(f"Signalas: {signal}")
print(f"RCI: {rci}")
print(f"Bollinger Bands: {bb_upper} - {bb_lower}")
print(f"MA: {ma}")
