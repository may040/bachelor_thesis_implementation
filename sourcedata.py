from metrics import *
from dpEvaluator import *
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from numpy import savetxt


# Problems:
# Google DP: saving sourcedata in file csv to evaluate it from command
# after this, reading file csv and evaluate it
# separate calculating and plotting from other

# Define properties of evaluation
dpEvaluator = DPEvaluator()
metricsSN = Metrics()
metricsIBM = Metrics()

epsilons = np.logspace(-3, 1, 500)
epsilon = 0.05
delta = 1.0e-16
sensitivity = 0.1

# Creating dataset from distribution
distribution = [4, 9, 10, 6, 6, 7, 8, 9, 8,
                7, 7, 6, 4.5, 3, 2, 1, 1.5, 0.5, 0.5]
weights = []
i = 0

for _ in range(0, 10):
    for x in range(0, 100):
        if (x % 5 == 0 and x != 0 and i != 18):
            i += 1
        weights.append(distribution[i])
    i = 0

weights = np.reshape(weights, (-1, 100))
sourceData = []
for index in range(0, 10):
    sourceData += random.choices(np.arange(0, 100),
                                 weights=weights[index], k=100)
sourceData = np.sort(sourceData).tolist()

# Creating neighboring datasets
d1=sourceData.copy()
randomAge=sourceData[random.randint(0,100)]
print(randomAge)
d2=sourceData.copy()
d2.remove(randomAge)

# Calculating mean of original data 
originalMean =[]
for i in range(0,1000):
    originalMean.append(np.mean(d1))


#Storing datasets
np.savetxt('sourcedata.csv', sourceData, delimiter=',',fmt='%1.0f', header='Age',comments='')
np.savetxt('originalMean.csv', originalMean, delimiter=',',fmt='%1.0f', header='Age',comments='')
np.savetxt('d1Data.csv', d1, delimiter=',',fmt='%1.0f', header='Age',comments='')
np.savetxt('d2Data.csv', d2, delimiter=',',fmt='%1.0f', header='Age',comments='')
print("FINISH")