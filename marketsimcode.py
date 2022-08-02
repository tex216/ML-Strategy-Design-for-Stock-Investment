""""""
"""MC2-P1: Market simulator.  		  	   		   	 		  		  		    	 		 		   		 		  

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
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data


def author():
    return 'txue34'


def compute_portvals(df_trades, start_val=100000, commission=0, impact=0):
    orders = df_trades
    orders.sort_index(inplace=True)

    stocks = list(orders.Symbol.unique())
    start_date = orders.index.min()
    end_date = orders.index.max()
    market_dates = pd.date_range(start_date, end_date)
    # build the "prices" data frame
    df_prices = get_data(stocks, market_dates)
    df_prices["Cash"] = 1
    df_prices = df_prices.drop("SPY", axis=1)
    # build the "holdings" data frame
    df_holdings = df_prices * 0
    df_holdings["Cash"] = 0
    df_holdings.iloc[0, -1] = start_val

    for index, row in orders.iterrows():
        stock = row["Symbol"]
        order = row["Order"]
        shares = row["Shares"]
        price = df_prices.loc[index, stock]
        if order == "BUY":
            df_holdings.loc[index, stock] += shares
            df_holdings.loc[index, "Cash"] -= shares * price
        else:
            df_holdings.loc[index, stock] -= shares
            df_holdings.loc[index, "Cash"] += shares * price
        # calculate transaction costs: Commissions and Market Impact
        df_holdings.loc[index, 'Cash'] -= commission + impact * shares * price

    # update the "holdings" data frame day by day
    for i in range(1, df_holdings.shape[0]):
        df_holdings.iloc[i] += df_holdings.iloc[i - 1]
    # build the final "values" data frame: values = prices * holdings
    df_values = df_prices * df_holdings
    portvals = df_values.sum(axis=1)
    return portvals