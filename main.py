from datetime import date
from db import *
from twitter import *
from trade import *
from config import *

#Pick random stock at 6:00AM, send tweet, and stores it in tweet_data
daily_tweet = send_tweet()
#Wait 3 hours until end of poll.
time.sleep(10800)

#Grab results of poll after it's completed and selects highest voted ticker
poll_results = retrieve_poll(daily_tweet)
daily_pick, num_votes = choose_top_pick(poll_results)

# Creates tables if they don't exist and inserts ticker into tweets table
create_base_table()
tweet_row = [date.today(), daily_tweet, daily_pick, num_votes]
insert_tweets_table(tweet_row)

#Wait until market is open
market = trading_client.get_clock()
open_time = get_time_to_next_open()
time.sleep(open_time)

if market.is_open:
    #Buy daily pick 
    buy_order_id = buy(daily_pick)
    buy_price = get_buy_filled_price(buy_order_id)
    buy_time = get_buy_filled_price(buy_order_id)

    #Fill in buy information for the trade_log table
    trade_row = [daily_pick, buy_time, buy_order_id, buy_price, 'NULL', 'NULL', 'NULL']
    insert_trade_table(trade_row)

    #Wait until 5 minutes before close.
    close_time = get_time_to_next_close() - 300
    time.sleep(close_time)

    #Sell daily pick at end of day.
    sell_order_id = sell(daily_pick)
    sell_price = get_sell_filled_price(sell_order_id)
    sell_time = get_sell_timestamp(sell_order_id)

    #Update row with sell information
    sell_row = [sell_time, sell_order_id, sell_price, buy_order_id]
    update_trade_table(sell_row)