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
from datetime import datetime, timezone
import time
import os
from os.path import join, dirname


from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
from algo_charles import entry_algo, exit_algo
from screener_charles import screen, screenFV
from stock import Stock

Alpaca_ID = os.getenv('Alpaca_ID')
Alpaca_Secret = os.getenv('Alpaca_Secret')
api = tradeapi.REST(os.getenv('Alpaca_ID'), os.getenv('Alpaca_Secret'), "https://paper-api.alpaca.markets")
todayString = datetime.now(timezone.est).strftime('%Y-%m-%d')

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


# API
Postgres_URI = os.environ.get('Postgres_URI')
app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = Postgres_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def login():
    runExits()
    runEntries()

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

## ENDPOINTS
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
@app.route('/', methods=['GET'])
def home():
    return '''<h1>This is Trader Charles' API</h1>
    <p>A prototype API for Charles' paper trading account.</p> '''
#TODO: implement websocket for stream directly from API
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
