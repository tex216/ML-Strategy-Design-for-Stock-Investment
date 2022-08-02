# ML Strategy Design for Stock Investment

Implemented two strategies and compare their performance. One strategy is a human-developed strategy, which is empirical-based. The another is a strategy learner, which will develop the trading rules using artificial intelligence (Details in https://lucylabs.gatech.edu/ml4t/fall2021/project-8/).

1. RTLearner.py

This file need not be run as it was designed to be imported in other files, it includes a `RTLearner Class` to train and query a Random Tree Learner 

2. BagLearner.py

This file need not be run as it was designed to be imported in other files, it includes a `BagLearner Class` to train and query with a learner ensemble.

3. ManualStrategy.py

This file need not be run as it was designed to be imported in other files, it includes a `ManualStrategy Class` that can learn a trading policy using the optimal manual strategy. Three indicators were used to evaluate the portfolio and benchmark performance both in sample and out of sample periods. Two comparison plots ('In_Sample.png', 'Out_Of_Sample.png') and a table ('table1.html') were generated in the final report.

4. StrategyLearner.py

This file need not be run as it was designed to be imported in other files, it includes a 'strategyLearner Class' that can learn a trading policy using the same three indicators used in ManualStrategy. An optimal trade dataframe was returned in the end.

5. indicators.py

This file need not be run as it was designed to be imported in other files, it contains the calculation method of three indicators to evaluate the portfolio performance in the report. 

6. experiment1.py

This file compares Manual Strategy with Strategy Learner in-sample trading JPM stocks. An relevant chart ('Experiment1.png') and table ('table2.html') was generated in the final report.

7. experiment2.py

This file conducts an experiment with StrategyLearner that shows how changing the value of impact should affect in-sample trading behavior. An relevant chart ('Experiment2.png') and table ('table3.html') was generated in the final report.

8. marketsimcode.py

This file need not be run as it was designed to be imported in other files, it accepts a "trades" DataFrame as input and provides portvalues as output.    

9. testproject.py

This file is considered the entry point to this project. All the 4 plots and 3 statistics tables for the report could be generated once running this file.

## How To Run:    
PYTHONPATH=../:. python testproject.py 
