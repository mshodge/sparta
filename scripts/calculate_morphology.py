from scipy.signal import savgol_filter
from scipy.signal import medfilt
import pandas as pd
import numpy as np
import math
import operator
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt


class CalculateMorphology(object):
    def __init__(self, args):
        self.__args = args
        self.__theta_T_dim = math.tan(math.radians(args.theta_T))
        self.__phi_T_dim = math.tan(math.radians(phi_T))
        self.__nump = int(args.distance_along_profile / args.number_of_profiles)

    def calculate_morphology(self,method,distance,height,bin_size,theta_T,phi_T):

        h = []
        slope = []
        w = []

        if method == 1:
            height_smooth=height
        elif method == 2: #average
            height_smooth=pd.rolling_mean(height,bin_size)
        elif method ==3:
            height_smooth=savgol_filter(height,bin_size,2)
        elif method ==4:
            height_smooth=medfilt(height,bin_size)
        elif method ==5:
            height_smooth=lowess(height,distance,bin_size/nump,it=0)
            height_smooth=height_smooth[:,1]

        #calculate slope
        dzdx = np.diff(height_smooth)
        dzdx = np.hstack((0,dzdx))
        d2zdx2 = np.diff(dzdx)
        d2zdx2 = np.hstack((0,d2zdx2))

        # dzdx < self.__args.theta_T_dim and d2zdx2 < self.__args.phi_T_dim:

        profile = np.hstack((profile, dump))

        last_s=np.empty((1,3))

        if (sum(profile[:,4])>0) and (profile[0,4]==0) and (profile[1,4]==0) and (profile[nump-1,4]==0) and (profile[nump-2,4]==0):
            x1=next((i for i, x in enumerate(profile[:,4]) if x), None) #first non zero element
            x2=index_of_last_nonzero(lst=profile[:,4]) #last non zero element
            y1=profile[x1,1] #first non zero element height
            y2=profile[x2,1] #last non zero element height
        else:
            x1=0
            x2=399
            y1=profile[x1,1] #first non zero element height
            y2=profile[x2,1] #last non zero element height

        upper=np.zeros((nump,4))
        lower=np.zeros((nump,4))
        scarp=np.zeros((nump,4))

        for x in range (0,nump):
            if (sum(profile[:,4])>0) and (profile[0,4]==0) and (profile[1,4]==0) and (profile[nump-1,4]==0) and (profile[nump-2,4]==0):
                if profile[x,0]<x1:
                    upper[x,0]=profile[x,0]
                    upper[x,1]=profile[x,1]
                    upper[x,2]=profile[x,2]
                    upper[x,3]=profile[x,3]
                elif profile[x,0]>x2:
                    lower[x,0]=profile[x,0]
                    lower[x,1]=profile[x,1]
                    lower[x,2]=profile[x,2]
                    lower[x,3]=profile[x,3]
                elif x1<=profile[x,0]<=x2:
                    scarp[x,0]=profile[x,0]
                    scarp[x,1]=profile[x,1]
                    scarp[x,2]=profile[x,2]
                    scarp[x,3]=profile[x,3]

        #save scarp width location values

        #remove zeros
        upper[upper == 0] = 'nan'
        scarp[scarp == 0] = 'nan'
        lower[lower == 0] = 'nan'

        if (sum(profile[:,4])>0) and (profile[0,4]==0) and (profile[1,4]==0) and (profile[nump-1,4]==0) and (profile[nump-2,4]==0):
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

            upper_poly_height = np.polyval(p_upper,distance)
            lower_poly_height = np.polyval(p_lower,distance)
            scarp_poly_height = np.polyval(p_scarp,distance)

        #find point of maximum slope on the scarp, return scarp heights from upper and lower slopes
            ind=np.nanargmin(scarp[:,2])
            h[i]=upper_poly_height[ind,0]-lower_poly_height[ind,0]
            w[i]=(x2+1)-x1
            slope[i]=-math.degrees(math.atan(p_scarp[0]))
        else:
            h[i]=float('nan')
            w[i]=float('nan')
            slope[i]=float('nan')
        if h[i] > 100: #stops very large scarps being picked due to error
            h[i]=float('nan')


    # return h, w, slope

    ### END
