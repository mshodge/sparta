#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:08:29 2017 - v1.0 Finalised Fri Apr 13

@author: michaelhodge
"""
#A script for calculating the manual scarp morphology for profiles - needed for misfit analysis

#Loads packages required
import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import plot, ginput, show, axis
from sklearn.metrics import mean_squared_error
import copy

#Specific here the number of profiles you want to analyse manually
num_subsample=50
subsample=np.int(np.ceil(num_profiles/num_subsample))
num_subsample=np.int(np.ceil(num_profiles/subsample))

#Creates blank variables
crest=np.zeros((num_subsample,2))
base=np.zeros((num_subsample,2))
dist_along_fault=np.zeros((num_subsample,1))
h=np.zeros((num_subsample,1))
slope=np.zeros((num_subsample,1))
w=np.zeros((num_subsample,1))
manual_morphology=np.zeros((num_subsample,0))
rmse_upper=np.zeros((num_subsample,1))
rmse_lower=np.zeros((num_subsample,1))
rmse_scarp=np.zeros((num_subsample,1))
rmse_av=np.zeros((num_subsample,1))

#Loop to calculate slope and derivative of slope values, 
#then plots the profile and requires user to click the 
#top (crest) and then bottom (base) of the scarp, a third 
#click then starts the calculation steps for the scarp parameters

n=-1

for i in range (0,num_profiles,subsample):
    
    n=n+1
    dist_along_fault[n,:]=i/(1000/dist_between_profiles)
    
    distance=prof_distance[i,:]
    height=prof_height[i,:]
    
    #Calculates the slope and derivative of slope based on the elevation profiles
    dzdx = np.diff(height)
    dzdx = np.hstack((0,dzdx))
    d2zdx2 = np.diff(dzdx)
    d2zdx2 = np.hstack((0,d2zdx2))
    
    #plots the elevation, slope and derivative of slope and asks the user to 
    #click the top, then bottom of the scarp, third click to finish
    plt.figure(1)
    plt.subplot(3,1,1)
    plt.scatter(distance, height,s=.5,facecolors='none', edgecolors='k')
    plt.plot(distance, height,color='k', linewidth=0.5)
    plt.ylabel('Height (m)', fontsize=8)
    plt.xticks([])
    plt.yticks(size = 8)
    plt.tight_layout()
    plt.subplot(3,1,2)
    plt.scatter(distance, dzdx,s=.5,facecolors='none', edgecolors='k')
    plt.ylabel('dz/dx ($^\circ$)', fontsize=8)
    plt.xticks([])
    plt.yticks(size = 8)
    plt.subplot(3,1,3)
    plt.scatter(distance, d2zdx2,s=.5,facecolors='none', edgecolors='k')
    plt.ylabel('d2z/dx2 ($^\circ$/m)', fontsize=8)
    plt.xlabel('Distance (m)', fontsize=8)
    plt.xticks(size = 8)
    plt.yticks(size = 8)
    plt.show()
    
    pts = ginput(3) # it will wait for three clicks
    pts = np.array(pts)
    
    #Saves the user specified location of the crest and the base
    crest[n,0]=pts[1,0]
    crest[n,1]=pts[1,1]
    base[n,0]=pts[0,0]
    base[n,1]=pts[0,1]
    plt.close()
    
    #Takes the data for the profile
    distance=np.reshape(distance,(nump,1))
    height=np.reshape(height,(nump,1))
    dzdx=np.reshape(dzdx,(nump,1))
    d2zdx2=np.reshape(d2zdx2,(nump,1))
    
    profile=np.zeros((nump,0))
    profile = np.hstack((profile, distance))
    profile = np.hstack((profile, height))
    profile = np.hstack((profile, dzdx))
    profile = np.hstack((profile, d2zdx2))
    
    #Blanks the upper oririginal surface, lower original surface and scarp surface variables
    upper=np.zeros((nump,4))
    lower=np.zeros((nump,4))
    scarp=np.zeros((nump,4))

    #Stores the upper oririginal surface, lower original surface and scarp surface 
    #variables based on the users clicks
    for x in range (0,nump):       
        if profile[x,0]<crest[n,0]:
            upper[x,0]=profile[x,0]
            upper[x,1]=profile[x,1]
            upper[x,2]=profile[x,2]
            upper[x,3]=profile[x,3]
        elif profile[x,0]>base[n,0]:
            lower[x,0]=profile[x,0]
            lower[x,1]=profile[x,1]
            lower[x,2]=profile[x,2]
            lower[x,3]=profile[x,3]
        elif crest[n,0]<=profile[x,0]<=base[n,0]:
            scarp[x,0]=profile[x,0]
            scarp[x,1]=profile[x,1]
            scarp[x,2]=profile[x,2]
            scarp[x,3]=profile[x,3] 
            
    #removes zeros and replaces with NaN result
    upper[upper == 0] = 'nan'
    scarp[scarp == 0] = 'nan'
    lower[lower == 0] = 'nan'
    
    #Calculates the regression line for each surface
    x=upper[:,0]
    y=upper[:,1]
    idx = np.isfinite(x) & np.isfinite(y)
    p_upper = np.polyfit(x[idx], y[idx],1);
    
    x=lower[:,0]
    y=lower[:,1]
    idx = np.isfinite(x) & np.isfinite(y)
    p_lower = np.polyfit(x[idx], y[idx],1);
    
    x=scarp[:,0]
    y=scarp[:,1]
    idx = np.isfinite(x) & np.isfinite(y)
    p_scarp = np.polyfit(x[idx], y[idx],1);
    
    #Extrapolates the regression line for each surface
    upper_poly_height = np.polyval(p_upper,distance)
    lower_poly_height = np.polyval(p_lower,distance)
    scarp_poly_height = np.polyval(p_scarp,distance)
    
    upper_min_ind=np.nanargmin(upper[:,0])
    upper_max_ind=np.nanargmax(upper[:,0])
    lower_min_ind=np.nanargmin(lower[:,0])
    lower_max_ind=np.nanargmax(lower[:,0])
    scarp_min_ind=np.nanargmin(scarp[:,0])
    scarp_max_ind=np.nanargmax(scarp[:,0])   
    
    
    #Calculates the RMSE
    rmse_upper[n]=mean_squared_error(upper[upper_min_ind:upper_max_ind,1], upper_poly_height[upper_min_ind:upper_max_ind,0])
    rmse_lower[n]=mean_squared_error(lower[lower_min_ind:lower_max_ind,1], lower_poly_height[lower_min_ind:lower_max_ind,0])
    rmse_scarp[n]=mean_squared_error(scarp[scarp_min_ind:scarp_max_ind,1], scarp_poly_height[scarp_min_ind:scarp_max_ind,0])
    rmse_av[n]=(rmse_upper[n]+rmse_lower[n])/2
     
    #Finds the point of maximum slope on the scarp, return scarp heights from 
    #upper and lower slopes
    ind=np.nanargmin(scarp[:,2])
    h[n]=upper_poly_height[ind,0]-lower_poly_height[ind,0]      
    w[n]=base[n,0]-crest[n,0]
    slope[n]=math.degrees(math.atan(p_scarp[0]))
    if h[n] > 100: #stops very large scarps being picked due to error
        h[n]=float('nan')

#Generates the manual along-fault plot from manual analysis        
plt.figure(2) #plot manual data
plt.subplot(3,1,1)
plt.scatter(dist_along_fault,h,s=5,facecolors='none', edgecolors='k')
plt.ylabel('Scarp Height (m)', fontsize=8)
plt.title('Manual Scarp Height Profile', fontsize=8)
plt.ylim([0, np.int(math.ceil(np.amax(h)/10.0))*10])
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
plt.subplot(3,1,2)
plt.scatter(dist_along_fault,w,s=5,facecolors='none', edgecolors='k')
plt.ylabel('Scarp Width (m)', fontsize=8)
plt.title('Manual Scarp Width Profile', fontsize=8)
plt.ylim([0, np.int(math.ceil(np.amax(w)/10.0))*10])
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
plt.subplot(3,1,3)
plt.scatter(dist_along_fault,slope,s=5,facecolors='none', edgecolors='k')
plt.xlabel('Distance along fault (km)', fontsize=8)
plt.ylabel('Scarp Slope ($^\circ$)', fontsize=8)
plt.title('Manual Scarp Slope Profile', fontsize=8)
plt.subplots_adjust(hspace=1)
plt.xticks(size = 8)
plt.yticks(size = 8)
plt.ylim([(np.int(math.ceil(np.amin(slope)/10.0))*10)-10,0])

#Stacks the variables
manual_morphology = np.hstack((manual_morphology,dist_along_fault))
manual_morphology = np.hstack((manual_morphology,h))
manual_morphology = np.hstack((manual_morphology,w))
manual_morphology = np.hstack((manual_morphology,slope))

#Saves the variables as two csv files using the previous filename: _manual is 
#the manually derived scarp parameters and _subsample is the data to be used
#by the algorithm to test its performance in a misfit analysis
np.savetxt(str(filename)+'_'+str(time_stamp)+'_manual.csv',manual_morphology,delimiter=',',header='Distance Along Fault (km),Scarp Height (m), Scarp Width (m), Scarp Slope (deg)')
np.savetxt(str(filename)+'_'+str(time_stamp)+'_subsample.csv',manual_morphology,delimiter=',',header='Distance Along Fault (km),Scarp Height (m), Scarp Width (m), Scarp Slope (deg)')

#Creates variables for isfit analysis

filename=print(str(filename)+'_'+str(time_stamp)+'_manual')

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
