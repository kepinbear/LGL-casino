import sqlite3

#Instantiate sqlite file
con = sqlite3.connect("casino.sqlite")
cur = con.cursor()

def create_base_table():
    """Create database and base tables if they didn't exist."""
    cur.execute("CREATE TABLE IF NOT EXISTS tweet_log(date, tweet_id, ticker, votes)")
    cur.execute("CREATE TABLE IF NOT EXISTS trade_log(ticker, buy_ts, buy_order_id, buy_price, sell_ts, sell_order_id, sell_price)")
    
def insert_tweet_table(data):
    """Insert tweet information into tweets_log."""
    cur.execute("INSERT INTO tweet_log VALUES (?, ?, ?, ?)", data)
    con.commit()

def insert_trade_table(data):
    """Insert trade information into trade_log."""
    cur.execute("INSERT INTO trade_log VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()

def update_trade_table(data):
    """Update trade_log with sell information."""
    cur.execute("UPDATE trade_log SET sell_ts = ?, sell_order_id = ?, sell_price = ? WHERE buy_order_id = ?", data)
    con.commit()