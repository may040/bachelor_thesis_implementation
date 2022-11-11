#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from diffprivlib import tools as dp
from timeit import default_timer as timer
from metrics import *
from dpEvaluator import *
d1Data = []
d2Data = []
originalMean = []

# Reading source data for evaluation
# d1Data
f = open(r'd1Data.csv', newline='')
reader = csv.reader(f)
next(reader, None)
d1Data = (np.concatenate(list(reader)).ravel()).astype(np.float)

# d2Data
f = open(r'd2Data.csv', newline='')
reader = csv.reader(f)
next(reader, None)
d2Data = (np.concatenate(list(reader)).ravel()).astype(np.float)

# originalMean
f = open(r'originalMean.csv', newline='')
reader = csv.reader(f)
next(reader, None)
originalMean = (np.concatenate(list(reader)).ravel()).astype(np.float)

epsilons = [0.5, 1.0, 1.5, 3.0, 5.0]

i = 0
# IBM: Execute dp algortihm MEAN on datasets 1000 times
ibmDPMeans1 = [[], [], [], [], []]
ibmDPMeans2 = [[], [], [], [], []]

for e in epsilons:
    for _ in range(0, 1000):
        ibmDPMeans1[i].append(
            float(dp.mean(d1Data, e, (min(d1Data), max(d1Data)))))
        ibmDPMeans2[i].append(
            float(dp.mean(d2Data, e, (min(d2Data), max(d2Data)))))
    i += 1

# Calculate metrics for IBM
# Define properties of evaluation
dpEvaluator = DPEvaluator()
metricsIBM = [Metrics() for _ in range(0, 5)]

for i in range(0, 5):
    metricsIBM[i].wasserstein_distance = dpEvaluator.wasserstein_distance(
        np.asfarray(ibmDPMeans1[i]), np.asfarray(ibmDPMeans2[i]))
    metricsIBM[i].mse = dpEvaluator.mse(np.asfarray(
        ibmDPMeans1[i]), np.asfarray(originalMean))
    metricsIBM[i].std = dpEvaluator.std(np.asfarray(ibmDPMeans1[i]))
    metricsIBM[i].msd = dpEvaluator.msd(np.asfarray(
        originalMean), np.asfarray(ibmDPMeans1[i]))

    d1hist, d2hist, bin_edges = dpEvaluator._generate_histogram_neighbors(
        ibmDPMeans1[i], ibmDPMeans2[i])
    statified, _, _, _, _ = dpEvaluator._dp_test(d1hist, d2hist, bin_edges, len(
        ibmDPMeans1[i]), len(ibmDPMeans2[i]), epsilons[i])
    metricsIBM[i].dp_res = statified

attr_names = dir(metricsIBM[0])[-5:]

members = [attr for attr in dir(metricsIBM[0]) if not callable(
    getattr(metricsIBM[0], attr)) and not attr.startswith("__")]
members.remove('wasserstein_distance')
members.insert(1, 'wasserstein_distance')
members.remove('mse')
members.insert(2, 'mse')
members.remove('std')
members.insert(3, 'std')

file_exists_result = os.path.isfile('ibmMetrics.csv')
with open('ibmMetrics.csv', 'a+', newline='') as csvfile:
    fieldnames = ['epsilon'] + members
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists_result:
        writer.writeheader()
    for i in range(0, 5):
        values = [getattr(metricsIBM[i], member) for member in members]
        writer.writerow({'epsilon': epsilons[i], members[0]: values[0], members[1]: values[1],
                        members[2]: values[2], members[3]:values[3], members[4]: values[4]})

        
print("FINISH")
