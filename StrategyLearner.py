""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Teng Xue (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: txue34 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903657846 (replace with your GT ID)  			  	   		   	 		  		  		    	 		 		   		 		  
"""

import datetime as dt
import random
import numpy as np
import pandas as pd
import util as ut

import RTLearner as rt
import BagLearner as bl
from indicators import *
import ManualStrategy as ms
import marketsimcode as msc

np.random.seed(903657846)

class StrategyLearner(object):
    """
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output.
    :type verbose: bool
    :param impact: The market impact of each transaction, defaults to 0.0
    :type impact: float
    :param commission: The commission amount charged, defaults to 0.0
    :type commission: float
    """

    # constructor
    def __init__(self, verbose=False, impact=0.005, commission=9.95):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=20, boost=False, verbose=False)

    def author(self):
        return 'txue34'

    def add_evidence(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        """
        Trains your strategy learner over a given time frame.
        """
        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        normed_prices = prices / prices.iloc[0]

        # Get all indicators, moving_window = 20 days
        sma, sma_ratio = getSMA(normed_prices, 20)
        upper_band, lower_band, bbp = getBBP(normed_prices, 20)
        momentum = getMOM(normed_prices, 20)

        # Lookback windows = 10 days, BUY/SELL threshold = 0.015
        x_train = pd.concat((sma_ratio, bbp, momentum), axis=1)
        x_train.fillna(0, inplace=True)
        x_train = x_train[:-10].values

        threshold = (normed_prices.values[10:] / normed_prices.values[:-10]) - 1
        buy_signal = (threshold > 0.015 + self.impact).astype(int)
        sell_signal = (threshold < -0.015 - self.impact).astype(int)
        y_train = np.array(buy_signal - sell_signal)
        self.learner.add_evidence(x_train, y_train)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol="JPM", sd=dt.datetime(2009, 1, 1), ed=dt.datetime(2010, 12, 31), sv=100000):
        """
        Tests your learner using data outside of the training data
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating
                 a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.
                 Values of +2000 and -2000 for trades are also legal when switching from long to short or short to
                 long so long as net holdings are constrained to -1000, 0, and 1000.
        :rtype: pandas.DataFrame
        """
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)
        prices = prices_all[syms]
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        normed_prices = prices / prices.iloc[0]

        # Get all indicators, moving_window = 20 days
        sma, sma_ratio = getSMA(normed_prices, 20)
        upper_band, lower_band, bbp = getBBP(normed_prices, 20)
        momentum = getMOM(normed_prices, 20)

        x_test = pd.concat((sma_ratio, bbp, momentum), axis=1)
        x_test.fillna(0, inplace=True)
        x_test = x_test.values
        # Query learner
        y_test = self.learner.query(x_test)
        df_trades = pd.DataFrame(index=normed_prices.index, columns=['Symbol', 'Order', 'Shares'])
        df_trades['Symbol'] = 'JPM'
        df_trades['Order'] = np.NaN
        df_trades['Shares'] = 1000
        holdings = 0
        for i in range(0, y_test.shape[0] - 1):
            # compare with price in tomorrow
            if normed_prices.iloc[i + 1, 0] > normed_prices.iloc[i, 0] and holdings <= 0:
                df_trades.iloc[i, 1] = 'BUY'
                holdings += 1000
            elif normed_prices.iloc[i + 1, 0] < normed_prices.iloc[i, 0] and holdings >= 0:
                df_trades.iloc[i, 1] = 'SELL'
                holdings -= 1000
        df_trades.dropna(inplace=True)
        return df_trades


if __name__ == "__main__":
    print("One does not simply think up a strategy")
