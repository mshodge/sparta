#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:21:14 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""
#A script used to load data from a manual analysis, used for the misfit analysis against the algorithm
#If script #2 has been run recently, then you do not need to run this
#This can follow script #1 if manual analysis was performed previously

#Loads packages required
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np

#Specific the filename e.g., THY_W_12_2018_04_13_manual
filename='FILENAME HERE'

#loads the data from the _manual file
manual_data = genfromtxt(str(filename) +'.csv', delimiter=',',skip_header=1) 

#creates the variables from the loaded data
dist_along_fault=manual_data[:,0] #the distance along the fault
h_manual=manual_data[:,1] #the manual scarp height
w_manual=manual_data[:,2] #the manual scarp width
slope_manual=manual_data[:,3] #the manual scarp slope

#calculates the number of subsamples used (i.e. the number of profiles a 
#manual analysis was performed for)
num_subsample=np.int(((len(dist_along_fault))))
subsample=np.int(np.ceil(num_profiles/num_subsample))

### END
