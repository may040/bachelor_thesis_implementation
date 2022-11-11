from metrics import *
from dpEvaluator import *
import csv
import numpy as np
import matplotlib.pyplot as plt
from diffprivlib import tools as dp
import pandas as pd
from snsql import Privacy
import snsql
import os.path
from timeit import default_timer as timer

originalMean = []
dpEvaluator = DPEvaluator()
results = [[], [], [], [], []]
calculationSN1 = [[], [], [], [], []]
calculationSN2 = [[], [], [], [], []]
snEv1 = [[], [], [], [], []]
snEv2 = [[], [], [], [], []]
executionTime = list()

# Original mean
f = open(r'originalMean.csv', newline='')
reader = csv.reader(f)
next(reader, None)
originalMean = (np.concatenate(list(reader)).ravel()).astype(np.float)
epsilons = [0.5, 1, 1.5, 3, 5]


# Execute dp algortihm on datasets 1000 times
delta = 1.0e-16
for _ in range(0, 1000):
    i = 0
    start = timer()
    for e in epsilons:
        d1_csv_path = r'd1Data.csv'
        meta_path = r'age.yaml'
        ageListD1 = pd.read_csv(d1_csv_path)
        privacy = Privacy(e, delta=delta)
        readerD1 = snsql.from_df(
            ageListD1, privacy=privacy, metadata=meta_path)

        d2_csv_path = r'd2Data.csv'
        meta_path = r'age.yaml'
        ageListD2 = pd.read_csv(d2_csv_path)
        privacy = Privacy(e, delta=delta)
        readerD2 = snsql.from_df(
            ageListD2, privacy=privacy, metadata=meta_path)

        for _ in range(0, 1000):
            calculationSN1[i].append(readerD1.execute(
                'SELECT AVG(Age) AS age FROM AGE.AGE'))
            calculationSN2[i].append(readerD2.execute(
                'SELECT AVG(Age) AS age FROM AGE.AGE'))
        i += 1

    end = timer()
    executionTime.append(end-start)

    for n in range(0, 5):
        for sublist in calculationSN2[n]:
            for item in sublist:
                for element in item:
                    if not isinstance(element, str):
                        snEv2[n].append(element)

    for n in range(0, 5):
        for sublist in calculationSN1[n]:
            for item in sublist:
                for element in item:
                    if not isinstance(element, str):
                        snEv1[n].append(element)

    for i in range(0, 5):
        metricsSN = Metrics()
        metricsSN.wasserstein_distance = dpEvaluator.wasserstein_distance(
            np.asfarray(snEv1[i]), np.asfarray(snEv2[i]))
        metricsSN.mse = dpEvaluator.mse(
            np.asfarray(snEv1[i]), np.asfarray(originalMean))
        metricsSN.std = dpEvaluator.std(np.asfarray(snEv1[i]))
        metricsSN.msd = dpEvaluator.msd(
            np.asfarray(originalMean), np.asfarray(snEv1[i]))

        d1hist, d2hist, bin_edges = dpEvaluator._generate_histogram_neighbors(
            snEv1[i], snEv2[i])
        statified, _, _, _, _ = dpEvaluator._dp_test(
            d1hist, d2hist, bin_edges, len(snEv1[i]), len(snEv2[i]), epsilons[i])
        metricsSN.dp_res = statified
        results[i] = metricsSN

    for s in range(0, 5):
        calculationSN1[s].clear()
        calculationSN2[s].clear()
        snEv1[s].clear()
        snEv2[s].clear()

    members = [attr for attr in dir(results[0]) if not callable(
        getattr(results[0], attr)) and not attr.startswith("__")]
    members.remove('wasserstein_distance')
    members.insert(1, 'wasserstein_distance')
    members.remove('mse')
    members.insert(2, 'mse')
    members.remove('std')
    members.insert(3, 'std')

file_exists_performance = os.path.isfile('sn_performance.csv')
with open('sn_performance.csv', 'a+', newline='') as csvfile:
    fieldnames = ['Smartnoise Performance Times']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists_performance:
        writer.writeheader()
    for i in range(0, len(executionTime)):
        writer.writerow({'Smartnoise Performance Times': executionTime[i]})

print("FINISH")
