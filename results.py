from config import *
from trade import *
from twitter import *
from db import *
from os import getcwd

db = getcwd() + '\\' + 'casino.sqlite'
print('Starting results.py')
#At the end of the day, retrieve stocks selected earlier.
stocks = retrieve_stock_table(db)

#Retrieve daily performance of stocks
daily_pnl = retrieve_stock_performance(stocks)

#Generate text for tweet.
text = generate_performance_text(daily_pnl)

#Send tweet.
end_tweet = send_results_tweet(text)
print(end_tweet)
print('Done')