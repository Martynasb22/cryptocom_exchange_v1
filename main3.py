import time

from market_data import MarketDataAPI
from trading_signals import TradingSignals
from symbols import CryptoComAPI


def main():
    api = CryptoComAPI()
    api.fetch_instruments()

    while True:
        for symbol in api.perpetuals:
            symbol = symbol['symbol']
            print(f"Checking signals for {symbol}")

            # Create a new MarketDataAPI object for each symbol
            marketDataAPI = MarketDataAPI(symbol)

            candlestick_data = marketDataAPI.get_candlestick()
            trades_data = marketDataAPI.get_trades()
            signals = TradingSignals(candlestick_data, trades_data, symbol)

            print("SMA Signal:", signals.sma_signals())
            print("EMA Signal:", signals.ema_signals())
            print("RSI Signal:", signals.rsi_signals())
            print("Bollinger Bands Signal:", signals.bollinger_bands_signals())
            print("MACD Signal:", signals.macd_signals())
            print("Volume Price Trend Signal:",
                  signals.volume_price_trend_signals())  # Pakeisti volume_signals() į volume_price_trend_signals()
            print("Stochastic Oscillator Signal:", signals.stochastic_signals())
            print("Fibonacci Signal:", signals.fibonacci_signals())  # Pridėti fibonacci_signals()

        print("Finished checking all symbols. Sleeping for 60 seconds.")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
