import random
import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import ginput
from sklearn.metrics import mean_squared_error
import pandas as pd


class ManualAnalysis(object):
    def __init__(self, args, profiles, number_of_profiles, distance_between_profiles, distance_along_profile,
                 manual_profiles_percent, reverse, profile_start_index_numbers, profile_end_index_numbers):
        self.__args = args
        self.__profiles = profiles
        self.__manual_profiles_percent = manual_profiles_percent
        self.__distance_between_profiles = distance_between_profiles
        self.__number_of_profiles = number_of_profiles
        self.__distance_along_profile = distance_along_profile
        self.__manual_profiles_percent = manual_profiles_percent
        self.__reverse = reverse
        self.__profile_start_index_numbers = profile_start_index_numbers
        self.__profile_end_index_numbers = profile_end_index_numbers


    def random_profile_start_numbers(self, number_of_profiles_to_sample):
        list_random_profile_start_numbers = []
        for x in range(number_of_profiles_to_sample):
            list_random_profile_start_numbers.append(random.randint(0, self.__number_of_profiles) * 1)
        return list_random_profile_start_numbers

    def get_profile(self, profiles, start, end):
        profile = profiles.iloc[start:end]
        return profile

    def split_profiles(self, distance, height, dzdx, d2zdx2, start, end):
        distance_split = distance[start:end]
        height_split = height[start:end]
        dzdx_split = dzdx[start:end]
        d2zdx2_split = d2zdx2[start:end]
        return distance_split, height_split, dzdx_split, d2zdx2_split

    def plot_profile(self, distance, height, dzdx, d2zdx2):
        # plots the elevation, slope and derivative of slope and asks the user to
        # click the top, then bottom of the scarp, third click to finish
        plt.figure(1)
        plt.subplot(3, 1, 1)
        plt.scatter(distance, height, s=.5, facecolors='none', edgecolors='k')
        plt.plot(distance, height, color='k', linewidth=0.5)
        plt.ylabel('Height (m)', fontsize=8)
        plt.xticks([])
        plt.yticks(size=8)
        plt.tight_layout()
        plt.subplot(3, 1, 2)
        plt.scatter(distance, dzdx, s=.5, facecolors='none', edgecolors='k')
        plt.ylabel('dz/dx ($^\circ$)', fontsize=8)
        plt.xticks([])
        plt.yticks(size=8)
        plt.subplot(3, 1, 3)
        plt.scatter(distance, d2zdx2, s=.5, facecolors='none', edgecolors='k')
        plt.ylabel('d2z/dx2 ($^\circ$/m)', fontsize=8)
        plt.xlabel('Distance (m)', fontsize=8)
        plt.xticks(size=8)
        plt.yticks(size=8)

        pts = ginput(2)  # it will wait for three clicks
        pts = np.array(pts)
        plt.close()
        # print("clicked", pts)

        return pts

    def calculate_morphology(self):

        crest = []
        base = []
        profile_num = []
        dist_along_fault = []
        h = []
        slope = []
        w = []
        rmse_upper = []
        rmse_lower = []
        rmse_scarp = []
        rmse_av = []

        list_random_profile_start_numbers = self.random_profile_start_numbers(int(self.__number_of_profiles/
                                                                                  self.__manual_profiles_percent))

        n = 0

        for profile_number in list_random_profile_start_numbers:
            dist_along_fault.append(profile_number * int(self.__distance_between_profiles))
            profile_num.append(profile_number)
            profile = self.get_profile(self.__profiles, self.__profile_start_index_numbers[profile_number],
                                       self.__profile_end_index_numbers[profile_number])

            distance = profile['x'].values
            height = profile['y'].values

            # Calculates the slope and derivative of slope based on the elevation profiles
            dzdx = np.diff(height)
            dzdx = np.hstack((0, dzdx))
            d2zdx2 = np.diff(dzdx)
            d2zdx2 = np.hstack((0, d2zdx2))

            pts = self.plot_profile(distance, height, dzdx, d2zdx2)

            # Saves the user specified location of the crest and the base
            crest.append([pts[1, 0],pts[1, 1]])
            base.append([pts[0, 0],pts[0, 1]])

            distance_upper, height_upper, dzdx_upper, d2zdx2_upper = self.split_profiles(distance, height, dzdx, d2zdx2,
                                                                                         0, int(crest[n][0]))
            distance_lower, height_lower, dzdx_lower, d2zdx2_lower = self.split_profiles(distance, height, dzdx, d2zdx2,
                                                                                         int(base[n][0]),
                                                                                         distance.size)
            distance_scarp, height_scarp, dzdx_scarp, d2zdx2_scarp = self.split_profiles(distance, height, dzdx, d2zdx2,
                                                                                         int(crest[n][0]),
                                                                                         int(base[n][0]))


            p_upper = np.polyfit(distance_upper, height_upper, 1);
            p_lower = np.polyfit(distance_lower, height_lower, 1);
            p_scarp = np.polyfit(distance_scarp, height_scarp, 1);

            # Extrapolates the regression line for each surface
            upper_poly_height = np.polyval(p_upper, distance)
            lower_poly_height = np.polyval(p_lower, distance)
            scarp_poly_height = np.polyval(p_scarp, distance)

            upper_min_ind = np.nanargmin(distance_upper)
            upper_max_ind = np.nanargmax(distance_upper)+1
            lower_min_ind = np.nanargmin(distance_lower)
            lower_max_ind = np.nanargmax(distance_lower)+1
            scarp_min_ind = np.nanargmin(distance_scarp)
            scarp_max_ind = np.nanargmax(distance_scarp)+1

            rmse_upper.append(mean_squared_error(height_upper,
                                               upper_poly_height[upper_min_ind:upper_max_ind]))
            rmse_lower.append(mean_squared_error(height_lower,
                                               lower_poly_height[lower_min_ind:lower_max_ind]))
            rmse_scarp.append(mean_squared_error(height_scarp,
                                               scarp_poly_height[scarp_min_ind:scarp_max_ind]))
            rmse_av.append((rmse_upper[n] + rmse_lower[n]) / 2)

            ind = np.nanargmin(dzdx_scarp)
            h.append(upper_poly_height[ind] - lower_poly_height[ind])
            w.append(base[n][0] - crest[n][0])
            slope.append(math.degrees(math.atan(p_scarp[0])))
            if h[n] > 100:  # stops very large scarps being picked due to error
                h[n] = float('nan')

            n = n + 1

        plt.figure(2)  # plot manual data
        plt.subplot(3, 1, 1)
        plt.scatter(dist_along_fault, h, s=5, facecolors='none', edgecolors='k')
        plt.ylabel('Scarp Height (m)', fontsize=8)
        plt.title('Manual Scarp Height Profile', fontsize=8)
        plt.ylim([0, np.int(math.ceil(np.amax(h) / 10.0)) * 10])
        plt.subplots_adjust(hspace=1)
        plt.xticks(size=8)
        plt.yticks(size=8)
        plt.subplot(3, 1, 2)
        plt.scatter(dist_along_fault, w, s=5, facecolors='none', edgecolors='k')
        plt.ylabel('Scarp Width (m)', fontsize=8)
        plt.title('Manual Scarp Width Profile', fontsize=8)
        plt.ylim([0, np.int(math.ceil(np.amax(w) / 10.0)) * 10])
        plt.subplots_adjust(hspace=1)
        plt.xticks(size=8)
        plt.yticks(size=8)
        plt.subplot(3, 1, 3)
        plt.scatter(dist_along_fault, slope, s=5, facecolors='none', edgecolors='k')
        plt.xlabel('Distance along fault (km)', fontsize=8)
        plt.ylabel('Scarp Slope ($^\circ$)', fontsize=8)
        plt.title('Manual Scarp Slope Profile', fontsize=8)
        plt.subplots_adjust(hspace=1)
        plt.xticks(size=8)
        plt.yticks(size=8)
        plt.ylim([(np.int(math.ceil(np.amin(slope) / 10.0)) * 10) - 10, 0])

        # Stacks the variables
        df = pd.DataFrame({
            'profile': profile_num,
            'distance': dist_along_fault,
            'height': h,
            'width': w,
            'slope': slope,
            'rmse_upper': rmse_upper,
            'rmse_lower': rmse_lower,
            'rmse_scarp': rmse_scarp,
            'rmse_average': rmse_av
        })

        df.to_csv('outputs/manual_analysis/' + self.__args.profile[:-4] + '_manual.csv', index=False)
