# Config variables

# needs to be an odd int (recommended: 35)
bin_max = 35

# needs to be an odd int (recommended: 9)
bin_min = 9

# needs to be an even int (recommended: 2)
bin_step = 2

# needs to be a positive int (recommended: 50)
theta_T_max = 50

# needs to be a positive int (recommended: 12)
theta_T_min = 12

# needs to be a positive int (recommended: 2)
theta_T_step = 2

# needs to be a positive int (recommended: 5)
phi_T = 5

# list of either average, savgol, median, and/or lowess
methods = ["average", "savgol"]

# weights between 0 and 1 for height, width and slope
criteria_weights = [0.6, 0.3, 0.1]
