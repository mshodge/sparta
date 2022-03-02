import pytest
from scripts.find_scarp import find_scarp
from scripts.tests.utils.create_data import create_profile_for_finding_scarp


def test_scarp():
    df, theta_T, phi_T = create_profile_for_finding_scarp()
    df, crest, base = find_scarp(df, theta_T, phi_T)
    assert df['scarp'].to_list() == [0] * 16 + [1] * 2 + [0] * 12

def test_crest():
    df, theta_T, phi_T = create_profile_for_finding_scarp()
    df, crest, base = find_scarp(df, theta_T, phi_T)
    assert base == 18

def test_base():
    df, theta_T, phi_T = create_profile_for_finding_scarp()
    df, crest, base = find_scarp(df, theta_T, phi_T)
    assert crest == 17
