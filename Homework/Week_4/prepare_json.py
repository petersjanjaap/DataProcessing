#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
this script imports data from csv and converts it to csv
"""

# import libraries
import pandas as pd

# define global variables
INPUT_CSV = 'worldbank_data.csv'


def load_file(csv_file, selected_variables):
    """
    returns file loaded from csv as a dataframe
    """

    # opens csv file and saves data to dataframe
    with open(INPUT_CSV) as myfile:
        df = pd.read_csv(myfile, delimiter=',')

    df = df[selected_variables]

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
    print(json_file)
    f.write(json_file)


if __name__ == "__main__":
    """
    this script imports data from csv and converts it to csv
    """

    # variables to use from datafile
    select_variables = ['Country Name',
                        'GDP per capita (constant 2010 US$) [NY.GDP.PCAP.KD]']

    # create dataframe from csv file and keep selected variables
    df = load_file(INPUT_CSV, select_variables)
    df = df.dropna()

    # rename variables
    df.columns = ['Country', 'GDP_capita']

    # save dataframe as json
    save_name = 'worldbank_data.json'
    json_save(df, save_name)
