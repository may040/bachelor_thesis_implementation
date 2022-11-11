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
googleDpMeans1 = [[], [], [], [], []]
googleDpMeans2 = [[], [], [], [], []]

# Reading source data for evaluation
# d1Data
f = open(r'dpMeans1.csv', newline='')
lis = [float(line.strip("\r\n")) for line in f if not "epsilon" in line]     
googleDpMeans1[0]= lis[0:1000]
googleDpMeans1[1]= lis[1000:2000]
googleDpMeans1[2]= lis[2000:3000]
googleDpMeans1[3]= lis[3000:4000]
googleDpMeans1[4]= lis[4000:5000]

# d2Data
f = open(r'dpMeans2.csv', newline='')
lis = [float(line.strip("\r\n")) for line in f if not "epsilon" in line]     
googleDpMeans2[0]= lis[0:1000]
googleDpMeans2[1]= lis[1000:2000]
googleDpMeans2[2]= lis[2000:3000]
googleDpMeans2[3]= lis[3000:4000]
googleDpMeans2[4]= lis[4000:5000]

# originalMean
f = open(r'originalMean.csv', newline='')
reader = csv.reader(f)
next(reader, None)
originalMean = [float(line) for line in f]  
epsilons = [0.5, 1.0, 1.5, 3.0, 5.0]



# Calculate metrics for IBM
# Define properties of evaluation
dpEvaluator = DPEvaluator()
metricsGoogle = [Metrics() for _ in range(0, 5)]

for i in range(0, 5):
    metricsGoogle[i].wasserstein_distance = dpEvaluator.wasserstein_distance(
        np.asfarray(googleDpMeans1[i]), np.asfarray(googleDpMeans2[i]))
    metricsGoogle[i].mse = dpEvaluator.mse(np.asfarray(
        googleDpMeans1[i]), np.asfarray(originalMean))
    metricsGoogle[i].std = dpEvaluator.std(np.asfarray(googleDpMeans1[i]))
    metricsGoogle[i].msd = dpEvaluator.msd(np.asfarray(
        originalMean), np.asfarray(googleDpMeans1[i]))

    d1hist, d2hist, bin_edges = dpEvaluator._generate_histogram_neighbors(
        googleDpMeans1[i], googleDpMeans2[i])
    statified, _, _, _, _ = dpEvaluator._dp_test(d1hist, d2hist, bin_edges, len(
        googleDpMeans1[i]), len(googleDpMeans2[i]), epsilons[i])
    metricsGoogle[i].dp_res = statified

attr_names = dir(metricsGoogle[0])[-5:]

members = [attr for attr in dir(metricsGoogle[0]) if not callable(
    getattr(metricsGoogle[0], attr)) and not attr.startswith("__")]
members.remove('wasserstein_distance')
members.insert(1, 'wasserstein_distance')
members.remove('mse')
members.insert(2, 'mse')
members.remove('std')
members.insert(3, 'std')

file_exists_result = os.path.isfile('googleMetrics.csv')
with open('googleMetrics.csv', 'a+', newline='') as csvfile:
    fieldnames = ['epsilon'] + members
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists_result:
        writer.writeheader()
    for i in range(0, 5):
        values = [getattr(metricsGoogle[i], member) for member in members]
        writer.writerow({'epsilon': epsilons[i], members[0]: values[0], members[1]: values[1],
                        members[2]: values[2], members[3]:values[3], members[4]: values[4]})

        
print("FINISH")