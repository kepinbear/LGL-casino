from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from config import *
import datetime

#Instantiates Alpaca client
trading_client = TradingClient(ALP_API_KEY, ALP_SECRET_KEY, paper=True)
historical_client = StockHistoricalDataClient(ALP_API_KEY, ALP_SECRET_KEY)

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
    """Checks if an asset is tradable at Alpaca."""
    return trading_client.get_asset(symbol).tradable

def retrieve_stock_performance(stocks):
    """Retrieve performance of the list of stocks generated for the poll and returns a dictionary."""
    start = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
    request_params = StockBarsRequest(
                        symbol_or_symbols=stocks,
                        timeframe=TimeFrame.Day,
                        start=start,
                        feed='iex'
                        )
    performance = historical_client.get_stock_bars(request_params)
    #Calculates difference between open and close prices from stock bars; Stores in dictionary.
    daily_pnl = {}
    for stock in stocks:
        pnl = round(performance[stock][0].open - performance[stock][0].close, 2)
        daily_pnl[stock] = pnl
    return daily_pnl

def generate_performance_text(daily_pnl):
    """Generates the text for the results tweet at end of market day."""
    text = 'How did we do #LGL?' + '\n\n' + "Today's choices:" + '\n'
    for stock in daily_pnl:
        text += f"#{stock}: {daily_pnl[stock]}"
        if daily_pnl[stock] > 0:
            text += '\U0001f7e9' + '\n'
        if daily_pnl[stock] < 0: 
            text += '\U0001f7e5' + '\n'
    return text