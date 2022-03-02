import numpy as np
import math

from scripts.utils.fit_poly import fit_poly


def calculate_scarp_profile(profile, crest, base):
    """
    Calculates the scarp profile height, width and slope
    :param: profile <DataFrame> The DataFrame with profile data in
    :param: crest <int> The location of the crest of the scarp (top)
    :param: base <int> The location of the base of the scarp (bottom)
    :return: height <float> The estimated height of the scarp
    :return: width <float> The estimated width of the scarp
    :return: slope <float> The estimated slope of the scarp
    """

    rmse_upper, upper, upper_poly_height, p_upper = fit_poly(profile, crest, base,
                                                             where = "upper")
    rmse_lower, lower, lower_poly_height, p_lower = fit_poly(profile, crest, base,
                                                             where = "lower")
    rmse_scarp, scarp, scarp_poly_height, p_scarp = fit_poly(profile, crest, base,
                                                             where = "scarp")

    if len(scarp) == 0:
        return None, None, None
    else:
        ind = np.nanargmin(scarp['elevation'])
        height = upper_poly_height[ind] - lower_poly_height[ind]
        width = base - crest
        slope = math.degrees(math.atan(p_scarp[0]))

        return height, width, slope
