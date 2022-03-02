from sklearn.metrics import mean_squared_error
import numpy as np
import warnings

warnings.simplefilter('ignore', np.RankWarning)

def fit_poly(profile, crest, base, where):
    """
    Fits a polynomial line to a surface of a scarp
    :param profile: <DataFrame> The profile of the scarp
    :param crest: <int> The estimated location of the scarp crest (top)
    :param crest: <int> The estimated location of the scarp base (bottom)
    :param where: <string> Whether to fit the polynomial to the upper surface, lower surface or scarp
    :return: rmse <float> The root mean squared error between the surface and the polynomial
    :return: surface <DataFrame> The DataFrame of the surface
    :return: poly_height <ndarray> The surface height
    :return: p <ndarray> The polynomial coefficients
    """

    if where == "upper":
        surface = profile[profile['dist'] < crest]
    elif where == "lower":
        surface = profile[profile['dist'] > base]
    else:
        surface = profile[profile['dist'] <= base]
        surface = surface[surface['dist'] >= crest]

    x = surface.dist.values
    y = surface.elevation.values
    if len(x) > 0 and len(y) > 0:
        idx = np.isfinite(x) & np.isfinite(y)
        p = np.polyfit(x[idx], y[idx], 1)
        min_ind = np.nanargmin(x)
        max_ind = np.nanargmax(x)
        poly_height_surface = np.polyval(p, surface['dist'])
        poly_height = np.polyval(p, profile['dist'])
        if len(x) > 1 and len(y) > 1:
            rmse = mean_squared_error(surface['elevation'].values[min_ind:max_ind],
                                      poly_height_surface[min_ind:max_ind])
        else:
            rmse = None
    else:
        rmse = None
        poly_height = None
        p = None
    return rmse, surface, poly_height, p
