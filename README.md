# FaultScarpAlgorithm (FAST)

A semi-automated algorithm to calculate fault scarp morphological parameters (height, width and slope) from two-dimensional elevation profiles extracted from a digital elevation model (DEM), and produce an along-strike profile.

### Elevation Profiles

Profiles can be oriented as desired; typically they are oriented either perpendicular to the local scarp trend (if slip direction is unknown), or perpendicular to the slip direction. Please note profiles length (in meters) and distance between elevation measurement points, which should be equal to the DEM resolution.

## The Algorithm

This repository contains 7 .py files, 2 are the algorithm calculation files and 5 the step-by-step processes. The algorithm can be run
simply by using only 2 step-by-step processes (#1 and #5), but for the best performance, please run from #1 to #5.

### Packages used

The following codes use the following packages:

copy

datetime

last_zero

math

matplotlib

numpy

operator

pandas

pickle

pylab

scipy

sklearn

statsmodels

### #1_Read_Data.py

This script loads in the elevation data from a specified .csv file within the same location as the saved script. The csv file should be presented in a two column format (1: Distance along the elevation profile; 2: Height in meters), where the first row contains the header information. In line 22 please replace <i><b>FILENAME HERE</i></b> with the name of the csv file. If the csv file does not have a header row, change skip_header=1 to skip_header=0 (line 26). <b>NOTE</b>: Some GIS elevation profile extraction tools may give the elevation distance in reverse order (e.g., 400 to 1, rather than 1 to 400), if so, line 32 should be changed to reverse = 1. State the DEM resolution (i.e., the distance between elevation measurements) in line 35, and the length of the elevation profile in line 38. The distance between profiles along the fault should be given in line 41. 

### #2_Manual_Analysis.py

This script can be used to calculate the scarp morphological parameters manually for all profiles (not recommended) or to measure a subsample of elevation profiles for the misfit analysis (highly recommended). Specify the number of manual measurements in line 19. The larger the number of manual measurements, the better the misfit analysis. Running the script will produce an figure for each subsampled profile; the top panel will be the elevation profile; the middle panel the slope profile; and the bottom panel the derivative of slope profile. If the elevation profile is backward, please alter the value in line 32 of #1_Read_Data.py. For each profile, please click the bottom of, then the top of the scarp on the elevation profile (top panel), then click anywhere to load the next profile.

After all subsampled profiles have been analysed manually, an along-strike profile will be generated. The results will also be saved in a csv file with the prefix of the filename you loaded in #1_Read_Data.py and the suffix <b><<TIME STAMP>>_manual</b>, where <b><<TIME STAMP>></b> was the date the data was loaded in #1_Read_Data.py. Please rename manually if you are running multiple analyses on the same data.

<b>NOTE</b>: If this script has been run, skip #3_Load_Manual_Analysis.py and go to #4_Misfit_Analysis.py.

### #3_Load_Manual_Analysis.py

This script loads a previously performed manual analysis. Replace <i><b>FILENAME HERE</b></i> in line 18 with the relevant filename.

### #4_Misfit_Analysis.py

This script performs the misfit analysis between the manual analysis and the algorithm to identify the best performing parameter space for the fault scarp. The misfit analysis is based on the subsampled number given in #2_Manual_Analysis.py. 

Please alter the values in lines 44 to 50 to change the parameter space. The algorithm uses a filter to improve the signal-to-noise ratio on the elevation profiles. Each filter (see below for definitions) uses a moving window, where the size of the window is termed the bin width. Lines 44 to 46 therefore relate to the bin width minimum, maximum and step. As the bin width must be an odd integer, the minimum value must be odd and the step, even. The algorithm then uses a slope and derivative of slope threshold to identify the scarp. As the derivative of slope threshold is deemed to be less sensitive (following filtering) it is fixed (line 50). The default value of 5 should be sufficient. For the slope threshold, the minimum, maximum and step can be changed in lines 47 to 49. The values given here are positive integers, which will be changed to negative values within the algorithm.

<b>NOTE</b>: Choosing a large range (difference between maximum and minimum) and step will dramatically increase computational time. For best practice, choose a large step and perform multiple misfit analyses where the parameter space becomes more focused.

The misfit analysis compares two filter types at a time. There are five filters to choose from:

method = 1: No filter - no filter is applied 

method = 2: Average - rolling mean algorithm from the pandas Python module

method = 3: Savitzky–Golay - local least-squares polynomial approximation; it is less aggressive than simple moving filters and is therefore better at preserving data features such as peak height and width

method = 4: Median - moving median algorithm from the SciPy Python module

method = 5: Lowess - a non-parametric regression method and requires larger sample sizes than the other filters (Cleveland, 1981). 
                      Can be performed iteratively, but here set to a single pass for computational efficiency.

Lines 61 to 84 should be commented/uncommented as appropriate to the first chosen filter, and lines 93 to 116 for the second filter.

After the misfit analysis has completed, the best parameter space will be shown in the console in the form:

<i>Best Parameter Space:

method = 

bin size = 

slope threshold = 

average misfit height (m) =

average misfit width (m) =

average misfit slope (degrees) =

misfit count =</i>

These parameters will also be saved as variables for the final algorithm run. Two additional figures will be produced, one where the
entire parameter space performance is shown for both filters, and one where the best parameter space scarp morphological parameters
are compared to the manual analysis for the along-strike profile.

### #5_Calculate_Morphology.py

This is the final script, which is used to calculate the scarp morphological parameters for the entire dataset (from the original csv loaded in #1_Load_Data.py) based on either the best performing parameters from #4_Misfit_Analysis.py (recommended) or from values specified in lines 32 to 35 (not recommended unless based on a misfit analysis that was performed previously). 

Raw results are then displayed in an along-strike profile, as well as quality-checked results. Quality-checked results are those where 'bad data' has been removed. 'Bad data' comprises results where negative scarp heights or positive scarp slopes are recorded, or scarps whose widths are wider than twice the maximum width found in the manual analysis, or if the measurements are greater than 2 standard deviations from the mean. Both are displayed as figures and saved with the suffix 'morphology.csv' and 'morphology_qualitychecked.csv'

### Algorithm_misfit.py

The algorithm used in #4_Misfit_Analysis.py

### Algorithm.py

The algorithm used in #5_Calculate_Morphology.py

