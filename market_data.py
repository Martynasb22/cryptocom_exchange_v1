# market_data.py

import requests
import json


class MarketDataAPI:
    def __init__(self, symbol):
        self.candlestick_data = None
        self.symbol = symbol
        self.base_url = "https://api.crypto.com/exchange/v1/public/"

    def get_book(self, depth=100):
        url = f"{self.base_url}get-book?instrument_name={self.symbol}&depth={depth}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            book_data = data['result']['data'][0]
            bids = []
            asks = []
            for bid in book_data['bids']:
                bids.append({
                    'price': float(bid[0]),
                    'quantity': float(bid[1]),
                    'number_of_orders': int(bid[2])
                })
            for ask in book_data['asks']:
                asks.append({
                    'price': float(ask[0]),
                    'quantity': float(ask[1]),
                    'number_of_orders': int(ask[2])
                })
            return {'bids': bids, 'asks': asks}
        else:
            return None

    def get_candlestick(self, timeframe="M15", count=100):
        url = f"{self.base_url}get-candlestick?instrument_name={self.symbol}&timeframe={timeframe}&count={count}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            candlestick_data = []
            for candle_data in data['result']['data']:
                candlestick_data.append({
                    'open_price': float(candle_data['o']),
                    'high_price': float(candle_data['h']),
                    'low_price': float(candle_data['l']),
                    'close_price': float(candle_data['c']),
                    'volume': float(candle_data['v']),
                    'start_time': int(candle_data['t'])
                })
            return candlestick_data
        else:
            return None

    def get_trades(self, count=25):
        url = f"{self.base_url}get-trades?instrument_name={self.symbol}&count={count}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            trades_data = []
            for trade_data in data['result']['data']:
                trades_data.append({
                    'trade_side': trade_data['s'],
                    'trade_price': float(trade_data['p']),
                    'trade_quantity': float(trade_data['q']),
                    'trade_timestamp': int(trade_data['t']),
                    'trade_id': trade_data['d'],
                    'trade_instrument': trade_data['i']
                })
            return trades_data
        else:
            return None

    def get_tickers(self):
        url = f"{self.base_url}get-tickers?instrument_name={self.symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            tickers_data = []
            for ticker_data in data['result']['data']:
                tickers_data.append({
                    'high_price': float(ticker_data['h']),
                    'low_price': float(ticker_data['l']),
                    'last_trade_price': float(ticker_data['a']),
                    'instrument_name': ticker_data['i'],
                    'total_volume_24h': float(ticker_data['v']),
                    'total_volume_value_24h': float(ticker_data['vv']),
                    'open_interest': float(ticker_data['oi']),
                    'price_change_24h': float(ticker_data['c']),
                    'best_bid_price': float(ticker_data['b']),
                    'best_ask_price': float(ticker_data['k'])
                })
            return tickers_data
        else:
            return None


