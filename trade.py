from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import *
import time

#Instantiates Alpaca client
trading_client = TradingClient(ALP_API_KEY, ALP_SECRET_KEY, paper=True)

def buy(top_pick):
    """Buy top pick at market open."""
    buy_order = MarketOrderRequest(
                        symbol=top_pick,
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.GTC
                    )
    submit_buy = trading_client.submit_order(buy_order)
    buy_order_id = str(submit_buy.id)
    return buy_order_id

def sell(top_pick):
    """Sell top pick at market close."""
    sell_order = MarketOrderRequest(
                        symbol=top_pick,
                        qty=1,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.GTC
                    )
    submit_sell = trading_client.submit_order(sell_order)
    sell_order_id = str(submit_sell.id)
    return sell_order_id

def get_buy_filled_price(buy_order_id):
    """Get fill price for buy order."""
    buy_price = trading_client.get_order_by_id(buy_order_id).filled_avg_price
    return buy_price

def get_sell_filled_price(sell_order_id):
    """Get sell price for sell order."""
    sell_price = trading_client.get_order_by_id(sell_order_id).filled_avg_price
    return sell_price

def get_buy_timestamp(buy_order_id):
    """Get time buy order was filled at."""
    buy_time = trading_client.get_order_by_id(buy_order_id).filled_at
    return buy_time

def get_sell_timestamp(sell_order_id):
    """Get time sell order was filled at."""
    sell_time = trading_client.get_order_by_id(sell_order_id).filled_at
    return sell_time

def get_time_to_next_open():
    """Calculate time to next market open."""
    market = trading_client.get_clock()
    time_to_open = round((market.next_open - market.timestamp).total_seconds())
    return time_to_open

def get_time_to_next_close():
    """Calculate time to next market close."""
    market = trading_client.get_clock()
    time_to_close = round((market.next_close - market.timestamp).total_seconds())
    return time_to_close

def check_if_tradable(symbol):
        return trading_client.get_asset(symbol).tradable