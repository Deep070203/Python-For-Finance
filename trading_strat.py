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

# Initialize the plot figure
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, ylabel='Price in $')

# Plot the closing price
df['Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index,
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='m')

# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index,
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Show the plot
plt.show()

