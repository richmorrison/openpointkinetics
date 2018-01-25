"""Logging and plotting module."""
import matplotlib.pyplot as plt
import numpy as np


class Logger:
    """Data logging class."""

    def __init__(self):
        self.data = {}

    def log(self, dataset, x, y):
        """Create a 2-D dataset and add data to it.

        Args:
            dataset - string for name of the dataset.
            x - list of values to be added as column 1 of dataset
            y - list of values to be added as column 2 of dataset

        Returns:
            None

        Excepts:
            None"""

        if dataset not in self.data.keys():
            self.data[dataset] = ([], [])

        self.data[dataset][0].append(x)
        self.data[dataset][1].append(y)

    def plot(self, datasets, xlabel=None, ylabel=None, title=None, grid=True,
             xlog=False, ylog=False):
        """Plotting function.

        Args:
            datasets - list of strings of the datasets to plot.
            xlabel - string for x-axis label.
            ylabel - string for y-axis label.
            title - string for graph title.
            grid - Boolean for grid on/off.
            xlog - Boolean for logarithmic scale on x-axis.
            ylog - Boolean for logarithmic scale on y-axis.

        Returns:
            None

        Excepts:
            None"""

        for dataset in datasets:
            x = np.asarray(self.data[dataset][0])
            y = np.asarray(self.data[dataset][1])
            plt.plot(x, y, label=dataset)

        plt.legend()

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.title(title)

        plt.grid(grid)

        if xlog:
            plt.xscale('log')
        else:
            plt.xscale('linear')

        if ylog:
            plt.yscale('log')
        else:
            plt.yscale('linear')

        plt.show()
