#Here the documentation
#https://pypi.org/project/pykrakenapi/
import krakenex
from pykrakenapi import KrakenAPI
import time as t
import random


#Define API connection to Kraken
#api = krakenex.API(key="JiO5INLMivEfcYoOqLiBqYYnJKTeiMi7cfDs81EheIh4I7IxbsyBih5u", secret="0tFkglYnMtdG/ziHQPsC2UIZeEuuX+WW39ZAXWj23/KVheQvuPiqMt+aDF5x/zJ4HgL+DmJKshENUqqZufpE1Q==")
api = krakenex.API(key="Y7N/Lv3rp+Yw6o+XHax8rOxEjHnpY4V/VQuZvkyQSI0jJwcgg0khDx8v", secret="/SVhWxqPudL9vJQM6nsKTH2muZXPvrIgW+/+CircOPz4VUrrxJgOi1w8y5mjFE9iOu0YxI0gV7VwRAh/t//7CQ==")

#Open Kraken connection and define repetition cycle for row update
k = KrakenAPI(api)

class Kraken_Trailing_Stop_Loss:
    def __init__(self):
        self.trading_pair = ''
        self.side = ''
        self.trade_type = ''  # change this to "market" if you need to sell quickly - careful, you will be a market taker!
        self.sell_cycles = 6  # max packet size
        self.time_cycle = 30  # time interval between order placements
        self.balance_symbol_crypto = ''
        self.balance_symbol_fiat = ''
        self.minimum_crypto_balance = 0  # min imum remaining balance of above symbol after trades are completed
        self.minimum_fiat_balance = 0.0000  # minimum level for Bitcoin
        self.balance_fiat = 0
        self.balance_crypto = 0
        self.trailing_stop_loss_percentage = 0
        self.trailing_stop_loss_fixed_value = 0
        self.bid_price = 0
        self.trading_volume = 0
        self.peak_value = 0
        self.stop_loss_exit_level = 0
        self.selling_price = 0
        self.buying_price = 0
        self.minimum_trading_value_btc = 0.002


    def get_balance_alternative(self):
        result = k.get_account_balance()
        print(result)
        self.balance_symbol_crypto = self.trading_pair[:3]
        #self.balance_symbol_crypto = 'EOS'
        print(self.balance_symbol_crypto)
        self.balance_symbol_fiat_init = self.trading_pair[3:]  # symbol for Bitcoin - to get balance
#        self.balance_symbol_fiat = '{}'.format(self.balance_symbol_fiat_init)
        self.balance_symbol_fiat = '{}{}'.format('Z', self.balance_symbol_fiat_init)
        #self.balance_symbol_fiat = 'EUR'
        print(self.balance_symbol_fiat)
        self.balance_crypto = result.loc[self.balance_symbol_crypto]['vol']
        self.balance_fiat = result.loc[self.balance_symbol_fiat]['vol']


    def get_balance(self):
        result = k.get_account_balance()
        print(result)
        self.balance_symbol_crypto = self.trading_pair[:4]
        self.balance_symbol_fiat = self.trading_pair[4:]  # symbol for Bitcoin - to get balance
        self.balance_crypto = result.loc[self.balance_symbol_crypto]['vol']
        self.balance_fiat = result.loc[self.balance_symbol_fiat]['vol']


    def get_selling_price(self):
        ticker = k.get_ticker_information(self.trading_pair)
        self.selling_price = float(ticker['a'][0][0])


    def get_buying_price(self):
        ticker = k.get_ticker_information(self.trading_pair)
        self.buying_price = float(ticker['b'][0][0])


    def sell_market_order(self):
        self.get_balance()
        self.trading_volume = self.balance_crypto / self.sell_cycles
        while self.balance_crypto >= self.minimum_trading_value_btc:
            self.get_selling_price()
            try:
                order = k.add_standard_order(self.trading_pair, self.side, self.trade_type, self.trading_volume, self.selling_price, validate=False)
                txid = (order['txid'])
                print("Order placed - TXID: {}".format(txid))
                self.get_balance()
            except:
                print("Order could not be placed!")
            t.sleep(self.time_cycle)


    def sell_market_order_alternative(self):
        self.get_balance_alternative()
        self.trading_volume = self.balance_crypto / self.sell_cycles
        while self.balance_crypto >= self.minimum_trading_value_btc:
            self.get_selling_price()
            try:
                order = k.add_standard_order(self.trading_pair, self.side, self.trade_type, self.trading_volume, self.selling_price, validate=False)
                txid = (order['txid'])
                print("Order placed - TXID: {}".format(txid))
                self.get_balance_alternative()
            except:
                print("Order could not be placed!")
            t.sleep(self.time_cycle)


    def get_recent_trades(self, start, end):
        #trades = k.get_recent_trades(self.trading_pair)
        #trades = k.get_closed_orders(trades=True, start=start, end=end)
        trades = k.get_trades_history(start=start, end=end)
        return trades