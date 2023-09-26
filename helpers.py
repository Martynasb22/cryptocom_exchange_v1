# helpers.py
import json
from pprint import pprint
from colorama import Fore, Style


class SymbolInfo:
    def __init__(self, json_file_path):
        with open(json_file_path, 'r') as f:
            self.symbols_data = json.load(f)
        self.symbol_dict = {}
        for item in self.symbols_data:
            self.symbol_dict[item['symbol']] = item

    def get_info_by_symbol(self, symbol):
        return self.symbol_dict.get(symbol, "Symbol not found")

    def get_display_name(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('display_name', 'Display name not found') if info != "Symbol not found" else info

    def get_quote_decimals(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('quote_decimals', 'Display name not found') if info != "Symbol not found" else info

    def get_quantity_decimals(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('quantity_decimals', 'Base currency not found') if info != "Symbol not found" else info

    def get_price_tick_size(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('price_tick_size', 'Quote currency not found') if info != "Symbol not found" else info

    def get_qty_tick_size(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('qty_tick_size', 'Base currency not found') if info != "Symbol not found" else info

    def get_max_leverage(self, symbol):
        info = self.get_info_by_symbol(symbol)
        return info.get('max_leverage', 'Max leverage not found') if info != "Symbol not found" else info


if __name__ == "__main__":
    symbol_info = SymbolInfo('symbols.json')
    print(Fore.BLUE + "Display Name:".ljust(25) + Style.RESET_ALL + Fore.RED + symbol_info.get_display_name(
        'BTCUSD-PERP').rjust(25) + Style.RESET_ALL)
    print(Fore.BLUE + "Quote decimals:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
        symbol_info.get_quote_decimals('BTCUSD-PERP')).rjust(25) + Style.RESET_ALL)
    print(Fore.BLUE + "Quantity decimals:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
        symbol_info.get_quantity_decimals('BTCUSD-PERP')).rjust(25) + Style.RESET_ALL)
    print(Fore.BLUE + "Qty tick size:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
        symbol_info.get_qty_tick_size('BTCUSD-PERP')).rjust(25) + Style.RESET_ALL)
    print(Fore.BLUE + "Price tick size:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
        symbol_info.get_price_tick_size('BTCUSD-PERP')).rjust(25) + Style.RESET_ALL)
    print(Fore.BLUE + "Max leverage:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
        symbol_info.get_max_leverage('BTCUSD-PERP')).rjust(25) + Style.RESET_ALL)


