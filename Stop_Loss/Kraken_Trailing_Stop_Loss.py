#https://github.com/ericsomdahl/python-bittrex
import Stop_Loss.Kraken_Trailing_Stop_Loss_Support as bt
import time as t

bit = bt.Kraken_Trailing_Stop_Loss()

bit.trading_pair = 'XXLMZEUR'              #trading pair
bit.side = "sell"
bit.trade_type = "market"                    #change this to "market" if you need to sell quickly - careful, you will be a market taker!
bit.sell_cycles = 10                       #max packet size
bit.time_cycle = 10                         #time interval between order placements
bit.increment = 0.00000001                  #smallest price increment
bit.minimum_remaining_balance = 0           #min imum remaining balance of above symbol after trades are completed
bit.minimum_btc_balance = 0.0000            #minimum level for Bitcoin
bit.trailing_stop_loss_percentage = 0.98
bit.trailing_stop_loss_fixed_value = 0.000002


bit.get_balance_alternative()
print("Initial {} balance: {}".format(bit.balance_symbol_crypto,bit.balance_crypto))
print("Initial {} balance: {}".format(bit.balance_symbol_fiat, bit.balance_fiat))

bit.get_selling_price()
if bit.selling_price >= bit.peak_value:
    bit.peak_value = bit.selling_price
bit.stop_loss_exit_level = bit.peak_value * bit.trailing_stop_loss_percentage

while bit.selling_price >= bit.stop_loss_exit_level:
    if bit.selling_price >= bit.peak_value:
        bit.peak_value = bit.selling_price
    bit.stop_loss_exit_level = bit.peak_value * bit.trailing_stop_loss_percentage
    print("****** Current Bid Price: {} ******** Current Peak Value: {} ********* Current Stop Loss Level: {}".format(bit.selling_price, bit.peak_value, bit.stop_loss_exit_level ))
    bit.get_selling_price()
    t.sleep(5)
print("Stop Loss Level reached with bid price {} to trailing stop loss level: {} - Sell Started!".format(bit.selling_price, bit.stop_loss_exit_level))
bit.sell_market_order_alternative()
