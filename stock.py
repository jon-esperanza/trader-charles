import pandas_datareader as pdr
import datetime as dt
from stanford_charles import adx, relative_volume, rsi_pctRank, rsi14, rsi2, atr, rsi2, day_high, day_low, moving_average


class Stock(object):
    def __init__(self, ticker):
        #overview
        self.ticker = ticker
        self.company = ""
        self.sector = ""
        self.industry = ""
        self.country = ""
        self.close = 0
        self.exchange = 0
        #trade vals - post position close
        self.shares = 0
        self.entry_price = 0
        self.cost_basis = 0
        self.marketvalue = 0
        self.pl = 0
        self.plpc = 0
        #fundamentals
        self.pe = 0
        self.marketcap = 0
        #technical
        self.prevSevenDayHigh = 0
        self.prevSevenDayLow = 0
        self.vol = 0
        self.rVol = 0
        self.rsi14 = 0
        self.rsi2 = 0
        self.adx5 = 0
        self.rsi14_pctRank = 0
        self.atr = 0
        self.sl = 0
    def getTechnicals(self):
        now = dt.datetime.now()
        start = dt.datetime(now.year - 1, now.month, now.day)
        df = round(pdr.get_data_yahoo(self.ticker, start, now), 3)
        
        self.close = df['Close'][len(df) - 1]
        df_noToday = df[:-1]
        self.prevSevenDayLow = day_low(df_noToday)
        self.prevSevenDayHigh = day_high(df_noToday)
        self.rsi14 = rsi14(df)
        df['RSI14'] = self.rsi14
        self.rsi14_pctRank = rsi_pctRank(df, 14, 63)
        self.rsi14 = self.rsi14[len(df) - 1]
        self.rsi2 = rsi2(df)[len(df)-1]
        self.atr = atr(df, 14)[len(df) - 1]
        self.adx5 = adx(df, 5)[len(df) - 1]
        self.sl = 2 * (atr(df, 20)[len(df) - 1])
        self.vol = df['Volume'][len(df) - 1]
        self.rVol = relative_volume(df)
        self.stoploss = (self.close - self.sl)
    def __str__(self):
        return '{} Close:{} Volume:{}'.format(self.ticker, self.close, self.vol)