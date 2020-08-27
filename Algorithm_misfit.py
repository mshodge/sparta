#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:28:05 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""
#The algorithm for the misfit analysis

#Loads packages required
from last_zero import index_of_last_nonzero
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import pandas as pd
import numpy as np
import math
import operator
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt


