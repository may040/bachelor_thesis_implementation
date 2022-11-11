import matplotlib.pyplot as plt
import csv
import numpy as np

keys = ["Wasserstein-Distanz", "Mittlere quadratische Abweichung",
        "Standardabweichung", "Mittlere vorzeichenbehaftete Abweichung"]
frameworkNames = ["Smartnoise SDK", "IBM DP", "Google DP"]
frameworkColors = ["blue", "orange", "red"]
epsilons = [0.5, 1.0, 1.5, 3.0, 5.0]
ibmMetrics = list()
snMetrics = list()
googleMetrics = list()

run = 1
results = dict(zip(keys, [list() for _ in range(0, len(keys))]))

f = open(r'ibmMetrics.csv', newline='')
reader = csv.reader(f)
next(reader, None)
for line in reader:
    ibmMetrics.append([float(x) for x in line[2:6]])

f = open(r'snMetrics.csv', newline='')
reader = csv.reader(f)
next(reader, None)
for line in reader:
    snMetrics.append([float(x) for x in line[2:6]])

f = open(r'googleMetrics.csv', newline='')
reader = csv.reader(f)
next(reader, None)
for line in reader:
    googleMetrics.append([float(x) for x in line[2:6]])

for i in range(0, len(keys)):
    results[keys[i]].append([line[i] for line in ibmMetrics])
    results[keys[i]].append([line[i] for line in snMetrics])
    results[keys[i]].append([line[i] for line in googleMetrics])


for key in keys:
    for framework in range(0, 3):
        plt.plot(epsilons, results[key][framework][0:run * 5], linestyle='--',
                 marker='o', color=frameworkColors[framework], label=frameworkNames[framework])
        plt.title(frameworkNames[framework]+" "+key)
        plt.xlabel("Epsilon-Werte")
        plt.legend(loc="best")
        plt.ylabel(key)
        plt.show()
    plt.plot(epsilons, results[key][0][0:run * 5], linestyle='--',
             marker='o', color=frameworkColors[0], label=frameworkNames[0])
    plt.plot(epsilons, results[key][1][0:run * 5], linestyle='--',
             marker='o', color=frameworkColors[1], label=frameworkNames[1])
    plt.plot(epsilons, results[key][2][0:run * 5], linestyle='--',
             marker='o', color=frameworkColors[2], label=frameworkNames[2])
    plt.title("Vergleich der Frameworks in"+" "+key)
    plt.xlabel("Epsilon-Werte")
    plt.legend(loc="best")
    plt.ylabel(key)
    plt.show()
