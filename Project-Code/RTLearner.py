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
import random


class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return "txue34"

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner
        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self.build_tree(data)

    def build_tree(self, data):
        # build and save the tree: X_train, Y_train
        data_y = data[:, -1]
        if data.shape[0] <= self.leaf_size or len(data.shape) == 1:  # only 1 row
            return np.array([['leaf', np.mean(data_y), -1, -1]])
        elif np.all(data_y == data[0, -1]):  # all elements in Y are same
            # return [leaf,	data.y,	NA,	NA]
            return np.array([['leaf', data[0, -1], -1, -1]])
        else:
            # A	Cutler Decision Tree Algorithm:
            # determine random feature 'i' to split on
            best_i = random.randint(0, data.shape[1] - 2)
            splitVal = np.median(data[:, best_i], axis=0)
            if splitVal == max(data[:, best_i]):
                return np.array([['leaf', np.mean(data_y), -1, -1]])

            leftTree = self.build_tree(data[data[:, best_i] <= splitVal])
            rightTree = self.build_tree(data[data[:, best_i] > splitVal])
            root = np.array([[best_i, splitVal, 1, leftTree.shape[0] + 1]])
            decision_tree = np.vstack((np.vstack((root, leftTree)), rightTree))
            return decision_tree

    def query(self, points):
        """
        Estimate a set of test points given the tree we built.
        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained tree
        :rtype: numpy.ndarray
        """
        # Given points as X_test, return results as Y_test
        results = []
        root = self.tree
        for i in range(points.shape[0]):
            node = 0
            while root[node, 0] != 'leaf':
                index = root[node, 0]
                splitVal = root[node, 1]
                if points[i, int(float(index))] <= float(splitVal):
                    left = int(float(root[node, 2]))
                    node = node + left
                else:
                    right = int(float(root[node, 3]))
                    node = node + right
            result = root[node, 1]
            results.append(float(result))
        return np.array(results)


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
