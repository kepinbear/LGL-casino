from datetime import date
import time
from os import getcwd
from db import *
from twitter import *
from trade import *
from config import *

csv = getcwd() + '\\' + 'sp500_companies.csv'
db = getcwd() + '\\' + 'casino.sqlite'
#Creates base tables
create_base_table(db)

#Pick random stocks at 6:00AM and sends tweet.
stocks = pick_random_stocks(csv)
daily_tweet = send_start_tweet(stocks)

#Inserts stocks into stock_table
insert_stocks_table(db, stocks)

#Wait 3 hours until end of poll.
time.sleep(10800)

#Grab results of poll after it's completed and selects highest voted stock
poll_results = retrieve_poll(daily_tweet)
daily_pick, num_votes = choose_top_pick(poll_results)

#Inserts chosen stocks into tweets table
tweet_row = [date.today(), daily_tweet, daily_pick, num_votes]
insert_tweet_table(db, tweet_row)

#Wait until market is open
open_time = get_time_to_next_open()
time.sleep(open_time)

#Buy daily pick 
buy_order_id = buy(daily_pick)
time.sleep(5)
buy_price = get_buy_filled_price(buy_order_id)
buy_time = get_buy_timestamp(buy_order_id)

#Fill in buy information for the trade_log table
trade_row = [daily_pick, buy_time, buy_order_id, buy_price, 'NULL', 'NULL', 'NULL']
insert_trade_table(db, trade_row)

#Wait until 5 minutes before close.
close_time = get_time_to_next_close()
time.sleep(close_time - 300)

#Sell daily pick at end of day.
sell_order_id = sell(daily_pick)
time.sleep(5)
sell_price = get_sell_filled_price(sell_order_id)
sell_time = get_sell_timestamp(sell_order_id)

#Update row with sell information
sell_row = [sell_time, sell_order_id, sell_price, buy_order_id]
update_trade_table(db, sell_row)