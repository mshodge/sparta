#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 14:02:54 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""

#A script to perform a misfit analysis between manual and algorithm methods
#to identify the best performing parameter space

#Loads packages required
import pickle
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
from Algorithm_misfit import algorithm_misfit

#Creates blank variables
prof_height_subsample=np.zeros((num_subsample,nump))
prof_distance_subsample=np.zeros((num_subsample,nump))

# Creates subsample of data for analysis
n=-1
for i in range (0,num_profiles,subsample):  
    n=n+1
    prof_height_subsample[n,:]=prof_height[i,:] 
    prof_distance_subsample[n,:]=prof_distance[i,:]    

iterations=num_subsample

print ('Running Algorithm on Sub Sampled Catalog of size %d, Please Wait...' % (iterations))

#Run smoothing and misfit analysis between subsampled data set

#Choose minimum and maximum filter bin size (bin_min, bin_max) and step between (bin_step).
#Choose minimum and maximum slope threshold (theta_T_min, theta_T_max) and step between (theta_T_step)
#Choose derivative of slope threshold (phi_T)

bin_max = 40
bin_min = 9 #needs to be an odd integer
bin_step = 4 #needs to be an even integer
theta_T_max = 40 #insert positive integer here, turns to negative later
theta_T_min = 7 #insert positive integer here, turns to negative later
theta_T_step = 4  #insert positive integer here, turns to negative later
phi_T = 5 

#---IMPORTANT---

#Choose two types of filter method to compare: 1 - None; 2 - Average; 
#3 - Sav Gol; 4 - Median; 5 - Lowess

#Comment out filters not needed

#---ANALYSIS 1----

#method = 1 #No smoothing
#method_name_1 = 'None'
#analysis_1=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (No Filter), Please Wait...')
#
#method = 2 #Average smoothing
#method_name_1 = 'Average'
#analysis_1=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Average Filter), Please Wait...')

method = 3 #Sav Gol smoothing
method_name_1 = 'Sav Gol'
analysis_1=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
print ('Finished Analysis (Savitzky-Golay Filter), Please Wait...')

#method = 4 #Median smoothing
#method_name_1 = 'Median'
#analysis_1=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Median Filter), Please Wait...')
#
#method = 5 #Lowess smoothing
#method_name_1 = 'Lowess'
#analysis_1=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Lowess Filter), Please Wait...')

analysis_number_1=method


#---IMPORTANT---

#---ANALYSIS 2----

#method = 1 #No smoothing
#method_name_2 = 'None'
#analysis_2=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (No Filter), Please Wait...')
#
#method = 2 #Average smoothing
#method_name_2 = 'Average'
#analysis_2=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Average Filter), Please Wait...')
#
#method = 3 #Sav Gol smoothing
#method_name_2 = 'Sav Gol'
#analysis_2=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Savitzky-Golay Filter), Please Wait...')
#
#method = 4 #Median smoothing
#method_name_2 = 'Median'
#analysis_2=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
#print ('Finished Analysis (Median Filter), Please Wait...')

method = 5 #Lowess smoothing
method_name_2 = 'Lowess'
analysis_2=algorithm_misfit(prof_distance_subsample,prof_height_subsample,h_manual,w_manual,slope_manual,nump,iterations,method,bin_max,bin_min,bin_step,theta_T_max,theta_T_min,theta_T_step,phi_T)
print ('Finished Analysis (Lowess Filter), Please Wait...')

analysis_number_2=method



#Output values for ANALYSIS 1

h_1=analysis_1[0] #scarp height
w_1=analysis_1[1] #scarp width
slope_1=analysis_1[2] #scarp slope

misfit_height_1=analysis_1[3] #misfit height
misfit_width_1=analysis_1[4] #misfit width
misfit_slope_1=analysis_1[5] #misfit slope

misfit_height_average_1=analysis_1[6] #average misfit height
misfit_width_average_1=analysis_1[7] #average misfit width
misfit_slope_average_1=analysis_1[8] #average misfit slope

#Output values for ANALYSIS 2

h_2=analysis_2[0] #scarp height
w_2=analysis_2[1] #scarp width
slope_2=analysis_2[2] #scarp slope

misfit_height_2=analysis_2[3] #misfit height
misfit_width_2=analysis_2[4] #misfit width
misfit_slope_2=analysis_2[5] #misfit slope

misfit_height_average_2=analysis_2[6] #average misfit height
misfit_width_average_2=analysis_2[7] #average misfit width
misfit_slope_average_2=analysis_2[8] #average misfit slope

#Grid setup

gridx=analysis_1[9]
gridy=analysis_1[10]

#Dump save analysis
with open('Misfit_Analysis.pickle', 'wb') as f:
    pickle.dump(h_1, f)
    pickle.dump(h_2, f)
    pickle.dump(w_1, f)
    pickle.dump(w_2, f)
    pickle.dump(slope_1, f)
    pickle.dump(slope_2, f)
    pickle.dump(misfit_height_1, f)
    pickle.dump(misfit_height_2, f)
    pickle.dump(misfit_width_1, f)
    pickle.dump(misfit_width_2, f)
    pickle.dump(misfit_slope_1, f)
    pickle.dump(misfit_slope_2, f)
    pickle.dump(misfit_height_average_1, f)
    pickle.dump(misfit_height_average_2, f)
    pickle.dump(misfit_width_average_1, f)
    pickle.dump(misfit_width_average_2, f)
    pickle.dump(misfit_slope_average_1, f)
    pickle.dump(misfit_slope_average_2, f)
    pickle.dump(gridx, f)
    pickle.dump(gridy, f)
 

#Count the number of samples where scarp parameter was calculated
misfit_height_1_min=np.zeros((iterations,1))
misfit_height_2_min=np.zeros((iterations,1))

misfit_height_1_count=np.zeros((len(misfit_height_average_1[:,1]),(len(misfit_height_average_1[1,:]))))
misfit_height_2_count=np.zeros((len(misfit_height_average_2[:,1]),(len(misfit_height_average_2[1,:]))))

for i in range (0,iterations):
    misfit_height_1_min[i]=np.ndarray.min(abs(misfit_height_1[i,:,:]))
    misfit_height_2_min[i]=np.ndarray.min(abs(misfit_height_2[i,:,:]))
    
misfit_height_1_count_all=np.count_nonzero(~np.isnan(misfit_height_1_min))
misfit_height_2_count_all=np.count_nonzero(~np.isnan(misfit_height_2_min))

for m in range (0,(len(misfit_height_average_1[:,1]))):
    for n in range (0,(len(misfit_height_average_1[1,:]))):
        misfit_height_1_count[m,n]=np.count_nonzero(~np.isnan(misfit_height_1[:,m,n]))
for m in range (0,(len(misfit_height_average_1[:,1]))):
    for n in range (0,(len(misfit_height_average_1[1,:]))):
        misfit_height_2_count[m,n]=np.count_nonzero(~np.isnan(misfit_height_2[:,m,n]))

    
#Determining the best parameter space
        
value = 0.0
count_min=0.5 #Minimum number of successful profiles (normally 50% or 0.5)

A=(abs(misfit_height_average_1)+abs(misfit_width_average_1)+abs(misfit_slope_average_1))/(misfit_height_1_count/num_subsample)
where_are_NaNs = np.isnan(A)
A[where_are_NaNs] = 9999
where_less_than_mincount=misfit_height_1_count/num_subsample<count_min
A[where_less_than_mincount] = 9999
X_1 = np.abs(A-value)
idx_1 = np.where( X_1 == X_1.min() )

B=(abs(misfit_height_average_2)+abs(misfit_width_average_2)+abs(misfit_slope_average_2))/(misfit_height_2_count/num_subsample)
where_are_NaNs = np.isnan(B)
B[where_are_NaNs] = 9999
where_less_than_mincount=misfit_height_2_count/num_subsample<count_min
B[where_less_than_mincount] = 9999
X_2 = np.abs(B-value)
idx_2 = np.where( X_2 == X_2.min() )

#Prints out the best parameter space as 'Method name (i.e., Sav Gol,), average height misfit, average width misfit, average slope misfit, count, slope threshold, bin size'

if abs(A[idx_1[0], idx_1[1]])<abs(B[idx_2[0], idx_2[1]]):
    print('Best Parameter Space:')
    print('method = %s' %method_name_1)
    print('bin size = %s' %gridy[idx_1[0], idx_1[1]])
    print('slope threshold = %s' %gridx[idx_1[0], idx_1[1]])
    print('average misfit height (m) = %s' %misfit_height_average_1[idx_1[0], idx_1[1]])
    print('average misfit width (m) = %s' %misfit_width_average_1[idx_1[0], idx_1[1]])
    print('average misfit slope (degrees) = %s' %misfit_slope_average_1[idx_1[0], idx_1[1]])
    print('misfit count = %s' %misfit_height_1_count[idx_1[0], idx_1[1]])
    method=analysis_number_1
    theta_T=np.int(gridx[idx_1[0], idx_1[1]])
    idx_theta=np.int(idx_1[1])
    bin_size=np.int(gridy[idx_1[0], idx_1[1]])
    idx_b=np.int(idx_1[0])
else:
    print('Best Parameter Space:')
    print('method = %s' %method_name_2)
    print('bin size = %s' %gridy[idx_2[0], idx_2[1]])
    print('slope threshold = %s' %gridx[idx_2[0], idx_2[1]])
    print('average misfit height (m) = %s' %misfit_height_average_2[idx_2[0], idx_2[1]])
    print('average misfit width (m) = %s' %misfit_width_average_2[idx_2[0], idx_2[1]])
    print('average misfit slope (degrees) = %s' %misfit_slope_average_2[idx_2[0], idx_2[1]])
    print('misfit count = %s' %misfit_height_2_count[idx_2[0], idx_2[1]])
    method=analysis_number_2
    theta_T=np.int(gridx[idx_2[0], idx_2[1]])
    idx_theta=np.int(idx_2[1])
    bin_size=np.int(gridy[idx_2[0], idx_2[1]])
    idx_b=np.int(idx_2[0])

###
    
#Set levels for misfit plots
    
levels_height=[-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10]
levels_width=[-20, -15, -5, 0, 5, 10, 15, 20]
levels_slope=[-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
levels_count=[2,4,6,8,10,12,14,16,18,20]


#Plot figures

plt.figure(3)

#Plot for analysis number 1

plt.subplot(4,2,1)
plt.contourf(gridx,gridy,misfit_height_average_1,levels_height,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit height (m)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit height using %s filter' %method_name_1, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,3)
plt.contourf(gridx,gridy,misfit_width_average_1,levels_width,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit width (m)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit width using %s filter' %method_name_1, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,5)
plt.contourf(gridx,gridy,misfit_slope_average_1,levels_slope,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit slope ($^\circ$)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit slope using %s filter' %method_name_1, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,7)
cmap = plt.cm.get_cmap("winter")
plt.contourf(gridx,gridy,misfit_height_1_count,levels_count,cmap=cmap, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit count', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.xlabel('$\mathit{b}$ value (m)', fontsize=8)
plt.ylabel('${\\theta}_T$ ($^\circ$)', fontsize=8)
plt.title('Misfit count using %s filter' %method_name_1, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

#Plot for analysis number 2

plt.subplot(4,2,2)
plt.contourf(gridx,gridy,misfit_height_average_2,levels_height,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit height (m)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit height using %s filter' %method_name_2, fontsize=8)
#plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,4)
plt.contourf(gridx,gridy,misfit_width_average_2,levels_width,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit width (m)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit width using %s filter' %method_name_2, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,6)
plt.contourf(gridx,gridy,misfit_slope_average_2,levels_slope,cmap=plt.cm.bwr, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit slope ($^\circ$)', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit slope using %s filter' %method_name_2, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.subplot(4,2,8)
cmap = plt.cm.get_cmap("winter")
plt.contourf(gridx,gridy,misfit_height_2_count,levels_count,cmap=cmap, extend ='both')
plt.gca().patch.set_color('.25')
cbar=plt.colorbar()
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=8)
cbar.set_label('misfit count', rotation=270, fontsize=8)
plt.scatter(gridx,gridy,s=2,facecolors='none', edgecolors='w')
plt.title('Misfit count using %s filter' %method_name_2, fontsize=8)
plt.xticks(size = 8)
plt.yticks(size = 8)

plt.tight_layout()


if method==analysis_number_1:
    h_subsample=h_1[:,idx_b,idx_theta]
    w_subsample=w_1[:,idx_b,idx_theta]
    slope_subsample=slope_1[:,idx_b,idx_theta]
else:
    h_subsample=h_2[:,idx_b,idx_theta]
    w_subsample=w_2[:,idx_b,idx_theta]
    slope_subsample=slope_2[:,idx_b,idx_theta]   


#Plot against manual plot

plt.figure(4) #plot manual data

plt.subplot(3,1,1)
plt.scatter(dist_along_fault,h_manual,s=5,color='black') 
plt.scatter(dist_along_fault,h_subsample,s=5,color='red')    
plt.ylabel('Scarp Height (m)', fontsize=8)
plt.title('Manual (black) v Algorithm (red) Scarp Height Profile', fontsize=8)
#plt.ylim([0, np.int(math.ceil(np.amax(h_manual)/10.0))*10])
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
plt.subplot(3,1,2)
plt.scatter(dist_along_fault,w_manual,s=5,color='black')  
plt.scatter(dist_along_fault,w_subsample,s=5,color='red')      
plt.ylabel('Scarp Width (m)', fontsize=8)
plt.title('Manual (black) v Algorithm (red) Scarp Width Profile', fontsize=8)
#plt.ylim([0, np.int(math.ceil(np.amax(w_manual)/10.0))*10])
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
plt.subplot(3,1,3)
plt.scatter(dist_along_fault,slope_manual,s=5,color='black')
plt.scatter(dist_along_fault,slope_subsample,s=5,color='red')        
plt.xlabel('Distance along fault (km)', fontsize=8)
plt.ylabel('Scarp Slope ($^\circ$)', fontsize=8)
plt.title('Manual (black) v Algorithm (red) Scarp Slope Profile', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
#plt.ylim([(np.int(math.ceil(np.amin(slope_manual)/10.0))*10)-10,0])

### END
