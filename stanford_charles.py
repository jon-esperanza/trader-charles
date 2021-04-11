import numpy as np


def wwma(values, n):
    """
     J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=2/(n+1), min_periods=n, adjust=False).mean()
def ema(values, n):
    """
     EMA 
    """
    return values.ewm(alpha=1/n, min_periods=n, adjust=False).mean()

def atr(df, n=14):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return round(atr, 2)

def adx(df, n=14):
    data = df.copy()
    data['atr'] = atr(df, n)
    data['Up Move'] = np.nan
    data['Down Move'] = np.nan
    data['PDM'] = np.nan
    data['NDM'] = np.nan
    data['PDI'] = np.nan
    data['EMAP'] = np.nan
    data['NDI'] = np.nan
    data['EMAN'] = np.nan
    data['PMINUSN'] = np.nan
    data['PPLUSN'] = np.nan
    data['EMAPMINUSN'] = np.nan
    data['ADX'] = np.nan
    # find +di and -di
    for x in range(1, len(data)):
        data['Up Move'][x] = 0
        data['Down Move'][x] = 0

        data['Up Move'][x] = data['High'][x] - data['High'][x-1]  
        data['Down Move'][x] = data['Low'][x-1] - data['Low'][x]

        if data['Up Move'][x] > 0 and data['Up Move'][x] > data['Down Move'][x]:
            data['PDM'][x] = data['Up Move'][x]
        else:
            data['PDM'][x] = 0
        if data['Down Move'][x] > 0 and data['Down Move'][x] > data['Up Move'][x]:
            data['NDM'][x] = data['Down Move'][x]
        else:
            data['NDM'][x] = 0

    data['EMAP'] = ema(data['PDM'], n)
    data['EMAN'] = ema(data['NDM'], n)
    data['PDI'] = (data['EMAP'] / data['atr'])
    data['NDI'] = (data['EMAN'] / data['atr'])
    data['PMINUSN'] = abs(data['PDI'] - data['NDI'])
    data['PPLUSN'] = abs(data['PDI'] + data['NDI'])
    dx = ((data['PMINUSN'])/(data['PPLUSN'])) * 100
    data['ADX'] = ema(dx, n)
    return round(data['ADX'], 2)
    

def day_low(df, days=5):
    low = 9223372036854775807
    data = df.tail(days)
    for x in range(0, len(data)):
        if (data['Low'][x] < low):
            low = data['Low'][x]
    return round(low, 3)
    
def day_high(df, days=5):
    high = -1
    data = df.tail(days)
    for x in range(0, len(data)):
        if (data['Close'][x] > high):
            high = data['Close'][x]
    return round(high, 3)

def moving_average(df, col, n=200):
    data = df[col].rolling(n, center=False).mean()
    return round(data[len(df) - 1], 2)

def average_volume(df):
    average = moving_average(df, 'Volume', 57)
    return average

def relative_volume(df):
    data = df.copy()
    average = average_volume(data)
    rel_average = data['Volume'][len(df)-1] / average
    return round(rel_average, 2)


def rsi14(df):
    #14_Day RSI
    data = df.copy()
    data['Up Move'] = np.nan
    data['Down Move'] = np.nan
    data['Average Up'] = np.nan
    data['Average Down'] = np.nan

    #Relative Strength
    data['RS'] = np.nan
    #Relative Strength Index
    data['RSI'] = np.nan

    #Calculate 'Up Move' & 'Down Move'
    for x in range(0, len(data)):
        data['Up Move'][x] = 0
        data['Down Move'][x] = 0
        
        if data['Adj Close'][x] > data['Adj Close'][x-1]:
            data['Up Move'][x] = data['Adj Close'][x] - data['Adj Close'][x-1]
            
        if data['Adj Close'][x] < data['Adj Close'][x-1]:
            data['Down Move'][x] = abs(data['Adj Close'][x] - data['Adj Close'][x-1])

    ## Calculate initial Average Up & Down, RS and RSI
    data['Average Up'][14] = data['Up Move'][1:15].mean()
    data['Average Down'][14] = data['Down Move'][1:15].mean()
    data['RS'][14] = data['Average Up'][14] / data['Average Down'][14]
    data['RSI'][14] = 100 - (100/(1+data['RS'][14]))  

    ## Calculate rest of Average Up, Average Down, RS, RSI
    for x in range(15, len(data)):
        data['Average Up'][x] = (data['Average Up'][x-1]*13+data['Up Move'][x])/14
        data['Average Down'][x] = (data['Average Down'][x-1]*13+data['Down Move'][x])/14
        data['RS'][x] = data['Average Up'][x] / data['Average Down'][x]
        data['RSI'][x] = 100 - (100/(1+data['RS'][x]))

    return round(data['RSI'], 2)
def rsi2(df):
    #2_Day RSI
    data = df.copy()
    data['Up Move'] = np.nan
    data['Down Move'] = np.nan
    data['Average Up'] = np.nan
    data['Average Down'] = np.nan

    #Relative Strength
    data['RS'] = np.nan
    #Relative Strength Index
    data['RSI'] = np.nan

    #Calculate 'Up Move' & 'Down Move'
    for x in range(0, len(data)):
        data['Up Move'][x] = 0
        data['Down Move'][x] = 0
        
        if data['Adj Close'][x] > data['Adj Close'][x-1]:
            data['Up Move'][x] = data['Adj Close'][x] - data['Adj Close'][x-1]
            
        if data['Adj Close'][x] < data['Adj Close'][x-1]:
            data['Down Move'][x] = abs(data['Adj Close'][x] - data['Adj Close'][x-1])

    ## Calculate initial Average Up & Down, RS and RSI
    data['Average Up'][2] = data['Up Move'][1:3].mean()
    data['Average Down'][2] = data['Down Move'][1:3].mean()
    data['RS'][2] = data['Average Up'][2] / data['Average Down'][2]
    data['RSI'][2] = 100 - (100/(1+data['RS'][2]))  

    ## Calculate rest of Average Up, Average Down, RS, RSI
    for x in range(3, len(data)):
        data['Average Up'][x] = (data['Average Up'][x-1]*1+data['Up Move'][x])/2
        data['Average Down'][x] = (data['Average Down'][x-1]*1+data['Down Move'][x])/2
        data['RS'][x] = data['Average Up'][x] / data['Average Down'][x]
        data['RSI'][x] = 100 - (100/(1+data['RS'][x]))

    return round(data['RSI'], 2)

def rsi_pctRank(df, period=14, days=63):
    data = df.copy()
    count = 0
    data = data.tail(days)
    for x in range(0, days):
        if (data['RSI'+str(period)][x] < data['RSI'+str(period)][days - 1]):
            count += 1
    pctRank = count / days
    return round(pctRank, 2)