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

    def print_symbol_info_data(self, symbol):
        info = self.get_info_by_symbol(symbol)

        if type(info) is dict:
            print(Fore.BLUE + "Display Name:".ljust(25) + Style.RESET_ALL + Fore.RED + info.get(
                'display_name', 'Display name not found').rjust(25) + Style.RESET_ALL)
            print(Fore.BLUE + "Quote decimals:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
                info.get('quote_decimals', 'Quote decimals not found')).rjust(25) + Style.RESET_ALL)
            print(Fore.BLUE + "Quantity decimals:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
                info.get('quantity_decimals', 'Quantity decimals not found')).rjust(25) + Style.RESET_ALL)
            print(Fore.BLUE + "Qty tick size:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
                info.get('qty_tick_size', 'Qty tick size not found')).rjust(25) + Style.RESET_ALL)
            print(Fore.BLUE + "Price tick size:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
                info.get('price_tick_size', 'Price tick size not found')).rjust(25) + Style.RESET_ALL)
            print(Fore.BLUE + "Max leverage:".ljust(25) + Style.RESET_ALL + Fore.RED + str(
                info.get('max_leverage', 'Max leverage not found')).rjust(25) + Style.RESET_ALL)
        else:
            print(Fore.RED + info + Style.RESET_ALL)


if __name__ == "__main__":
    symbol_info = SymbolInfo('symbols.json')
    symbol_info.print_symbol_info_data('ETHUSD-PERP')
    symbol_info.print_symbol_info_data('BTCUSD-PERP')
    symbol_info.print_symbol_info_data('BTCUSDT')
    symbol_info.print_symbol_info_data('ETHUSD')
    symbol_info.print_symbol_info_data('ETHUSD-210625')
