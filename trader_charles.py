## MAIN DRIVER FILE
import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql.schema import ForeignKey
import alpaca_trade_api as tradeapi
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime as dt
from datetime import datetime
import time
import os


from dotenv import load_dotenv
load_dotenv()
from algo_charles import entry_algo, exit_algo
from screener_charles import screen, screenFV
from stock import Stock

Alpaca_ID = os.environ.get('Alpaca_ID')
Alpaca_Secret = os.environ.get('Alpaca_Secret')
api = tradeapi.REST(Alpaca_ID, Alpaca_Secret, "https://paper-api.alpaca.markets")
todayString = datetime.now().strftime('%Y-%m-%d')

#account management
Alpaca_Watchlist = os.environ.get('Alpaca_Watchlist')
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
    return api.get_watchlist(Alpaca_Watchlist)
def canTrade():
    if int(float(buying_power())) >= 300:
        return True
    else:
        return False

def updateAccountInfo():
    total = equity()
    power = buying_power()
    portfolio = positions()
    orders = api.list_orders()
    watchlist = api.get_watchlist(Alpaca_Watchlist)
    acc = Account.query.filter_by(date=todayString).first()
    if (acc is not None):
        Portfolio.query.filter_by(acc_id=todayString).delete()
        Orders.query.filter_by(acc_id=todayString).delete()
        Watchlist.query.filter_by(acc_id=todayString).delete()
        Account.query.filter_by(date=todayString).delete()
    for position in portfolio:
        pos = Portfolio(shares=position.qty, ticker=position.symbol, avg_entry=position.avg_entry_price, acc_id=todayString)
        db.session.add(pos)
    for order in orders:
        orde = Order(shares=order.qty, ticker=order.symbol, acc_id=todayString)
        db.session.add(orde)
    for x in watchlist.assets:
        wat = Watchlist(ticker=x['symbol'], acc_id=todayString)
        db.session.add(wat)
    acc = Account(date=todayString, equity=total, buying_power=power)
    db.session.add(acc)
    db.session.commit()
    


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


#trade management
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
    print("}----- Charles is now looking for entries -----{")
    buy_stocks = entry_algo(stocks)
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
#TODO CHECK IF THIS WORKS
def placeExits(df):
    acc = Account.query.filter_by(date=todayString).first()
    for x in df:
        submitOrder(x.shares, x.ticker, 'sell')
        if x.pl > 0:
            acc.wins = Account.wins + 1
        else:
            acc.losses = Account.losses + 1
        exitStock = Trades(date= todayString, ticker= x.ticker, company= x.company, sector= x.sector, industry= x.industry, country= x.country, exchange= x.exchange, close= x.close, shares= x.shares, entry_price= x.entry_price, cost_basis= x.cost_basis, marketvalue= x.marketvalue, pl= x.pl, plpc= x.plpc)
        db.session.add(exitStock)
    db.session.commit()
def runExits():
    print("}----- Charles is checking his positions -----{")
    sell_stocks = sortExits(positions())
    print("}----- Charles is placing sell orders -----{")
    if (len(sell_stocks) > 0):
        placeExits(sell_stocks)


#TODO: schedule this task
def login():
    runExits()
    runEntries()
    updateAccountInfo()

# API
Postgres_URI = os.environ.get('Postgres_URI')
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = Postgres_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Account(db.Model):
    __tablename__ = 'account'
    date = db.Column(db.String, primary_key=True)
    equity = db.Column(db.Float, nullable=False)
    wins = db.Column(db.Float, default=2)
    losses = db.Column(db.Float, default=1)
    buying_power = db.Column(db.Float, nullable=False)
    portfolio = db.relationship("Portfolio", backref='date', lazy=True)
    orders = db.relationship("Orders", backref='date', lazy=True)
    watchlist = db.relationship("Watchlist", backref='date', lazy=True)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'date'           : self.date,
           'equity'         : self.equity,
           'buying_power'   : self.buying_power,
           'win percentage' : round(float(self.wins / (self.wins + self.losses)), 2),
           'portfolio'      : self.serialize_portfolio(),
           'orders'         : self.serialize_orders(),
           'watchlist'      : self.serialize_watchlist()
       }
    def serialize_portfolio(self):
        return [item.serialize for item in self.portfolio]
    def serialize_orders(self):
        return [item.serialize for item in self.orders]
    def serialize_watchlist(self):
        return [item.serialize for item in self.watchlist]
    def __repr__(self):
        return '<User %r>' % self.username
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    shares = db.Column(db.Integer)
    ticker = db.Column(db.String, primary_key=True)
    avg_entry = db.Column(db.Float)
    acc_id = db.Column(db.String, ForeignKey('account.date'), primary_key=True)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'ticker'         : self.ticker,
           'shares'         : self.shares,
           'average entry'  : self.avg_entry
       }
class Orders(db.Model):
    __tablename__ = 'orders'
    shares = db.Column(db.Integer)
    ticker = db.Column(db.String, primary_key=True)
    acc_id = db.Column(db.String, ForeignKey('account.date'), primary_key=True)
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'ticker'         : self.ticker,
           'shares'         : self.shares,
       }
class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    ticker = db.Column(db.String, primary_key=True)
    acc_id = db.Column(db.String, ForeignKey('account.date'), primary_key=True)
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'ticker'         : self.ticker
       }

class Trades(db.Model):
    __tablename__ = 'trades'
    date = db.Column(db.String, primary_key=True, nullable=False)
    ticker = db.Column(db.String, primary_key=True, nullable=False)
    company = db.Column(db.String)
    sector = db.Column(db.String)
    industry = db.Column(db.String)
    country = db.Column(db.String)
    exchange = db.Column(db.String)
    close = db.Column(db.Float)
    shares = db.Column(db.Integer)
    entry_price = db.Column(db.Float)
    cost_basis = db.Column(db.Float)
    marketvalue = db.Column(db.Float)
    pl = db.Column(db.Float)
    plpc = db.Column(db.Float, nullable=True)
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'date'           : self.date,
           'ticker'         : self.ticker,
           'company'        : self.company,
           'sector'         : self.sector,
           'industry'       : self.industry,
           'country'        : self.country,
           'exchange'       : self.exchange,
           'close'          : self.close,
           'shares'         : self.shares,
           'entry_price'    : self.entry_price,
           'cost_basis'     : self.cost_basis,
           'marketvalue'    : self.marketvalue,
           'pl'             : self.pl,
           'plpc'           : self.plpc
       }

def init_db():
    db.create_all()
    updateAccountInfo()


#To reduce traffic into postgres. 
#TODO: IDEA: Schedule an update database task every 10/15/30 mins and hold query inside a local variable
#            return that local variable for endpoints.

## ENDPOINTS
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
@app.route('/', methods=['GET'])
def home():
    return '''<h1>This is Trader Charles' API</h1>
    <p>A prototype API for Charles' paper trading account.</p> '''
#TODO: implement websocket for stream directly from API
@app.route('/account', methods=['GET'])
def account():
    charles = Account.query.filter_by(date=todayString).first()
    return jsonify(charles.serialize)
@app.route('/account/history', methods=['GET'])
def account_history():
    history = [i.serialize for i in Account.query.all()]
    return jsonify(history)
@app.route('/trades', methods=['GET'])
def trades_history():
    history = [i.serialize for i in Trades.query.all()]
    return jsonify(history)
@app.route('/today', methods=['GET'])
def today():
    return todayString

if __name__ == "__main__":
    init_db()
    app.run()
