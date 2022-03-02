import argparse
import pandas as pd
import os

from scripts.utils.read_data import load_data
from scripts.manual_analysis import manual_analysis
from scripts.misfit_analysis import find_best
from scripts.calculate_morphology import calculate_morphology
from scripts.utils.argschecker import argschecker
from config import config


def main(filename, manual, distance_between_profiles, number_of_profiles, misfit, morphology, plot):

    df = load_data(filename = filename, dist_between_profiles = int(distance_between_profiles))

    if manual:
        manual_analysis(df, num = int(number_of_profiles))

    if misfit:
        path = os.path.join(os.path.dirname(__file__), "outputs", "manual.csv")
        df_manual = pd.read_csv(path)

        find_best(df, df_manual, config.methods, config.bin_max, config.bin_min,
                  config.bin_step, config.theta_T_max,
                  config.theta_T_min, config.theta_T_step, config.phi_T, config.criteria_weights,
                  plot)

    if morphology:
        bin_value = input("please enter the smoothing bin value to use:\n")
        theta_t_value = input("please enter the theta value to use:\n")
        phi_t_value = input("please enter the phi value to use (default is 5):\n")
        method_value = input("please enter the method to use (average, savgol, median, lowess):\n")

        params = {
            "bin": int(bin_value),
            "theta_t": int(theta_t_value),
            "phi_t": int(phi_t_value),
            "method": method_value
        }

        calculate_morphology(df, params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', default = None,
                        help = 'The filename of the profiles to analyse.')
    parser.add_argument('-manual', action = 'store_true', default = False,
                        help = 'Whether to perform the manual analysis or not.')
    parser.add_argument('-d', default = None,
                        help = 'Distance between profiles.')
    parser.add_argument('-n', default = None,
                        help = 'Number of profiles to manually analyse.')
    parser.add_argument('-misfit', action = 'store_true', default = False,
                        help = 'Whether to perform the misfit analysis or not.')
    parser.add_argument('-morphology', action = 'store_true', default = False,
                        help = 'Whether to perform along strike morphological analysis or not.')
    parser.add_argument('-p', action = 'store_true', default = False,
                        help = 'Whether to create plots or not for misfit analysis.')
    args = parser.parse_args()

    argschecker(args)

    main(filename = args.filename, manual = args.manual, distance_between_profiles = args.d,
             number_of_profiles = args.n, misfit = args.misfit, morphology = args.morphology, plot = args.p)
