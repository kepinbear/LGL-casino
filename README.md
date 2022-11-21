"# LGL-casino" 

LGL-casino is a bot that makes trades based off of the results of a Twitter poll.

"## Process Flow"
1. Send a tweet with 4 random tickers at 6:00AM.
2. Wait 3 hours and find the ticker with the highest number of votes.
3. Record the tweet and winner into a table called tweet_log.
4. Buy a share of the winner at 9:30AM.
5. Record buy order, buy price, and buy time into a table called trade_log.
6. Sell share at 3:55PM.
7. Record sell order, sell price, and sell time into trade_log.
8. Calculate PnL for random tickers at the end of the day.
9. Send tweet with PnL for tickers.
10. Celebrate??