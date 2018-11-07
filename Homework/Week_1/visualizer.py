#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
from statistics import mean
# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

if __name__ == "__main__":

    # opens csv file and save data to object dictionary
    with open(INPUT_CSV) as myfile:
        reader = csv.DictReader(myfile)

        # iterates over row and saves data to global dictionary
        for row in reader:
            data_dict[row['Year']].append(float(row['Rating']))

        # lists contains the values for axes of plot
        x_axis = []
        y_axis = []

        # iterates over keys in data dictionary
        for key in data_dict:

            # stores values of years and average ratings in relevant axes
            x_axis.append(key)
            y_axis.append(mean(data_dict[key]))

        # plots average rating per year
        plt.plot(x_axis, y_axis)
        plt.show()
