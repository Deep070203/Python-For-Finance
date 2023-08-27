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

"""
# Assign `Adj Close` to `daily_close`
daily_close = df[['Adj Close']]

# Daily returns
daily_pct_c = daily_close.pct_change()

# Replace NA values with 0
daily_pct_c.fillna(0, inplace=True)

# Inspect daily returns
# print(daily_pct_c)

# Daily log returns
daily_log_returns = np.log(daily_close.pct_change()+1)

# Print daily log returns
# print(daily_log_returns)


# Resample `aapl` to business months, take last observation as value
monthly = aapl.resample('BM').apply(lambda x: x[-1])

# Calculate the monthly percentage change
# print(monthly.pct_change())

# Resample `aapl` to quarters, take the mean as value per quarter
quarter = aapl.resample("4M").mean()

# Calculate the quarterly percentage change
# print(quarter.pct_change())

daily_pct_c = daily_close / daily_close.shift(1) - 1

# Print `daily_pct_c`
# print(daily_pct_c)

# Plot the distribution of `daily_pct_c`
daily_pct_c.hist(bins=50)

# Show the plot
# plt.show()

# Pull up summary statistics
# print(daily_pct_c.describe())

# Calculate the cumulative daily returns
cum_daily_return = (1 + daily_pct_c).cumprod()

# Print `cum_daily_return`
# print(cum_daily_return)

# Plot the cumulative daily returns
cum_daily_return.plot(figsize=(12, 8))

# show the plot
# plt.show()

# Resample the cumulative daily return to cumulative monthly return
cum_monthly_return = cum_daily_return.resample("M").mean()

# Print the `cum_monthly_return`
print(cum_monthly_return)
"""


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

# Plot the distributions
daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

# Show the resulting plot
# plt.show()


# Plot a scatter matrix with the `daily_pct_change` data
pd.plotting.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))

# Show the plot
plt.show()
