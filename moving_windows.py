from pandas_datareader import data as pdr
import datetime
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

yf.pdr_override()

aapl = pdr.get_data_yahoo('AAPL', start=datetime.datetime(2016, 10, 1), end=datetime.datetime(2022, 1, 1))
# aapl = data.DataReader('AAPL', 'yahoo', start=datetime.datetime(2016, 10, 1), end=datetime.datetime(2022, 1, 1))
aapl.to_csv('data/aapl_ohlc.csv')

df = pd.read_csv('data/aapl_ohlc.csv', header=0, index_col='Date', parse_dates=True)

# Isolate the adjusted closing prices
adj_close_px = df['Adj Close']

# Calculate the moving average
moving_avg = adj_close_px.rolling(window=40).mean()

# Inspect the result
# print(moving_avg[-10:])

# Short moving window rolling mean
df['42'] = adj_close_px.rolling(window=40).mean()

# Long moving window rolling mean
df['252'] = adj_close_px.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means
df[['Adj Close', '42', '252']].plot()

plt.show()
