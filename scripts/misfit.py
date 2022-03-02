import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from scripts.find_scarp import find_scarp
from scripts.utils.smooth_profile import smooth_profile
from scripts.calculate_scarp_profile import calculate_scarp_profile


def save_to_csv(df, method, profile):
    """
    Saves DataFrame to csv file.
    :param df <pandas.DataFrame> A pandas DataFrame to save
    :return: pandas.DataFrame.to_csv
    """

    filename = f'misfit_{method}_{profile}.csv'
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', filename)
    return df.to_csv(save_path, index = False)


def misfit_calculation(profile, profile_manual,
                       method, bin_max, bin_min, bin_step, theta_T_max,
                       theta_T_min, theta_T_step, phi_T, plot, save_file):
    """
    Calculates the misfit for a profile between the algorithm and the manual analysis
    :param: profile <DataFrame> The DataFrame with profile data in
    :param: profile_manual <DataFrame> The DataFrame with the manual results in to compare to
    :param: method <string> The method to be used
    :param: bin_max <int> The maximum smoothing bin value to use
    :param: bin_min <int> The minimum smoothing bin value to use
    :param: bin_step <int> The smoothing bin step value to use
    :param: theta_T_max <int> The maximum theta value to use
    :param: theta_T_min <int> The minimum theta value to use
    :param: theta_T_step <int> The theta step value to use
    :param: phi_T <int> The phi value to use
    :param: plot <boolean> Whether to make plots or not
    :param: save_file <boolean> Whether to save the file or not
    :return: misfit_df <DataFrame> The misfit DataFrame
    """

    misfit_height = []
    misfit_width = []
    misfit_slope = []
    theta_t_list = []
    bin_list = []
    method_list = []

    bin_it_list = list(range(bin_min, bin_max + 1, bin_step))
    theta_t_it_list = list(range(theta_T_min, theta_T_max + 1, theta_T_step))

    for bin_run_num, bin in enumerate(bin_it_list):
        for theta_run_num, theta_T in enumerate(theta_t_it_list):

            profile = smooth_profile(profile, method, bin)

            profile, crest, base = find_scarp(profile, theta_T, phi_T)

            if base is not None and crest is not None:
                height, width, slope = calculate_scarp_profile(profile, crest, base)

                misfit_height.append(abs(height - profile_manual['height'].values[0]))
                misfit_width.append(abs(width - profile_manual['width'].values[0]))
                misfit_slope.append(abs(slope - profile_manual['slope'].values[0]))
                method_list.append(method)
                theta_t_list.append(theta_T)
                bin_list.append(bin)

            else:
                misfit_height.append(None)
                misfit_width.append(None)
                misfit_slope.append(None)
                method_list.append(method)
                theta_t_list.append(theta_T)
                bin_list.append(bin)


    misfit_df = pd.DataFrame(
        {'profile': profile.profile[0],
         'method': method_list,
         'misfit_height': misfit_height,
         'misfit_width': misfit_width,
         'misfit_slope': misfit_slope,
         'theta_t': theta_t_list,
         'bin': bin_list
         })

    if plot:
        for value in ['height', 'width', 'slope']:
            df_plot = misfit_df[[f'misfit_{value}', 'bin', 'theta_t']].groupby(['theta_t', 'bin']).mean().unstack(
                level = 0)
            df_plot.columns = df_plot.columns.droplevel()
            ax = sns.heatmap(df_plot, linewidths = 0.1, annot = False, cbar = True,
                             cbar_kws = {'label': f'misfit_{value}'}, vmin = 0, cmap = "viridis")
            plt.show()

    misfit_df['misfit_total'] = misfit_df['misfit_height'] + misfit_df['misfit_width'] + misfit_df['misfit_slope']

    if save_file:
        save_to_csv(misfit_df, method, profile_number)
    return misfit_df

