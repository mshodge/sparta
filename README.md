# <b><u>S</b></u>carp <b><u>PAR</b></u>ame<b><u>T</b></u>er <b><u>A</b></u>lgorithm (SPARTA)

A semi-automated algorithm to calculate fault scarp morphological parameters (height, width and slope) from
two-dimensional elevation profiles extracted from a digital elevation model (DEM), and produce an along-strike profile.


## Get

1. To clone locally use:

    ```git clone https://github.com/mshodge/sparta```

## Set

1. Install requirements to your chosen virtual environment:

    ```pip install -r requirements.txt```


2. Put your csv file with scarp profiles in `data` folder. The folder contains information about the schema needed.
 See `data/sample.csv` for example.

3. Update `config/config.py` with your chosen variables.


## Go

1. To run:

    ```
    python sparta.py <args>
    ```

    Where `<args>` are:

        - `-filename`: the filename of your csv
        - `-manual`: if you want to process profiles manually so you can perform a misfit analysis
        - `-d`: the distance between profiles along strike
        - `-n`: the number of profiles you want to analyse manually
        - `-misfit`: if you want to perform a misfit analysis to find the best performing parameters
        - `-morphology`: to calculate the along strike scarp morphology

    This will save the outputs to the `/outputs/` folder.

## Additional Information

### Elevation Profiles

Profiles can be oriented as desired; typically they are oriented either perpendicular to the local scarp trend
(if slip direction is unknown), or perpendicular to the slip direction. Please note profiles length (in meters) and
distance between elevation measurement points, which should be equal to the DEM resolution.

### Smoothing

This algorithm applies a smoothing method to the scarp profiles. There are five filters to choose from:

- `average`: rolling mean algorithm from the pandas Python module
- `savgol`: (Savitzky–Golay) local least-squares polynomial approximation; it is less aggressive than simple moving
filters and is therefore better at preserving data features such as peak height and width
- `median`: moving median algorithm from the SciPy Python module
- `lowess`: a non-parametric regression method and requires larger sample sizes than the other filters (Cleveland, 1981).
Can be performed iteratively, but here set to a single pass for computational efficiency.

