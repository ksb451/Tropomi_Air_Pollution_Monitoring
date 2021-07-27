#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 00:48:17 2021

@author: ksb4
"""
import numpy as np
import sys
from numpy import unravel_index
from netCDF4 import Dataset
import math
import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = pd.read_csv("data_val.csv", index_col=0)
print(df.head())
df.info()
df.index = pd.to_datetime(df.index)
df.info()
print(df.head())

fig, ax = plt.subplots(figsize=(20, 10))
ax.scatter(df.index.values,
        df['0'],
        color='purple')

ax.plot(df.index.values,df['0'],color='purple')

ax.set(xlabel="Date",
       ylabel="O3 vertical Column (mol/m2)",
       title="O3 level in Delhi as per the last few years")
plt.setp(ax.get_xticklabels(), rotation=45)

plt.show()
