from stanford_charles import day_high
import alpaca_trade_api as tradeapi
import sys
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime as dt
import time



from bookkeeper_charles import API_KEYS
from algo_charles import entry_algo, exit_algo
from screener_charles import screen, screenFV
from stock import Stock

api = tradeapi.REST(API_KEYS.Alpaca_ID.value, API_KEYS.Alpaca_Secret.value, "https://paper-api.alpaca.markets")

def getFakePositions():
    tickers = ['ALTA','AAP','ABC', 'ALTG', 'NUZE', 'BLPH', 'TSLA']
    closes = []
    highs = []
    now = dt.datetime.now()
    start = dt.datetime(now.year - 1, now.month, now.day)
            
    for x in tickers:
        df = round(pdr.get_data_yahoo(x, start, now), 3)
        df_noToday = df[:-1]
        day = day_high(df_noToday)
        closes.append(df['Close'][len(df) - 1])
        highs.append(day)

    positions = {'Ticker': tickers,
                'Close': closes,
                'prev7DayHigh': highs}

    positions_df = pd.DataFrame(positions)
    return positions_df

#account management

def equity():
    return api.get_account().equity
def last_equity():
    return api.get_account().last_equity
def buying_power():
    return api.get_account().buying_power
def positions():
    return api.list_positions()
def orders():
    return api.list_orders()
def watchlist():
    return api.get_watchlist("756988e8-7ef9-4e09-9fb0-8c6e2bd275f7")
def canTrade():
    if int(float(buying_power())) >= 300:
        return True
    else:
        return False

def getAccountInfo():
    portfolio = positions()
    orders = api.list_orders()
    watchlist = api.get_watchlist("756988e8-7ef9-4e09-9fb0-8c6e2bd275f7")
    print("Charles' Account:")
    print("   $" + equity() + " Equity")
    print("   $" + buying_power() + " Buying Power")
    print("   Portfolio:")
    for position in portfolio:
        print("      >" + str(position.qty) + " shares of " + str(position.symbol) + " at " + str(position.avg_entry_price))
    print("   Pending Orders:")
    for order in orders:
        print("      > " + str(order.qty) + " shares of $" + str(order.symbol))
    print("   Watchlist:")
    for x in watchlist.assets:
        print ("      > $" + str(x['symbol']))


#market management
def isOpen():
    return api.get_clock().is_open

def minUntilOpen():
    clock = api.get_clock()
    openingTime = clock.next_open.replace(tzinfo=dt.timezone.utc).timestamp()
    currTime = clock.timestamp.replace(tzinfo=dt.timezone.utc).timestamp()
    timeToOpen = int((openingTime - currTime) / 60)
    if (timeToOpen > 0):
        print(str(timeToOpen) + " minutes til market open.")
    else:
        print("Market is currently open")
    return timeToOpen

def awaitNextLogin(done):
    while (done == True):
        if (minUntilOpen() == 888):
            print("Charles is logging on...")
            done = False
            break
        print(str(minUntilOpen()) + " minutes til market open.")
        time.sleep(60)


#trade
def submitOrder(qty, stock, side):
    resp = False
    if (qty > 0):
        try:
            api.submit_order(stock, qty, side, 'market', 'day')
            print("///!! Market order of | " + str(qty) + " " + stock + " " + side.upper() + " | submitted.")
            resp = True
        except:
            print("///!! Order of | " + str(qty) + " " + stock + " " + side.upper() + " | did not go through.")
            resp = False
    else:
        print("Quantity is 0, order of | " + str(qty) + " " + stock.upper() + " " + side + " | not completed.") 
        resp = False
    return resp
def sortEntries(df):
    cols = ['Ticker', 'Desired Shares']
    data = pd.DataFrame(columns=cols, index=range(0,len(df)))
    x = 0
    amount = int(float(buying_power()))
    while (x < len(df)):
        if (amount >= 300):
            ten_pct = amount / 10
            data['Desired Shares'][x] = round(ten_pct / df['Close'][x], None)
            data['Ticker'][x] = df['Ticker'][x]
            amount = amount - (data['Desired Shares'][x] * df['Close'][x])
        else:
            api.add_to_watchlist(watchlist().id, df['Ticker'][x])
        x += 1
    
    return data.dropna()

def placeEntries(df):
    if canTrade():
        for x in range(0, len(df)):
            ticker = df['Ticker'][x]
            qty = df['Desired Shares'][x]
            submitOrder(qty, ticker, 'buy')
    else:
        print("Charles is broke. $" + buying_power)

def runEntries():
    print("}----- Charles is looking for good plays -----{")
    stocks, excel_file = screen()
    print("/// Found plays")
    print("}----- Charles is now looking for entries -----{")
    buy_stocks = entry_algo(stocks)
    print("/// Found good entry stocks")
    print("}----- Charles is checking if he can trade -----{")
    can_buy = sortEntries(buy_stocks)
    print("}----- Charles is placing buy orders -----{")
    placeEntries(can_buy)

def sortExits(df):
    stocks = []
    for position in df:
        stock = Stock(position.symbol)
        stock.getTechnicals()
        stock.exchange = position.exchange
        stock.marketvalue = int(float(position.market_value))
        stock.cost_basis = int(float(position.cost_basis))
        stock.entry_price = int(float(position.avg_entry_price))
        stock.shares = int(float(position.qty))
        stock.pl = int(float(position.unrealized_pl))
        stock.plpc = int(float(position.unrealized_plpc))
        stocks.append(stock)
    sell_stocks = exit_algo(stocks)
    return sell_stocks

def placeExits(df):
    for x in df:
        submitOrder(x.shares, x.ticker, 'sell')
"""         if x.pl > 0:
            win += 1
        else:
            loss += 1 """

def runExits():
    print("}----- Charles is checking his positions -----{")
    sell_stocks = sortExits(positions())
    print("}----- Charles is placing sell orders -----{")
    if (len(sell_stocks) > 0):
        placeExits(sell_stocks)

def run():
    print()
    getAccountInfo()
    print()
    runExits()
    runEntries()
    print()
    getAccountInfo()

run()

