#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
this script imports data from csv and converts it to json
"""

# import libraries
import pandas as pd

# define global variables
CSV_FILES = ['GOOG.csv', 'AAPL.csv', 'MSFT.csv']


def load_file(csv_file, select_variables):
    """
    returns file loaded from csv as a dataframe
    """

    # opens csv file and saves data to dataframe
    with open(csv_file) as myfile:
        df = pd.read_csv(myfile, delimiter=',')

    # keeps selected variables
    df = df[select_variables]

    # returns dataframe
    return df


def json_save(df, save_title):
    """
    saves dataframe to json file using specified index variable
    file is saved under title entered in function
    """
    # open new file to save
    f = open(save_title, "w")

    # create JSON datafile and save it
    json_file = df.to_json(orient='index')
    f.write(json_file)


if __name__ == "__main__":
    """
    this script imports data from csv and converts it to csv
    """
    #  iterate over csv files to convert
    for csv_file in CSV_FILES:

        # variables to use from datafile
        select_variables = ['Date', 'Close']

        # create dataframe from csv file and keep selected variables
        df = load_file(csv_file, select_variables)
        df = df.dropna()

        # save dataframe as json
        save_name = csv_file.split('.csv')[0] + '.json'
        json_save(df, save_name)
