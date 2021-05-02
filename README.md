# trader-charles

Trader Charles is an algorithmic trading bot, that manages a Paper Trading account using Alpaca API at 6pm EST everyday. He collects data from his trades and has his own REST API to query through his Postgres database of completed trades.

## Meet the Team
There are multiple versions of Charles that come together to help Charles trade.
 * **Screener Charles** - uses an unofficial FinViz API to screen stocks to provide a proper list of potential trades.
 * **Stanford Charles** - handles the numbers and calculates many popular trading indicators.
 * **Algo Charles** - checks if a stock has a good entry or exit price.
 * **Trader Charles** - uses the help of the other Charles' to manage his trading account.

## Technologies Used
Many of the libraries used in this project were standard. **numpy and pandas** were mainly used for the helper functions. **Alpaca API and finviz** helped when dealing with stocks and trading. I implemented **PostgresQL** as a database to hold metadata for the stocks he finalized a trade with. This helped me develop a Flask API to query through his most and least profitable trades and deploy it on Heroku. I used **memcache** to store updated data when needed. To visualize his account and trade data, I developed a web app using **React.js** and **Node.js**. I was able to visualize this data using **Chart.js** components. 

## Features
The order of operations for Charles is:
 > Check current positions to see if he should sell any. If he can, he will place 
sell orders. 

 > Once a trade is completed, he stores the metadata in a Postgres table

 > Get list of potential trades from Screener Charles.

 > Give list to Algo Charles to see if any of them are good to enter in a trade.

 > Check account buying power to see if he is able to place 10% in a trade. If he can, he will place buy orders for appropriate amount of shares.
 
 Charles is run through a Heroku scheduler add-on, this command also initiates cache load, where all endpoint responses are stored in memcache through another Heroku add-on.
 This helps reduce the query requests to the Postgres database and make response time faster for api requests to Charles.
 

## Roadmap
I have a lot of future plans for Charles, I would like to create an API around his trading account. I think a nice one page web app would be nice.

Feature | Progress |
:------------ | :-------------|
Implement Flask | ☑️ |
Integrate Database | ☑️ |
Design & Develop Frontend | ☑️ | 

### Current System Design
![image](https://user-images.githubusercontent.com/9872176/115946885-29e53600-a492-11eb-9331-5210a97ecdbd.png)
