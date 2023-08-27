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

# Initialize the short and long windows
short_window = 5
long_window = 44

# Initialize the signals Dataframe with 'signal' column
signals = pd.DataFrame(index=df.index)
signals['signal'] = 0.0

# Create short SMA over short window
signals['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long SMA over long window
signals['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

# Generate Trading orders
signals['positions'] = signals['signal'].diff()

# Set the initial capital
initial_capital = float(100000.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions['AAPL'] = 100 * signals['signal']

# Initialize the portfolio with value owned
portfolio = positions.multiply(df['Adj Close'], axis=0)

# Store the difference in shares owned
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(df['Adj Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(df['Adj Close'], axis=0)).sum(axis=1).cumsum()

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

"""
Sharpe Ratio
"""

# Isolate the returns of your strategy
returns = portfolio['returns']

# annualized Sharpe ratio
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

# Print the Sharpe ratio
# print(sharpe_ratio)

"""
Maximum Drawdown
"""
# Define a trailing 252 trading day window
window = 252

# Calculate the max drawdown in the past window days for each day
rolling_max = df['Adj Close'].rolling(window, min_periods=1).max()
daily_drawdown = df['Adj Close']/rolling_max - 1.0

# Calculate the minimum (negative) daily drawdown
max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

# Plot the results
daily_drawdown.plot()
max_daily_drawdown.plot()

# Show the plot
# plt.show()

"""
Compound Annual Growth Rate
"""
# Get the number of days in `aapl`
days = (aapl.index[-1] - aapl.index[0]).days

# Calculate the CAGR
cagr = ((((aapl['Adj Close'][-1]) / aapl['Adj Close'][1])) ** (365.0/days)) - 1

# Print CAGR
print(cagr)
