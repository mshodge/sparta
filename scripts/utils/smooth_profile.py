from scipy.signal import savgol_filter
from scipy.signal import medfilt
from statsmodels.nonparametric.smoothers_lowess import lowess


def smooth_profile(df, method, bin):
    """
    Smoothes the profile based on the method chosen
    :param: df <DataFrame> The DataFrame with profile data in
    :param: method <string> The method to be used, either average, savgol, median, or lowess (or None)
    :param: bin <int> The  smoothing bin value to use
    :return: df <DataFrame> The DataFrame with the smoothed value in
    """

    distance = df['dist']
    elevation = df['elevation']

    if method == 'average':  # average
        df['elevation_smooth'] = elevation.rolling(bin).mean()
    elif method == 'savgol':
        df['elevation_smooth'] = savgol_filter(elevation, bin, 2)
    elif method == 'median':
        df['elevation_smooth'] = medfilt(elevation, bin)
    elif method == 'lowess':
        elevation_smooth = lowess(elevation, distance, bin / len(df), it = 0)
        df['elevation_smooth'] = elevation_smooth[:, 1]
    else:
        df['elevation_smooth'] = elevation

    return df
