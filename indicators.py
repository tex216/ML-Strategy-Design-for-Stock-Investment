import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data
from pandas.plotting import register_matplotlib_converters


def author():
    return 'txue34'


# Indicator 1 - Simple Moving Average
def getSMA(prices, moving_window):
    sma = prices.rolling(window=moving_window).mean()
    sma.bfill()
    sma_ratio = prices / sma
    return sma, sma_ratio


# Indicator 2 - Bollinger Bands Percentage
def getBBP(prices, moving_window):
    sma = prices.rolling(window=moving_window).mean()
    sma.bfill()
    rolling_std = prices.rolling(window=moving_window).std()
    rolling_std.bfill()
    upper_band = sma + (2 * rolling_std)
    lower_band = sma - (2 * rolling_std)
    bbp = (prices - lower_band) / (upper_band - lower_band)
    return upper_band, lower_band, bbp


# Indicator 3 - Momentum
def getMOM(prices, moving_window):
    momentum = prices / prices.shift(moving_window) - 1
    momentum.bfill()
    return momentum


if __name__ == "__main__":
    print('txue34')
