#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Metrics:
    
    'Defines the fields available in the metrics payload object'
    def __init__(self):
        'Privacy Category'
        self.dp_res = False
        self.wasserstein_distance = 0.0
        'Accuracy Category'
        self.mse = 0.0
        self.std = 0.0
        'Bias Category'
        self.msd = 0.0

