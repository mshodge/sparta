import pytest
from scripts.calculate_scarp_profile import calculate_scarp_profile
from scripts.tests.utils.create_data import create_profile_for_calculating_scarp_morphology


def test_height():
    df, crest, base = create_profile_for_calculating_scarp_morphology()
    height, width, slope = calculate_scarp_profile(df, crest, base)
    assert int(height) == 10

def test_width():
    df, crest, base = create_profile_for_calculating_scarp_morphology()
    height, width, slope = calculate_scarp_profile(df, crest, base)
    assert int(width) == 1

def test_slope():
    df, crest, base = create_profile_for_calculating_scarp_morphology()
    height, width, slope = calculate_scarp_profile(df, crest, base)
    assert int(slope) == -45