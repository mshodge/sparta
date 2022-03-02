import pandas as pd
from tqdm import tqdm

from scripts.find_scarp import find_scarp
from scripts.utils.smooth_profile import smooth_profile
from scripts.calculate_scarp_profile import calculate_scarp_profile
from scripts.utils.plotting import plot_along_strike_profile

pd.options.mode.chained_assignment = None  # default='warn'


def calculate_morphology(df, params):
    """
    Calculate the along strike morphology of the fault
    :param df <pandas.DataFrame> The DataFrame with the profiles in
    :param params <dict> Dictionary of parameters to use
    """

    height_along = []
    width_along = []
    slope_along = []
    distance_along = []

    total_num_of_profiles = set(list(df['profile']))

    for profile_number in tqdm(total_num_of_profiles):
        set(list(df['profile']))
        profile = df[df['profile'] == profile_number].reset_index()
        profile = smooth_profile(profile, params.get('method'), params.get('bin'))
        profile, crest, base = find_scarp(profile, params.get('theta_t'), params.get('phi_t'))
        height, width, slope = calculate_scarp_profile(profile, crest, base)

        height_along.append(height)
        width_along.append(width)
        slope_along.append(slope)
        distance_along.append(profile['dist_along_fault'].values[0])

    plot_df = pd.DataFrame(
        {'dist_along_fault': distance_along,
         'height': height_along,
         'width': width_along,
         'slope': slope_along
         })

    plot_along_strike_profile(plot_df)
