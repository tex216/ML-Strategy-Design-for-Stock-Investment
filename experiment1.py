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
import pandas as pd
import numpy as np
import util as ut
import matplotlib.pyplot as plt
import datetime as dt

import StrategyLearner as sl
import ManualStrategy
import marketsimcode as msc
from pandas.plotting import register_matplotlib_converters


def author():
    return 'txue34'


def stats(portvals):
    daily_returns = (portvals / portvals.shift(1)) - 1
    dr = daily_returns[1:]
    cr = (portvals[-1] / portvals[0]) - 1  # cumulative return
    mdr = dr.mean()  # mean of daily return
    sddr = dr.std()  # stdev of daily return
    return cr, mdr, sddr

def table():
    symbol = ['JPM']
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    impact = 0.005
    commission = 9.95

    ms = ManualStrategy.ManualStrategy(symbol)
    df_trades = ms.testPolicy(symbol, sd, ed, sv)
    ms_portvals = msc.compute_portvals(df_trades, sv, 9.95, 0.005)
    ms_portvals = ms_portvals / ms_portvals.iloc[0]
    cr1, mdr1, sddr1 = stats(ms_portvals)

    bench_portvals = ms.benchmark(symbol, sd, ed, sv)
    bench_portvals = bench_portvals / bench_portvals.iloc[0]
    cr2, mdr2, sddr2 = stats(bench_portvals)

    learner = sl.StrategyLearner(verbose=False, impact=0.005)
    learner.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals = msc.compute_portvals(trades_df, sv, 9.95, 0.005)
    learner_portvals = learner_portvals / learner_portvals.iloc[0]
    cr3, mdr3, sddr3 = stats(learner_portvals)

    return cr1, cr2, cr3, mdr1, mdr2, mdr3, sddr1, sddr2, sddr3


def plots():
    register_matplotlib_converters()
    np.random.seed(903657846)
    symbol = ['JPM']
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    impact = 0.005
    commission = 9.95

    ms = ManualStrategy.ManualStrategy(symbol)
    df_trades = ms.testPolicy(symbol, sd, ed, sv)
    ms_portvals = msc.compute_portvals(df_trades, sv, 9.95, 0.005)
    ms_portvals = ms_portvals / ms_portvals.iloc[0]

    bench_portvals = ms.benchmark(symbol, sd, ed, sv)
    bench_portvals = bench_portvals / bench_portvals.iloc[0]

    learner = sl.StrategyLearner(verbose=False, impact=0.005)
    learner.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals = msc.compute_portvals(trades_df, sv, 9.95, 0.005)
    learner_portvals = learner_portvals / learner_portvals.iloc[0]

    plt.figure(figsize=(18, 9))
    plt.plot(ms_portvals, 'b', label='Manual Strategy')
    plt.plot(bench_portvals, 'g', label='Benchmark')
    plt.plot(learner_portvals, 'r', label='Strategy Learner')
    plt.xticks(rotation=13, fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=20)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Normalized Price', fontsize=20)
    plt.title('Normalized Value of Manual Strategy vs Benchmark vs Strategy Learner', fontsize=26)
    plt.savefig('Experiment1.png')
    plt.close()


if __name__ == "__main__":
    plots()
