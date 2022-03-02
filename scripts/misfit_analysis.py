import seaborn as sns
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

from scripts.misfit import misfit_calculation


def save_to_csv(df, name):
    """
    Saves DataFrame to csv file.
    :param df <pandas.DataFrame> A pandas DataFrame to save
    :return: pandas.DataFrame.to_csv
    """

    filename = f'misfit_{name}.csv'
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', filename)
    return df.to_csv(save_path, index = False)


def find_best(df, df_manual, methods, bin_max, bin_min,
              bin_step, theta_t_max,
              theta_t_min, theta_t_step, phi_t, criteria_weights,
              plot):
    """
    Finds the best set of parameters to use in the algorithm
    :param: df <DataFrame> The DataFrame with profile data in
    :param: df_manual <DataFrame> The DataFrame with the manual results in to compare to
    :param: methods <list> A list of methods to be used
    :param: bin_max <int> The maximum smoothing bin value to use
    :param: bin_min <int> The minimum smoothing bin value to use
    :param: bin_step <int> The smoothing bin step value to use
    :param: theta_t_max <int> The maximum theta value to use
    :param: theta_t_min <int> The minimum theta value to use
    :param: theta_t_step <int> The theta step value to use
    :param: phi_t <int> The phi value to use
    :param: plot <boolean> Whether to make plots or not
    :param: criteria_weights <list> The list of weights to apply to the results
    """

    for method in methods:
        print(f"Performing misfit analysis for method: {method}")
        for n, profile in tqdm(enumerate(df_manual.profile)):

            profile_number = df_manual['profile'][n]
            profile = df[df['profile'] == profile_number].reset_index()
            profile_manual = df_manual[df_manual['profile'] == profile_number]

            df_tmp = misfit_calculation(profile, profile_manual,
                                        method, bin_max, bin_min,
                                        bin_step, theta_t_max,
                                        theta_t_min, theta_t_step, phi_t,
                                        plot = False, save_file = False)

            try:
                df_out = df_out.append(df_tmp)
            except NameError:
                df_out = df_tmp

    df_out_average = df_out.groupby(['method', 'theta_t', 'bin']).mean().reset_index().drop('profile', axis = 1)

    if plot:
        for method in methods:
            df_out_average_method = df_out_average[df_out_average['method'] == method]
            for value in ['height', 'width', 'slope']:
                df_out_average_plot = df_out_average_method[[f'misfit_{value}', 'bin', 'theta_t']].groupby(
                    ['theta_t', 'bin']).mean().unstack(
                    level = 0)
                df_out_average_plot.columns = df_out_average_plot.columns.droplevel()
                ax = sns.heatmap(df_out_average_plot, linewidths = 0.1, annot = False, cbar = True,
                                 cbar_kws = {'label': f'misfit_{value}'}, vmin = 0, cmap = "viridis")
                ax.set_title(f'{method}')

                plt.show()

    df_out_average['misfit_total'] = \
        df_out_average['misfit_height'] * criteria_weights[0] + \
        df_out_average['misfit_width'] * criteria_weights[1] + \
        df_out_average['misfit_slope'] * criteria_weights[2]

    for criteria in ['total', 'height', 'width', 'slope']:
        best_value = min(df_out_average[f'misfit_{criteria}'])
        the_best = df_out_average[df_out_average[f'misfit_{criteria}'] == best_value]
        print(f'\nThe best parameters using criteria {criteria} are:')
        print(the_best.to_string())

        try:
            df_out_best = df_out_best.append(the_best)
        except NameError:
            df_out_best = the_best

    save_to_csv(df_out_average, name = 'all')
    save_to_csv(df_out_best, name = 'best')

