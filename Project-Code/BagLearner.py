""""""
"""  		  	   		     		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
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
"""

import numpy as np
# import DTLearner as dt
# import RTLearner as rt
# import LinRegLearner as lrl		  	   		     		  		  		    	 		 		   		 		  

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return "txue34"

    def add_evidence(self, data_x, data_y):
        rows = data_x.shape[0]
        for learner in self.learners:
            # select random indices
            i = np.random.choice(rows, size=rows)
            # select random entries
            learner.add_evidence(data_x[i], data_y[i])

    def query(self, points):
        results = []
        for learner in self.learners:
            result = learner.query(points)
            results.append(result)
        # calculate the average from each learner
        results = np.mean(np.array(results), axis=0)
        return results

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
