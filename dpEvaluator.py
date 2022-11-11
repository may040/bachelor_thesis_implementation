#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt



class DPEvaluator:
    
    def wasserstein_distance(self, noisedData1, noisedData2):
        'Wasserstein Distance between responses of repeated algorithm on neighboring datasets'
        
        return stats.wasserstein_distance(noisedData1.astype(np.float), noisedData2.astype(np.float))
    
    def mse(self, originalData, noisedData):
        'Mean Squared Error between responses of repeated algorithm on neighboring datasets'
        
        return np.mean((originalData-noisedData) **2)
    
    def msd(self, originalData, noisedData):
        'Mean Signed Derivation between responses of repeated algorithm on neighboring datasets'
        
        return np.sum(noisedData.astype(np.float) - originalData) / noisedData.size
    
    def std(self, noisedData):
        'Standard deviation between responses of repeated algorithm on neighboring datasets'
        
        return   np.std(noisedData.astype(np.float))
    
    def _generate_histogram_neighbors(self, noisedData1, noisedData2):
        """
        Generate histograms given the vectors of repeated aggregation results
        applied on neighboring datasets
        """
        
        noisedData1 = np.asarray(noisedData1, dtype="float64")
        noisedData2 = np.asarray(noisedData2, dtype="float64")
        d = np.concatenate((noisedData1, noisedData2), axis=None)
        n = len(noisedData1)
        binlist = []
        minval = min(min(noisedData1), min(noisedData2))
        maxval = max(max(noisedData1), max(noisedData2))

        # Deciding bin width and bin list
        iqr = np.subtract(*np.percentile(d, [75, 25]))
        numerator = 2 * iqr if iqr > 0 else maxval - minval
        denominator = n ** (1.0 / 3)
        binwidth = numerator / denominator  # Freedman–Diaconis' choice
        numbins = int(math.ceil((maxval - minval) / binwidth)) if maxval > minval else 20
        binlist = np.linspace(minval, maxval, numbins)


        # Calculating histograms of fD1 and fD2
        fD1hist, bin_edges = np.histogram(noisedData1, bins=binlist, density=False)
        fD2hist, bin_edges = np.histogram(noisedData2, bins=binlist, density=False)

        return fD1hist, fD2hist, bin_edges
    
    def _plot_histogram_neighbors(
        self,
        fD1,
        fD2,
        d1histupperbound,
        d2histupperbound,
        d1hist,
        d2hist,
        d1lower,
        d2lower,
        binlist,
    ):
        """
        Plot histograms given the vectors of repeated aggregation results
        applied on neighboring datasets
        """
        plt.figure(figsize=(15, 5))
       

        ax = plt.subplot(1, 2, 1)
        ax.ticklabel_format(useOffset=False)
        plt.xlabel("Bin")
        plt.ylabel("Probability")
       
        plt.bar(
            binlist[:-1],
            d2histupperbound,
            alpha=0.5,
            width=np.diff(binlist),
            ec="k",
            align="edge",
        )
        plt.bar(binlist[:-1], d1lower, alpha=0.5, width=np.diff(binlist), ec="k", align="edge")
        plt.legend(["D1", "D2"], loc="upper right")
       

        ax = plt.subplot(1, 2, 2)
        ax.ticklabel_format(useOffset=False)
        plt.xlabel("Bin")
        plt.ylabel("Probability")
        
        plt.bar(
            binlist[:-1],
            d1histupperbound,
            alpha=0.5,
            width=np.diff(binlist),
            ec="k",
            align="edge",
        )
        plt.bar(binlist[:-1], d2lower, alpha=0.5, width=np.diff(binlist), ec="k", align="edge")
        plt.legend(["D2", "D1"], loc="upper right")
        
        plt.show()
        
    
    def _dp_test(
        self, d1hist, d2hist, binlist, d1size, d2size, epsilon
    ):
        """
        Differentially Private Predicate Test
        Check if histogram of fD1 values multiplied by e^epsilon and
        summed by delta is bounding fD2 and vice versa
        Use the histogram results and create bounded histograms
        to compare in DP test
        """
        d1_error_interval = 0.0
        d2_error_interval = 0.0
        # Lower and Upper bound
        num_buckets = binlist.size - 1
        alpha = 0.05
        critical_value = stats.norm.ppf(1 - (alpha / 2 / num_buckets), loc=0.0, scale=1.0)
        d1_error_interval = critical_value * math.sqrt(num_buckets / d1size) / 2
        d2_error_interval = critical_value * math.sqrt(num_buckets / d2size) / 2

        num_buckets = binlist.size - 1
        px = np.divide(d1hist, d1size)
        py = np.divide(d2hist, d2size)
        
        delta=1.0
        d1histbound = px * math.exp(epsilon) + delta
        d2histbound = py * math.exp(epsilon) + delta

        d1upper = np.power(np.sqrt(px * num_buckets) + d1_error_interval, 2) / num_buckets
        d2upper = np.power(np.sqrt(py * num_buckets) + d2_error_interval, 2) / num_buckets
        d1lower = np.power(np.sqrt(px * num_buckets) - d1_error_interval, 2) / num_buckets
        d2lower = np.power(np.sqrt(py * num_buckets) - d2_error_interval, 2) / num_buckets

        np.maximum(d1lower, 0.0, d1lower)
        np.maximum(d2lower, 0.0, d2lower)

        d1histupperbound = d1upper * math.exp(epsilon) + delta
        d2histupperbound = d2upper * math.exp(epsilon) + delta

        # Check if any of the bounds across the bins violate the relaxed DP condition
        bound_exceeded = np.any(
            np.logical_and(
                np.greater(d1hist, np.zeros(d1hist.size)), np.greater(d1lower, d2histupperbound)
            )
        ) or np.any(
            np.logical_and(
                np.greater(d2hist, np.zeros(d2hist.size)), np.greater(d2lower, d1histupperbound)
            )
        )

        return not bound_exceeded, d1histupperbound, d2histupperbound, d1lower, d2lower
    
  

