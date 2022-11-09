import pandas as pd
import tweepy
from config import *

#Creates Twitter session
client = tweepy.Client(
    consumer_key=TWT_API_KEY,
    consumer_secret=TWT_API_SECRET_KEY,
    access_token=TWT_ACCESS_TOKEN,
    access_token_secret=TWT_ACCESS_TOKEN_SECRET
)

def pick_random_stocks():
    """Pick 4 random stocks from spreadsheet as a list."""
    csvfile = pd.read_csv("D:\Documents\projects\casino\sp500_companies.csv", header=0).sample(n=4)
    stocks = csvfile['Symbol'].values.tolist()
    return stocks

# def pick_one_stock():
#     csvfile = pd.read_csv("D:\Documents\projects\casino\sp500_companies.csv", header=0).sample(n=1)
#     replacement = ''.join(csvfile['Symbol'])
#     return replacement

# def check_valid_poll(poll):
#     """Performs a check on randomly generated stocks, replaces stock with new one until all are True."""
#     #Create check to grab index of untradeable stock
#     check = [check_if_tradable(item) for item in poll]
#     #Keep changing stock until all are True
#     while all(check) != True:
#         i = check.index(False)
#         poll[i] = pick_one_stock()
#         check = [check_if_tradable(item) for item in poll]
#     return poll

def send_tweet():
    """Send tweet using 4 random stocks and return id of that tweet."""
    poll_choices = pick_random_stocks()
    tweet = client.create_tweet(poll_options = poll_choices, poll_duration_minutes=180, text="Which one moons today? 🚀")
    tweet_id = tweet.data['id']
    return tweet_id

def retrieve_poll(tweet_id):
    """Gets poll information using tweet_id"""
    results = client.get_tweet(tweet_id, expansions=['attachments.poll_ids'], user_auth=True)
    poll_data = results.includes['polls'][0]['options']
    return poll_data

def choose_top_pick(poll_data):
    """Loops through poll_data and selects one with highest votes. Stores in tuple."""
    top_pick = ""
    top_votes = 0
    for i in range(len(poll_data)):
        if poll_data[i]['votes'] > top_votes:
            top_pick = poll_data[i]['label']
            top_votes = poll_data[i]['votes']
    return top_pick, top_votes