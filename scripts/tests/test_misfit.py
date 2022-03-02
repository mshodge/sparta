import pytest
from scripts.tests.utils.create_data import create_profile_for_calculating_misfit, create_manual_profile_for_calculating_misfit
from scripts.misfit import misfit_calculation


def test_misfit_calculation_average():
    profile = create_profile_for_calculating_misfit()
    profile_manual = create_manual_profile_for_calculating_misfit()
    misfit_df = misfit_calculation(profile, profile_manual,
                       method = "average", bin_max = 11, bin_min = 5, bin_step = 2, theta_T_max = 40,
                       theta_T_min = 30, theta_T_step = 2, phi_T = 5, plot = False, save_file = False)

    misfit_df['misfit_height'] = misfit_df['misfit_height'].fillna(0).astype(int)
    misfit_df['misfit_width'] = misfit_df['misfit_width'].fillna(0).astype(int)
    misfit_df['misfit_slope'] = misfit_df['misfit_slope'].fillna(0).astype(int)
    misfit_df['misfit_total'] = misfit_df['misfit_total'].fillna(0).astype(int)

    assert misfit_df.loc[0].to_list() == [1, 'average', 1, 6, 1, 30, 5, 8]


def test_misfit_calculation_savgol():
    profile = create_profile_for_calculating_misfit()
    profile_manual = create_manual_profile_for_calculating_misfit()
    misfit_df = misfit_calculation(profile, profile_manual,
                                   method = "savgol", bin_max = 11, bin_min = 5, bin_step = 2, theta_T_max = 40,
                                   theta_T_min = 30, theta_T_step = 2, phi_T = 5, plot = False, save_file = False)

    misfit_df['misfit_height'] = misfit_df['misfit_height'].fillna(0).astype(int)
    misfit_df['misfit_width'] = misfit_df['misfit_width'].fillna(0).astype(int)
    misfit_df['misfit_slope'] = misfit_df['misfit_slope'].fillna(0).astype(int)
    misfit_df['misfit_total'] = misfit_df['misfit_total'].fillna(0).astype(int)

    assert misfit_df.loc[0].to_list() == [1, 'savgol', 1, 5, 4, 30, 5, 10]


def test_misfit_calculation_median():
    profile = create_profile_for_calculating_misfit()
    profile_manual = create_manual_profile_for_calculating_misfit()
    misfit_df = misfit_calculation(profile, profile_manual,
                                   method = "median", bin_max = 11, bin_min = 5, bin_step = 2, theta_T_max = 40,
                                   theta_T_min = 30, theta_T_step = 2, phi_T = 5, plot = False, save_file = False)

    misfit_df['misfit_height'] = misfit_df['misfit_height'].fillna(0).astype(int)
    misfit_df['misfit_width'] = misfit_df['misfit_width'].fillna(0).astype(int)
    misfit_df['misfit_slope'] = misfit_df['misfit_slope'].fillna(0).astype(int)
    misfit_df['misfit_total'] = misfit_df['misfit_total'].fillna(0).astype(int)

    assert misfit_df.loc[0].to_list() == [1, 'median', 0, 0, 0, 30, 5, 0]


def test_misfit_calculation_lowess():
    profile = create_profile_for_calculating_misfit()
    profile_manual = create_manual_profile_for_calculating_misfit()
    misfit_df = misfit_calculation(profile, profile_manual,
                                   method = "lowess", bin_max = 11, bin_min = 5, bin_step = 2, theta_T_max = 40,
                                   theta_T_min = 30, theta_T_step = 2, phi_T = 5, plot = False, save_file = False)

    misfit_df['misfit_height'] = misfit_df['misfit_height'].fillna(0).astype(int)
    misfit_df['misfit_width'] = misfit_df['misfit_width'].fillna(0).astype(int)
    misfit_df['misfit_slope'] = misfit_df['misfit_slope'].fillna(0).astype(int)
    misfit_df['misfit_total'] = misfit_df['misfit_total'].fillna(0).astype(int)

    assert misfit_df.loc[0].to_list() == [1, 'lowess', 1, 5, 4, 30, 5, 10]


def test_misfit_calculation_no_smoothing():
    profile = create_profile_for_calculating_misfit()
    profile_manual = create_manual_profile_for_calculating_misfit()
    misfit_df = misfit_calculation(profile, profile_manual,
                                   method = None, bin_max = 11, bin_min = 5, bin_step = 2, theta_T_max = 40,
                                   theta_T_min = 30, theta_T_step = 2, phi_T = 5, plot = False, save_file = False)

    misfit_df['misfit_height'] = misfit_df['misfit_height'].fillna(0).astype(int)
    misfit_df['misfit_width'] = misfit_df['misfit_width'].fillna(0).astype(int)
    misfit_df['misfit_slope'] = misfit_df['misfit_slope'].fillna(0).astype(int)
    misfit_df['misfit_total'] = misfit_df['misfit_total'].fillna(0).astype(int)

    assert misfit_df.loc[0].to_list() == [1, None, 0, 0, 0, 30, 5, 0]