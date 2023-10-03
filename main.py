# main.py


from balance import Balance
from dotenv import load_dotenv
import os
import json
import time
from tickers import Tickers
from candlestick import Candles
from colorama import Fore, Style
from helpers import SymbolInfo
from order_bot import OrderBot
from decimal import Decimal

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Inicijuojame Balance klasę ir gauname balansą
balance = Balance(api_key, api_secret)
balance.fetch_balance()

print(Fore.BLUE + "Available Balance:".ljust(25) + Style.RESET_ALL, Fore.RED + str(balance.user_balance).rjust(25)
      + Style.RESET_ALL)
print(Fore.BLUE + "USD Balance:".ljust(25) + Style.RESET_ALL, Fore.RED + str(balance.usd_balance).rjust(25)
      + Style.RESET_ALL)

# Nurodome base_url ir simbolį
base_url = "api.crypto.com/exchange/v1"
symbol = "AGIXUSD-PERP"
# Inicijuojame Tickers klasę ir gauname duomenis pagal simbolį
tickers = Tickers()
ticker_data = tickers.get_ticker_by_symbol(base_url, symbol)

# Atspausdiname gautus duomenis, jei jie yra
if ticker_data:
    print(Style.DIM + Fore.WHITE + f"Ticker Data:".ljust(25) + Style.RESET_ALL)
    tickers.print_ticker_data()

symbol_info = SymbolInfo('symbols.json')

candlestick = Candles()
candlestick_data = candlestick.get_candles_by_symbol(base_url, symbol, time_interval="M5")

if candlestick_data:
    print(Style.DIM + Fore.WHITE + f"Candlestick Data:".ljust(25) + Style.RESET_ALL)
    print_candlestick_data = candlestick.print_candlestick_data(symbol_name=symbol)

with open("symbols.json", "r") as f:
    symbols = json.load(f)

order_bot = OrderBot(api_key, api_secret, 'symbols.json')
ticker = Tickers()
while True:
    for symbol_dict in symbols:  # Assuming symbols is a list of dictionaries
        base_url = "api.crypto.com/exchange/v1"

        symbol = symbol_dict.get('symbol', None)
        if symbol is None:
            print("Symbol not found in dictionary")
            continue

        print(f"Fetching data for symbol: {symbol}")  # Debugging line

        ticker_data = tickers.get_ticker_by_symbol(base_url, symbol)

        if ticker_data:
            print(Style.DIM + Fore.WHITE + f"Ticker Data:".ljust(25) + Style.RESET_ALL)
            tickers.print_ticker_data()

        candlestick = Candles()

        print(f"Fetching candlestick data for instrument_name: {symbol}")

        candlestick_data = candlestick.get_candles_by_symbol(base_url, symbol, time_interval="M5")

        if candlestick_data:
            candlestick.print_candlestick_data(symbol_name=symbol)
        else:
            print(f"Failed to fetch candlestick data for {symbol}")
            continue

        sma, upper_band, lower_band = candlestick.calculate_bollinger_bands(period=20, deviation=2)

        if upper_band is None:
            continue

        close_price = float(candlestick_data[-1].get("c", 0))

        signal = None
        if close_price > upper_band:
            print(f"Planning to open SHORT position on {symbol} at price {close_price}")
            signal = 'SHORT'
        elif close_price < lower_band:
            print(f"Planning to open LONG position on {symbol} at price {close_price}")
            signal = 'LONG'
        else:
            print(f"No action planned on {symbol}")
            continue

        # Fetch the current balance
        balance.fetch_balance()
        price = float(candlestick_data[-1].get("o", 0))

        if price is not None:
            qty = balance.user_balance / price
            qty = qty * 0.95
            qty = round(qty, 0)
            qty = qty * 15
            # Reduce the quantity by 5% to avoid insufficient balance error
        else:
            print(f"Failed to fetch best price for {symbol}")

        if signal == "SHORT":
            response = order_bot.open_order(symbol, "SELL", "MARKET", qty)
            print(response)
        elif signal == "LONG":
            response = order_bot.open_order(symbol, "BUY", "MARKET", qty)
            print(response)

        # If the response is not None and the order is successfully placed
        if response and response.get("code", None) == 0:
            print("Order placed successfully for", symbol)

        time.sleep(0.5)
