#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:21:14 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""
#The first script, used to load the raw profile data - always required

#Loads packages required
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import datetime

#Grab timestamp for saving files
time_stamp = '{:%Y_%m_%d}'.format(datetime.datetime.now())


#Specify the filename of the data
filename = 'FILENAME HERE' #CSV format: Col 1: Distance along elevation profile; Col 2: Height in meters; 
                        #Row 1: Headers

#Loads the data under the variable 'data'
data = genfromtxt(str(filename) +'.csv', delimiter=',',skip_header=1) #change skip_header=1 to 
                                                                    #skip_header=0 if no header in csv


#Are the profiles in the correct order? If yes, use 0, if not use 1. Sometimes 
#GIS software can output data in the reverse order.
reverse = 0 #1 = yes, 2 = no

#State the resolution of the DEM
resolution = 12 #units meters

#Specify the length of each profile in meters
profile_length = 400 #units meters

#Specify the distance between profiles:
dist_between_profiles = 100 #units meters

#Creates a distance variable
prof_distance_raw=data[:,0]

#Creates a elevation variable
prof_elevation_raw=data[:,1]

#Calculates the number of profiles
try:
    nump
except NameError:
    nump = np.int(np.ceil(profile_length/resolution)) #number of points in a profile
num_profiles=np.int(((len(prof_distance_raw))/nump))

#Transposes and edits the elevation and distance data if the profiles need to be reversed  
prof_elevation_raw=np.transpose(prof_elevation_raw)
prof_elevation_raw = np.reshape(prof_elevation_raw,(num_profiles,nump))
if reverse==1:
    prof_elevation_raw=np.fliplr(prof_elevation_raw)
prof_distance_raw=np.array([np.arange(nump)*resolution,]*num_profiles)

#Interpolates to 1m resolution to allow for smoothing later
prof_height=np.zeros((num_profiles,profile_length))
prof_distance=np.zeros((num_profiles,profile_length))

for x in range (0,num_profiles,1):
    prof_distance[x,:]=np.linspace(0,profile_length-1,profile_length)
    f = interp1d(prof_distance_raw[x,:], prof_elevation_raw[x,:],fill_value='extrapolate')
    prof_height[x,:]=f(prof_distance[x,:])
    
nump=profile_length

### END
