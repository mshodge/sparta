import numpy as np
import math
from random import sample
import os
import pandas as pd

from scripts.utils.fit_poly import fit_poly
from scripts.utils.plotting import plot_profiles, plot_along_strike_profile

pd.options.mode.chained_assignment = None


def load_data(filename, dist_between_profiles):
    """
    Loads csv file as a DataFrame
    :param filename: <string> The filename to be loaded
    :param dist_between_profiles: <int> The distance along strike between profiles
    :return: <DataFrame> The DataFrame
    """

    df = pd.read_csv(f"../data/{filename}")
    df['dist_along_fault'] = (df['profile'] - 1) * dist_between_profiles
    return df


def add_row(df, ls):
    """
    Given a DataFrame and a list, append the list as a new row to the DataFrame.
    :param df: <DataFrame> The original DataFrame
    :param ls: <list> The new row to be added
    :return: <DataFrame> The DataFrame with the newly appended row
    """

    num_el = len(ls)
    new_row = pd.DataFrame(np.array(ls).reshape(1, num_el), columns = list(df.columns))
    df = df.append(new_row, ignore_index = True)
    return df


def save_to_csv(df):
    """
    Saves DataFrame to csv file.
    :param df <pandas.DataFrame> A pandas DataFrame to save
    :return: pandas.DataFrame.to_csv
    """

    filename = 'manual.csv'
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', filename)
    return df.to_csv(save_path, index = False)


def manual_analysis(df, num):
    """
    Perform manual analysis on profiles and save height, width and slope features to file
    :param df: <DataFrame> The original DataFrame
    :param num: <int> The number of profiles to perform manual analysis on
    """

    samples_profiles = sample(df['profile'].to_list(), num)
    samples_profiles.sort()

    df_out = pd.DataFrame(columns = ['profile', 'dist_along_fault', 'height', 'width', 'slope'])

    for n, profile_number in enumerate(samples_profiles):

        sample_profile = df[df['profile'] == profile_number]

        dist_along_fault = int(sample_profile['dist_along_fault'].values[0])

        # Calculates the slope and derivative of slope based on the elevation profiles
        dzdx = list(np.insert(np.diff(sample_profile.loc[:, 'elevation']), 0, 0))
        sample_profile['dzdx'] = dzdx

        d2zdx2 = list(np.insert(np.diff(sample_profile.loc[:, 'dzdx']), 0, 0))
        sample_profile['d2zdx2'] = d2zdx2

        base, crest = plot_profiles(sample_profile)

        rmse_upper, upper, upper_poly_height, p_upper = fit_poly(sample_profile, crest[0], base[0], where = "upper")
        rmse_lower, lower, lower_poly_height, p_lower = fit_poly(sample_profile, crest[0], base[0], where = "lower")
        rmse_scarp, scarp, scarp_poly_height, p_scarp = fit_poly(sample_profile, crest[0], base[0], where = "scarp")

        # Finds the point of maximum slope on the scarp, return scarp heights from
        # upper and lower slopes
        ind = np.nanargmin(scarp['elevation'])
        h = upper_poly_height[ind] - lower_poly_height[ind]
        w = base[0] - crest[0]
        slope = math.degrees(math.atan(p_scarp[0]))
        if h > 100:  # stops very large scarps being picked due to error
            h = None

        df_out = add_row(df_out, [profile_number, dist_along_fault, h, w, slope])
        save_to_csv(df_out)

    plot_along_strike_profile(df_out)


if __name__ == '__main__':
    df = load_data(filename = "sample.csv", dist_between_profiles = 100)
    manual_analysis(df, num = 10)
