import numpy as np


arr = [[2, 5 ,3],[2,7,9],[-2,9,1]]
#arr = {'2','5','3','2','7','9','-2','9','1','4'}
arr2 = (arr == 1)
print(arr2)
mySum = np.sum(arr, axis = 0)
print(mySum)