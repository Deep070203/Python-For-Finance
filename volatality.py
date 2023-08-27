from pandas_datareader import data as pdr
import datetime
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

yf.pdr_override()

def get(tickers, startdate, enddate):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=startdate, end=enddate)
    datas = map (data, tickers)
    return pd.concat(datas, keys=tickers, names=['Ticker', 'Date'])


tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
all_data = get(tickers, datetime.datetime(2016, 10, 1), datetime.datetime(2022, 1, 1))
# print(all_data.head())

daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')

# Calculate the daily percentage change for `daily_close_px`
daily_pct_change = daily_close_px.pct_change()
# Define the minumum of periods to consider
min_periods = 75

# Calculate the volatility
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

# Plot the volatility
vol.plot(figsize=(10, 8))

# Show the plot
plt.show()
