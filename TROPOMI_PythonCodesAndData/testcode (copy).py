#!/usr/bin/python      
from netCDF4 import Dataset
import numpy as np
from numpy import unravel_index
import os
os.environ['PROJ_LIB'] = '/home/ksb4/anaconda3/share/proj'
import sys
import time
import calendar
import datetime as dt
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt