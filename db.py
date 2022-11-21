import sqlite3

def create_base_table(db):
    """Create database and base tables if they didn't exist."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tweet_log(date, tweet_id, ticker, votes)")
    cur.execute("CREATE TABLE IF NOT EXISTS trade_log(ticker, buy_ts, buy_order_id, buy_price, sell_ts, sell_order_id, sell_price)")
    cur.execute("CREATE TABLE IF NOT EXISTS daily_stocks(ticker1, ticker2, ticker3, ticker4)")
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

def insert_stocks_table(db, data):
    """Insert tweet information into daily_stocks."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("INSERT INTO daily_stocks VALUES (?, ?, ?, ?)", data)
    con.commit()
    con.close()

def update_trade_table(db, data):
    """Update trade_log with sell information."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("UPDATE trade_log SET sell_ts = ?, sell_order_id = ?, sell_price = ? WHERE buy_order_id = ?", data)
    con.commit()
    con.close()

def retrieve_stock_table(db):
    """Retrieve latest row from daily_stocks and returns a list."""
    con = sqlite3.connect(db)
    cur = con.cursor()
    stocks = cur.execute("SELECT * FROM daily_stocks ORDER BY rowid DESC LIMIT 1;").fetchone()
    con.close()
    return list(stocks)