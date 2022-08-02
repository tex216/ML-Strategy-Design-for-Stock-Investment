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
    commission = 0.00

    # impact = 0.00
    learner = sl.StrategyLearner(verbose=False, impact=0)
    learner.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals = msc.compute_portvals(trades_df, sv, 0, 0)
    learner_portvals = learner_portvals / learner_portvals.iloc[0]
    cr1, mdr1, sddr1 = stats(learner_portvals)
    # impact = 0.005
    learner0 = sl.StrategyLearner(verbose=False, impact=0)
    learner0.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df0 = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals0 = msc.compute_portvals(trades_df0, sv, 0, 0.005)
    learner_portvals0 = learner_portvals0 / learner_portvals0.iloc[0]
    cr2, mdr2, sddr2 = stats(learner_portvals0)
    # impact = 0.01
    learner1 = sl.StrategyLearner(verbose=False, impact=0.01)
    learner1.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df1 = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals1 = msc.compute_portvals(trades_df1, sv, 0, 0.01)
    learner_portvals1 = learner_portvals1 / learner_portvals1.iloc[0]
    cr3, mdr3, sddr3 = stats(learner_portvals1)

    return cr1, cr2, cr3, mdr1, mdr2, mdr3, sddr1, sddr2, sddr3


def plots():
    register_matplotlib_converters()
    np.random.seed(903657846)
    symbol = ['JPM']
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    commission = 0.00

    # impact = 0.00
    learner = sl.StrategyLearner(verbose=False, impact=0)
    learner.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals = msc.compute_portvals(trades_df, sv, 0, 0)
    learner_portvals = learner_portvals / learner_portvals.iloc[0]
    # impact = 0.005
    learner0 = sl.StrategyLearner(verbose=False, impact=0)
    learner0.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df0 = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals0 = msc.compute_portvals(trades_df0, sv, 0, 0.005)
    learner_portvals0 = learner_portvals0 / learner_portvals0.iloc[0]
    # impact = 0.01
    learner1 = sl.StrategyLearner(verbose=False, impact=0.01)
    learner1.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
    trades_df1 = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    learner_portvals1 = msc.compute_portvals(trades_df1, sv, 0, 0.01)
    learner_portvals1 = learner_portvals1 / learner_portvals1.iloc[0]

    plt.figure(figsize=(18, 9))
    plt.plot(learner_portvals, 'r', label='Impact Value = $0.00')
    plt.plot(learner_portvals0, 'g', label='Impact Value = $0.005')
    plt.plot(learner_portvals1, 'b', label='Impact Value = $0.01')
    plt.xticks(rotation=13, fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=20)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Normalized Price', fontsize=20)
    plt.title('Strategy Learner with Different Impact Values', fontsize=26)
    plt.savefig('Experiment2.png')
    plt.close()



if __name__ == "__main__":
    plots()
