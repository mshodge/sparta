import numpy as np
import math


def find_scarp(df, theta_T, phi_T):
    """
    Finds the scarp from a profile using theta and phi values
    :param: profile <DataFrame> The DataFrame with profile data in
    :param: theta_T <int> The value of dxdz
    :param: phi_T <int> The value of d2xdz2
    :return: df <DataFrame> The DataFrame with the estimated scarp location in
    :return: crest <int> The estimated location of the crest of the scarp (top)
    :return: base <int> The estimated location of the base of the scarp (bottom)
    """

    theta_T_dimensionless = math.tan(math.radians(theta_T))
    phi_T_dimensionless = math.tan(math.radians(phi_T))

    # calculate slope
    df['dzdx'] = list(np.abs(np.insert(np.diff(df.loc[:, ('elevation_smooth')]), 0, 0)))
    df['d2zdx2'] = list(np.abs(np.insert(np.diff(df.loc[:, ('dzdx')]), 0, 0)))

    scarp = []
    for index, row in df.iterrows():
        if 10 < index < len(df) - 10:
            if row['dzdx'] > theta_T_dimensionless:
                if row['d2zdx2'] > phi_T_dimensionless:
                    scarp.append(1)
                else:
                    scarp.append(0)
            else:
                scarp.append(0)
        else:
            scarp.append(0)

    df['scarp'] = scarp

    try:
        crest = int(df.loc[np.min(np.nonzero(scarp)), 'dist'])
    except ValueError:
        crest = None

    try:
        base = int(df.loc[np.max(np.nonzero(scarp)), 'dist'])
    except ValueError:
        base = None

    return df, crest, base
