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
WORKING WITH PANDAS
"""

print(df.head())


# Inspect the index
df.index

# Inspect the columns
df.columns

# Select only the last 10 observations of `Close`
ts = df['Close'][-10:]

# Check the type of `ts`
type(ts)

# Inspect the first rows of November-December 2006
print(df.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].head())

# Inspect the first rows of 2007
print(df.loc['2007'].head())

# Inspect November 2006
print(df.iloc[22:43])

# Inspect the 'Open' and 'Close' values at 2006-11-01 and 2006-12-01
print(df.iloc[[22,43], [0, 3]])

# Sample 20 rows
sample = df.sample(20)

# Print `sample`
print(sample)

# Resample to monthly level
monthly_df = df.resample('M')

# Print `monthly_df'
print(monthly_df)

df.asfreq("M", method="bfill")

# Add a column `diff` to `aapl` 
df['diff'] = df.Open - df.Close

# Delete the new `diff` column
del df['diff']


df['Close'].plot(grid=True)
plt.show()


"""
COMMON FINANCIAL ANALYSIS

Returns = returns.py
"""





