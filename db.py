import sqlite3

def create_base_table(db):
    """Create database and base tables if they didn't exist."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tweet_log(date, tweet_id, ticker, votes)")
    cur.execute("CREATE TABLE IF NOT EXISTS trade_log(ticker, buy_ts, buy_order_id, buy_price, sell_ts, sell_order_id, sell_price)")
    con.close()
    
def insert_tweet_table(db, data):
    """Insert tweet information into tweet_log."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("INSERT INTO tweet_log VALUES (?, ?, ?, ?)", data)
    con.commit()
    con.close()

def insert_trade_table(db, data):
    """Insert trade information into trade_log."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("INSERT INTO trade_log VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()
    con.close()

def update_trade_table(db, data):
    """Update trade_log with sell information."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("UPDATE trade_log SET sell_ts = ?, sell_order_id = ?, sell_price = ? WHERE buy_order_id = ?", data)
    con.commit()
    con.close()