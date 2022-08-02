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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import ManualStrategy
import experiment1 as e1
import experiment2 as e2


def author():
    return 'txue34'


def results():
    np.random.seed(903657846)
    ms = ManualStrategy.ManualStrategy(symbol='JPM')
    ms.PlotInSample()
    ms.PlotOutOfSample()
    e1.plots()
    e2.plots()

    cr1, cr2, cr3, cr4, mdr1, mdr2, mdr3, mdr4, sddr1, sddr2, sddr3, sddr4 = ms.table()
    table1 = pd.DataFrame({'Manual Strategy (In-Sample)': [cr1, mdr1, sddr1],
                           'Benchmark (In-Sample)': [cr2, mdr2, sddr2],
                           'Manual Strategy (Out-of-Sample)': [cr3, mdr3, sddr3],
                           'Benchmark (Out-of-Sample)': [cr4, mdr4, sddr4]},
                          index=['Cumulative Return', 'Mean of Daily Returns', 'STDEV of Daily Returns'])
    table1.to_html('table1.html')

    cr5, cr6, cr7, mdr5, mdr6, mdr7, sddr5, sddr6, sddr7 = e1.table()
    table2 = pd.DataFrame({'Manual Strategy': [cr5, mdr5, sddr5], 'Benchmark': [cr6, mdr6, sddr6],
                           'Strategy Learner': [cr7, mdr7, sddr7]},
                          index=['Cumulative Return', 'Mean of Daily Returns', 'STDEV of Daily Returns'])
    table2.to_html('table2.html')

    cr8, cr9, cr10, mdr8, mdr9, mdr10, sddr8, sddr9, sddr10 = e2.table()
    table3 = pd.DataFrame({'Impact Value of $0.00': [cr8, mdr8, sddr8], 'Impact Value of $0.005': [cr9, mdr9, sddr9],
                           'Impact Value of $0.01': [cr10, mdr10, sddr10]},
                          index=['Cumulative Return', 'Mean of Daily Returns', 'STDEV of Daily Returns'])
    table3.to_html('table3.html')


if __name__ == "__main__":
    results()
