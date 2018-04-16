#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:52:25 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""

#A script to calculate the along-strike scarp height, width and slope for
#a fault using an semi-automated algorithm approach

#Loads packages required
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
from Algorithm import algorithm

#For the best results, please perform a misfit analysis (steps #1 to #4).
#This will help identify the best parameter space to use to reduce errors.
#If you have already performed this misfit analysis, and know the best parameters
#to use, please change below to '0' and specify the parameters. Remember to use
#script #1 to load the data first though...

continued = 1 #1 - yes, 0 - no

if continued == 0:
    bin_size = 21 #specify filter bin size
    theta_T = -21 #specify slope threshold
    phi_T = 5 #specify derivative of slope threshold
    method = 5 #specify filter method type: 1 - None; 2 - Average; 3 - Sav Gol; 4 - Median; 5 - Lowess
    
iterations=num_profiles
print ('Running Algorithm on Complete Catalog of size %d, Please Wait...' % (iterations))

#Run algorithm for entire catalog
analysis=algorithm(prof_distance,prof_height,nump,iterations,method,bin_size,theta_T,phi_T)
print ('Finished Analysis, Please Wait...')
  
h=analysis[0]
w=analysis[1]    
slope=-analysis[2]
    
h_qc=copy.copy(h)
w_qc=copy.copy(w)
slope_qc=copy.copy(slope)

#remove widths larger than the maximum in the manual study, or 100 m
#if np.amax(manual_data[:,2])>100:
#    w_max=np.amax(manual_data[:,2])*2
#else:
#    w_max=100
    
w_max=np.amax(manual_data[:,2])*2 

for i in range(iterations):
    if w[i]>w_max or w[i]<0:
        h[i]='nan'
        w[i]='nan'
        slope[i]='nan'

h_max=np.nanmean(h)+(2*np.nanstd(h))
w_max=np.nanmean(w)+(2*np.nanstd(w))
slope_min=np.nanmean(slope)-(2*np.nanstd(slope))

#Remove data that is 2 standard deviations from the mean, or negative heights and positive slopes
for i in range(iterations):
    if h[i]>h_max or h[i]<0 or np.isnan(h[i]):
        h_qc[i]='nan'
        w_qc[i]='nan'
        slope_qc[i]='nan'
    if w[i]>w_max or w[i]<0 or np.isnan(w[i]):
        h_qc[i]='nan'
        w_qc[i]='nan'
        slope_qc[i]='nan'
    if slope[i]>0 or slope[i]<slope_min or np.isnan(slope[i]):
        h_qc[i]='nan'
        w_qc[i]='nan'
        slope_qc[i]='nan'      
  
#Apply a moving average to the along-strike profile

start_dist=0 #does the profile start from the beginning of the fault, if not specify the distance
dist=((np.array(np.arange(iterations),))/10)+start_dist #distance along fault

#specify the amount of smoothing wanted

smoothing_required=1000 #i.e., 1000m

h_smooth=pd.rolling_mean(h,np.int(smoothing_required/dist_between_profiles),min_periods=2)
w_smooth=pd.rolling_mean(w,np.int(smoothing_required/dist_between_profiles),min_periods=2)
slope_smooth=pd.rolling_mean(slope,np.int(smoothing_required/dist_between_profiles),min_periods=2)

h_qc_smooth=pd.rolling_mean(h_qc,np.int(smoothing_required/dist_between_profiles),min_periods=2)
w_qc_smooth=pd.rolling_mean(w_qc,np.int(smoothing_required/dist_between_profiles),min_periods=2)
slope_qc_smooth=pd.rolling_mean(slope_qc,np.int(smoothing_required/dist_between_profiles),min_periods=2)

#Plots the raw algorithm results without the quality check

plt.figure(5)
plt.subplot(3,1,1)
plt.plot(dist,h,'bo',markersize=1)
plt.plot(dist,h_smooth,'r')
plt.ylabel('Scarp Height (m)', fontsize=8)
plt.title('Scarp Height Profile', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([0, 25])
plt.subplot(3,1,2)
plt.plot(dist,w,'bo',markersize=1)
plt.plot(dist,w_smooth,'r')
plt.ylabel('Scarp Width (m)', fontsize=8)
plt.title('Scarp Width Profile', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([0, 100])
plt.subplot(3,1,3)
plt.plot(dist,slope,'bo',markersize=1)
plt.plot(dist,slope_smooth,'r')
plt.xlabel('Distance along fault (km)', fontsize=8)
plt.ylabel('Scarp Slope ($^\circ$)', fontsize=8)
plt.title('Scarp Slope Profile', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([-50, 0])

#Plots the along-strike profiles following a quality check

plt.figure(6)
plt.subplot(3,1,1)
plt.plot(dist,h_qc,'bo',markersize=1)
plt.plot(dist,h_qc_smooth,'r')
plt.ylabel('Scarp Height (m)', fontsize=8)
plt.title('Scarp Height Profile (Quality Checked)', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([0, 50])
plt.subplot(3,1,2)
plt.plot(dist,w_qc,'bo',markersize=1)
plt.plot(dist,w_qc_smooth,'r')
plt.ylabel('Scarp Width (m)', fontsize=8)
plt.title('Scarp Width Profile (Quality Checked)', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([0, 100])
plt.subplot(3,1,3)
plt.plot(dist,slope_qc,'bo',markersize=1)
plt.plot(dist,slope_qc_smooth,'r')
plt.xlabel('Distance along fault (km)', fontsize=8)
plt.ylabel('Scarp Slope ($^\circ$)', fontsize=8)
plt.title('Scarp Slope Profile (Qquality Checked)', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([-50, 0])

#Dump save results

with open('Algorithm_Results.pickle', 'wb') as f:
    pickle.dump(h, f)
    pickle.dump(w, f)
    pickle.dump(slope, f)

#Save results to csv file

dist=np.reshape(dist,(np.size(dist),1))
scarp_morphology=np.hstack((dist,h))
scarp_morphology=np.hstack((scarp_morphology,w))
scarp_morphology=np.hstack((scarp_morphology,slope))

scarp_morphology_qc=np.hstack((dist,h_qc))
scarp_morphology_qc=np.hstack((scarp_morphology_qc,w_qc))
scarp_morphology_qc=np.hstack((scarp_morphology_qc,slope_qc))

np.savetxt(str(filename)+'_'+str(time_stamp)+'_morphology.csv',scarp_morphology,delimiter=',',header='Distance Along Fault (km),Scarp Height (m), Scarp Width (m), Scarp Slope (deg)')
np.savetxt(str(filename)+'_'+str(time_stamp)+'_morphology_qualitychecked.csv',scarp_morphology_qc,delimiter=',',header='Distance Along Fault (km),Scarp Height (m), Scarp Width (m), Scarp Slope (deg)')

### END
