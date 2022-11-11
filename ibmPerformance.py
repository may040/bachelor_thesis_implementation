#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import numpy as np
import matplotlib.pyplot as plt
from diffprivlib import tools as dp
from timeit import default_timer as timer

d1Data=[]
d2Data=[]

#Reading source data for evaluation
#d1Data
f= open(r'd1Data.csv', newline='')
reader = csv.reader(f)
next(reader, None)
d1Data = (np.concatenate(list(reader)).ravel()).astype(np.float)

#d2Data
f= open(r'd2Data.csv', newline='')
reader = csv.reader(f)
next(reader, None)
d2Data = (np.concatenate(list(reader)).ravel()).astype(np.float)

#epsilons = [0.5,1.0,1.5,3.0,5.0]
epsilons = [1,2,3,4,5]

i=0
#IBM: Execute dp algortihm on datasets 1000 times
ibmEv1 = [[],[],[],[],[]]
ibmEv2 = [[],[],[],[],[]]
executionTime =list()
for n in range(0,1000):
    start = timer()
    for e in epsilons:
        for _ in range(0,1000):
            ibmEv1[i].append(dp.mean(d1Data,e,(min(d1Data),max(d1Data))))
            ibmEv2[i].append(dp.mean(d2Data,e,(min(d2Data),max(d2Data))))
        i+=1
    end = timer()
    if n == 999:
        continue
    for s in range(0,5):
        ibmEv1[s].clear()
        ibmEv2[s].clear()
    i=0
    executionTime.append(end-start)
    print(end-start)
print("FINISH")
np.savetxt('ibmPerformance.csv', executionTime,  fmt='%.8f',delimiter=',', header='IBM Performance Times',comments='')
# %%
