import pandas as pd
import os

def load_data(filename, dist_between_profiles):

    path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    df = pd.read_csv(path)
    df['dist_along_fault'] = (df['profile'] - 1) * dist_between_profiles
    return df
