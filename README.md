# trader-charles

Trader Charles is an algorithmic trading bot, that manages a Paper Trading account using Alpaca API.

## Meet the Team
There are multiple versions of Charles that come together to help Charles trade.
 * **Screener Charles** - uses an unofficial FinViz API to screen stocks to provide a proper list of potential trades.
 * **Stanford Charles** - handles the numbers and calculates many popular trading indicators.
 * **Algo Charles** - checks if a stock has a good entry or exit price.
 * **Trader Charles** - uses the help of the other Charles' to manage his trading account.

## Technologies Used
Many of the libraries used in this project were standard. **numpy, pandas, and pickle** were mainly used for the helper functions. **Alpaca API and finviz** helped when dealing with stocks and trading.

## Features
The order of operations for Charles is:
 > Check current positions to see if he should sell any. If he can, he will place 
sell orders.

 > Get list of potential trades from Screener Charles.

 > Give list to Algo Charles to see if any of them are good to enter in a trade.

 > Check account buying power to see if he is able to place 10% in a trade. If he can, he will place buy orders for appropriate amount of shares.
## Roadmap
I have a lot of future plans for Charles, I would like to create an API around his trading account. I think a nice one page web app would be nice.

Feature | Progress |
:------------ | :-------------|
Implement Flask | :white_large_square: |
Integrate Database | :white_large_square: |
Design & Develop Frontend | :white_large_square: | 
