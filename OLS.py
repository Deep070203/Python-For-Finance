# Ordinary Least-Squares Regression (OLS)

# Import the `api` model of `statsmodels` under alias `sm`
import statsmodels.api as sm
from pandas import tseries
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
# Isolate the adjusted closing price
all_adj_close = all_data[['Adj Close']]

# Calculate the returns
all_returns = np.log(all_adj_close / all_adj_close.shift(1))

# Isolate the AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')

# Isolate the MSFT returns
msft_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker')

# Build up a new DataFrame with AAPL and MSFT returns
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']

# Add a constant
X = sm.add_constant(return_data['AAPL'])

# Construct the model
model = sm.OLS(return_data['MSFT'],X).fit()

# Print the summary
# print(model.summary())

"""
plt.plot(return_data['AAPL'], return_data['MSFT'], 'r.')
ax = plt.axis()
x = np.linspace(ax[0], ax[1] + 0.01)

plt.plot(x, model.params[0] + model.params[1] * x, 'b', lw=2)

plt.grid(True)
plt.axis('tight')
plt.xlabel('Apple Returns')
plt.ylabel('Microsoft returns')
"""

return_data['MSFT'].rolling(window=252).corr(return_data['AAPL']).plot()
plt.show()
