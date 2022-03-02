import pandas as pd


def create_profile_for_finding_scarp():
    df = pd.DataFrame({"elevation_smooth": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                9, 8, 7, 6, 5, 4, 2, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       "dist": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
                       })
    theta_T = 0.5
    phi_T = 0.5
    return df, theta_T, phi_T


def create_profile_for_calculating_scarp_morphology():
    df = pd.DataFrame({"elevation": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                9, 8, 7, 6, 5, 4, 2, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       "dist": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                       })
    crest = 17
    base = 18
    return df, crest, base


def create_profile_for_calculating_misfit():
    df = pd.DataFrame({"profile": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       "elevation": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                9, 8, 7, 6, 5, 4, 2, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       "dist": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                       })
    return df

def create_manual_profile_for_calculating_misfit():
    df = pd.DataFrame({"profile": [1],
                       "dist_along_fault": [1],
                       "height": [10],
                       "width": [1],
                       "slope": [-45]
                       })
    return df