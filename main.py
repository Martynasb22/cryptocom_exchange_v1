# main.py

from balance import Balance
from dotenv import load_dotenv
import os
from tickers import Tickers
from candlestick import Candles
from colorama import Fore, Style
import matplotlib.pyplot as plt

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

candlestick = Candles()
candlestick_data = candlestick.get_candles_by_symbol(base_url, symbol, time_interval="M5")

if candlestick_data:
    print(Style.DIM + Fore.WHITE + f"Candlestick Data:".ljust(25) + Style.RESET_ALL)
    print_candlestick_data = candlestick.print_candlestick_data()


