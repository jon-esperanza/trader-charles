from trader_charles import db


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
    
    def __init__(self, date, equity, wins, losses, buying_power, portfolio, orders, watchlist):
        self.date = date
        self.equity = equity
        self.wins = wins
        self.losses = losses
        self.buying_power = buying_power
        self.portfolio = portfolio
        self.orders = orders
        self.watchlist = watchlist
    
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
    acc_id = db.Column(db.Integer, ForeignKey('account.date'), primary_key=True)
    
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
    acc_id = db.Column(db.Integer, ForeignKey('account.date'), primary_key=True)
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'ticker'         : self.ticker,
           'shares'         : self.shares,
           'average entry'  : self.avg_entry
       }
class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    ticker = db.Column(db.String, primary_key=True)
    acc_id = db.Column(db.Integer, ForeignKey('account.date'), primary_key=True)
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'ticker'         : self.ticker
       }