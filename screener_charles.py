from bookkeeper_charles import API_KEYS
import pandas as pd
import os
import sys
import time
import requests, time, re, pickle
from finvizfinance.screener.overview import Overview
from progress.bar import Bar
from stock import Stock


url = 'https://api.tdameritrade.com/v1/instruments'

def screenFV():
    foverview = Overview()
    filters_dict = {'Price':'$5 to $20', '50-Day Simple Moving Average':'Price above SMA50', '200-Day Simple Moving Average':'SMA200 below SMA50', 'PEG':'Under 1', 'Current Volume':'Over 400K', 'Relative Volume':'Over 1'}
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.ScreenerView()
    return df


#DATA CONVERSION AND CALCULATIONS
def toStockDF(df, stock, index):
    df['Ticker'][index] = stock.ticker
    df['Company'][index] = stock.company
    df['Sector'][index] = stock.sector
    df['Industry'][index] = stock.industry
    df['Country'][index] = stock.country
    df['Close'][index] = stock.close
    df['Market Cap'][index] = stock.marketcap
    df['Volume'][index] = stock.vol
    df['Relative Volume'][index] = stock.rVol
    df['prev7DayHigh'][index] = stock.prevSevenDayHigh
    df['prev7DayLow'][index] = stock.prevSevenDayLow
    df['RSI(14)'][index] = stock.rsi14
    df['RSI(14)pctRank'][index] = stock.rsi14_pctRank
    df['RSI(2)'][index] = stock.rsi2
    df['ADX(5)'][index] = stock.adx5
    df['ATR'][index] = stock.atr
    df['Stop Loss'][index] = stock.sl
    df['PE'][index] = stock.pe
def toStockExcelData(df):
    bar = Bar('Converting into Data', max=len(df))
    cols = ['Ticker', 'Company', 'Sector', 'Industry', 'Country', 'Close', 'Market Cap', 'Volume', 'Relative Volume', 'prev7DayHigh',
            'prev7DayLow', 'RSI(14)','RSI(14)pctRank', 'RSI(2)','ADX(5)',
            'ATR', 'Stop Loss', 'PE']
    data = pd.DataFrame(columns=cols, index=range(0, len(df)))
    for x in range(0, len(df)):
        meta = df[0].iloc[x]
        toStockDF(data, meta, x)
        bar.next()
    bar.finish()
    return data  
def createStockData(df):
    bar = Bar('Creating Stocks', max=len(df))
    stocks = []
    for index, row in df.iterrows():
        stock = Stock(row['Ticker'])
        stock.pe = row['P/E']
        stock.company = row['Company']
        stock.sector = row['Sector']
        stock.industry = row['Industry']
        stock.country = row['Country']
        stock.marketcap = row['Market Cap']
        stock.getTechnicals()
        stocks.append(stock)
        bar.next()
    stockData = pd.DataFrame(stocks)
    writeStockFile(stockData)
    bar.finish()
    return stockData

def get_col_widths(dataframe):
    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
#File Management
def writeStockFile(data, file_name=re.sub('[ :]','_', time.asctime() + 'SCREEN_STOCKS.pkl')):
    if not os.path.isdir("OldStockData"):
        os.makedirs("OldStockData")
    with open('OldStockData/' + file_name, 'wb') as file:
        pickle.dump(data, file)
    return file_name
def writeStockExcel(data, file_name=re.sub('[ :]','_', time.asctime() + 'SCREEN_STOCKS.xlsx')):
    if not os.path.isdir("Screens"):
        os.makedirs("Screens")
    writer = pd.ExcelWriter('Screens/' + file_name, engine='xlsxwriter')
    data.to_excel(writer)
    worksheet = writer.sheets['Sheet1']
    for i, width in enumerate(get_col_widths(data)):
        worksheet.set_column(i, i, width)
    writer.save()
    return file_name

def get_col_widths(dataframe):
    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

def loadStockFile(file_name):
    with open('OldStockData/' + file_name, 'rb') as f:
        info = pickle.load(f)
    return info

# screening methods
def screen():
    df = screenFV()
    stocks_done = toStockExcelData(createStockData(df))
    excel_file = writeStockExcel(stocks_done)
    return stocks_done, excel_file