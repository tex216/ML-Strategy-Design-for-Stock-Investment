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
import pandas as pd
import util as ut
import numpy as np
import matplotlib.pyplot as plt

from indicators import *
import marketsimcode as msc
from pandas.plotting import register_matplotlib_converters


class ManualStrategy(object):
    # constructor
    def __init__(self, symbol, verbose=False, impact=0.005, commission=9.95):
        """
        Constructor method
        """
        self.symbol = symbol
        self.verbose = verbose
        self.impact = impact
        self.commission = commission

    def author(self):
        return 'txue34'

    def testPolicy(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = get_data(symbol, dates)  # automatically adds SPY
        prices = prices_all[symbol]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        normed_prices = prices / prices.iloc[0]
        holdings = 0
        # Get all indicators, moving_window = 20 days
        sma, sma_ratio = getSMA(normed_prices, 20)
        upper_band, lower_band, bbp = getBBP(normed_prices, 20)
        momentum = getMOM(normed_prices, 20)
        # build the "trades" data frame
        df_trades = pd.DataFrame(index=normed_prices.index, columns=['Symbol', 'Order', 'Shares'])
        df_trades['Symbol'] = 'JPM'
        df_trades['Order'] = np.NaN
        df_trades['Shares'] = 1000
        for i in range(0, df_trades.shape[0] - 1):
            # compare with price in tomorrow
            if holdings <= 0 and (sma_ratio.iloc[i, 0] < 0.6 or bbp.iloc[i, 0] < 0.2 or momentum.iloc[i, 0] < -0.2):
                df_trades.iloc[i, 1] = 'BUY'
                holdings += 1000
            elif holdings >= 0 and (sma_ratio.iloc[i, 0] > 1.4 or bbp.iloc[i, 0] > 0.8 or momentum.iloc[i, 0] > 0.2):
                df_trades.iloc[i, 1] = 'SELL'
                holdings -= 1000
        df_trades.dropna(inplace=True)
        return df_trades

    def benchmark(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        # Starting with $100,000 cash, investing in 1000 shares of JPM, and holding that position.
        df_benchmark = self.testPolicy(symbol, sd, ed, sv)
        df_benchmark.iloc[0, 1] = 'BUY'
        for i in range(1, df_benchmark.shape[0] - 1):
            df_benchmark.iloc[i, 1] = np.NaN
        df_benchmark.dropna(inplace=True)
        bench_portvals = msc.compute_portvals(df_benchmark, 100000, 9.95, 0.005)
        return bench_portvals

    def stats(self, portvals):
        daily_returns = (portvals / portvals.shift(1)) - 1
        dr = daily_returns[1:]
        cr = (portvals[-1] / portvals[0]) - 1  # cumulative return
        mdr = dr.mean()  # mean of daily return
        sddr = dr.std()  # stdev of daily return
        return cr, mdr, sddr

    def table(self):
        symbol = ['JPM']
        start_val = 100000
        # In Sample Period
        df_trades1 = self.testPolicy(symbol, dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), start_val)
        portvals1 = msc.compute_portvals(df_trades1, start_val, 9.95, 0.005)
        portvals1 = portvals1 / portvals1.iloc[0]
        cr1, mdr1, sddr1 = self.stats(portvals1)
        bench_portvals1 = self.benchmark(symbol, dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), start_val)
        bench_portvals1 = bench_portvals1 / bench_portvals1.iloc[0]
        cr2, mdr2, sddr2 = self.stats(bench_portvals1)
        # Out of Sample Period
        df_trades2 = self.testPolicy(symbol, dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), start_val)
        portvals2 = msc.compute_portvals(df_trades2, start_val, 9.95, 0.005)
        portvals2 = portvals2 / portvals2.iloc[0]
        cr3, mdr3, sddr3 = self.stats(portvals2)
        bench_portvals2 = self.benchmark(symbol, dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31), start_val)
        bench_portvals2 = bench_portvals2 / bench_portvals2.iloc[0]
        cr4, mdr4, sddr4 = self.stats(bench_portvals2)
        return cr1, cr2, cr3, cr4, mdr1, mdr2, mdr3, mdr4, sddr1, sddr2, sddr3, sddr4

    # Compare the performance of Manual Strategy versus the benchmark for the in-sample and out-of-sample time periods.
    def PlotInSample(self):  # In-Sample period
        register_matplotlib_converters()
        symbol = ['JPM']
        start_date = dt.datetime(2008, 1, 1)
        end_date = dt.datetime(2009, 12, 31)
        start_val = 100000
        df_trades = self.testPolicy(symbol, start_date, end_date, start_val)
        portvals = msc.compute_portvals(df_trades, start_val, 9.95, 0.005)
        portvals = portvals / portvals.iloc[0]

        bench_portvals = self.benchmark(symbol, start_date, end_date, start_val)
        bench_portvals = bench_portvals / bench_portvals.iloc[0]

        fig, ax = plt.subplots(figsize=(18, 9))
        plt.plot(portvals, 'r', label="Manual Strategy")
        plt.plot(bench_portvals, 'g', label="Benchmark")
        plt.title("Manual Strategy vs. Benchmark: In-Sample", fontsize=26)
        plt.xlabel("Date", fontsize=20)
        plt.xticks(rotation=13, fontsize=18)
        plt.ylabel("Normalized Portfolio Value", fontsize=20)
        plt.yticks(fontsize=18)

        for index, item in df_trades.iterrows():
            if item['Order'] == 'SELL':
                plt.axvline(index, color='b', linestyle='--', label="LONG")
            elif item['Order'] == 'BUY':
                plt.axvline(index, color='k', linestyle='--', label="SHORT")
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        plt.legend(handle_list, label_list, fontsize=18)
        plt.savefig('In_Sample.png')
        plt.close()

    def PlotOutOfSample(self):  # Out-Of-Sample period
        register_matplotlib_converters()
        symbol = ['JPM']
        start_date = dt.datetime(2010, 1, 1)
        end_date = dt.datetime(2011, 12, 31)
        start_val = 100000
        df_trades = self.testPolicy(symbol, start_date, end_date, start_val)
        portvals = msc.compute_portvals(df_trades, start_val, 9.95, 0.005)
        portvals = portvals / portvals.iloc[0]

        bench_portvals = self.benchmark(symbol, start_date, end_date, start_val)
        bench_portvals = bench_portvals / bench_portvals.iloc[0]

        fig, ax = plt.subplots(figsize=(18, 9))
        plt.plot(portvals, 'r', label="Manual Strategy")
        plt.plot(bench_portvals, 'g', label="Benchmark")
        plt.title("Manual Strategy vs. Benchmark: Out-Of-Sample", fontsize=26)
        plt.xlabel("Date", fontsize=20)
        plt.xticks(rotation=13, fontsize=18)
        plt.ylabel("Normalized Portfolio Value", fontsize=20)
        plt.yticks(fontsize=18)

        for index, item in df_trades.iterrows():
            if item['Order'] == 'SELL':
                plt.axvline(index, color='b', linestyle='--', label="LONG")
            elif item['Order'] == 'BUY':
                plt.axvline(index, color='k', linestyle='--', label="SHORT")
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        plt.legend(handle_list, label_list, fontsize=18)
        plt.savefig('Out_Of_Sample.png')
        plt.close()


if __name__ == "__main__":
    print("One does not simply think up a strategy")

