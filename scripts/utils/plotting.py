import matplotlib.pyplot as plt
import numpy as np


def tellme(s):
    """
    Prints a string to a plot
    :param s: <string> The title to be printed
    """

    plt.title(s, fontsize = 16)
    plt.draw()


def plot_profiles(df):
    """
    Plots the elevation, dzdx and d2zdx2 of the scarp and asks user to select the scarp location for manual analysis
    :param: <DataFrame> The DataFrame with the data in
    """

    plt.clf()
    plt.figure(1)
    plt.subplot(3, 1, 1)
    plt.scatter(df['dist'], df['elevation'], s = .5, facecolors = 'none', edgecolors = 'k')
    plt.plot(df['dist'], df['elevation'], color = 'k', linewidth = 0.5)
    plt.ylabel('Height (m)', fontsize = 8)
    plt.xticks([])
    plt.yticks(size = 8)
    plt.tight_layout()

    tellme('Select the scrap top, then bottom. Click to begin.')

    plt.subplot(3, 1, 2)
    plt.scatter(df['dist'], df['dzdx'], s = .5, facecolors = 'none', edgecolors = 'k')
    plt.ylabel('dz/dx ($^\circ$)', fontsize = 8)
    plt.xticks([])
    plt.yticks(size = 8)
    plt.subplot(3, 1, 3)
    plt.scatter(df['dist'], df['d2zdx2'], s = .5, facecolors = 'none', edgecolors = 'k')
    plt.ylabel('d2z/dx2 ($^\circ$/m)', fontsize = 8)
    plt.xlabel('Distance (m)', fontsize = 8)
    plt.xticks(size = 8)
    plt.yticks(size = 8)

    pts = []
    pts = plt.ginput(3, timeout = 0)  # it will wait for three clicks
    pts = np.array(pts)
    if len(pts) == 3:
        plt.close()

    # Saves the user specified location of the crest and the base
    base = [pts[1, 0], pts[1, 1]]
    crest = [pts[0, 0], pts[0, 1]]

    return base, crest


def plot_along_strike_profile(df):
    """
    Plots an along strike profile for height, width and slope for the fault scarp
    :param: <DataFrame> The DataFrame with the data in
    """

    for n, metric in enumerate(['height', 'width', 'slope']):
        df[f'{metric}_smooth'] = df[metric].rolling(10, min_periods = 1).mean()
        plt.subplot(3, 1, n + 1)
        plt.scatter(df['dist_along_fault'], df[metric], s = 5, facecolors = 'none', edgecolors = 'k')
        plt.plot(df['dist_along_fault'], df[f'{metric}_smooth'])
        plt.ylabel(f'Scarp {metric}', fontsize = 8)
        plt.title(f'Along fault scarp {metric} profile', fontsize = 8)
        plt.subplots_adjust(hspace = 1)
        plt.xticks(size = 8)
        plt.yticks(size = 8)

        if n == 2:
            plt.xlabel(f'Distance along fault', fontsize = 8)
            plt.ylim(top = 0)

        else:
            plt.ylim(bottom = 0)

    plt.show()
