#!/usr/bin/env python
# Name: Jan Peters
# Student number: 10452125
"""
this script analyzes data obtained from a .csv file
"""

# imports libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Global constants
INPUT_CSV = "input.csv"


def load_file(csv_file):
    """
    returns file loaded from csv as a dataframe
    """

    # opens csv file and saves data to dataframe
    with open(INPUT_CSV) as myfile:
        df = pd.read_csv(myfile)

    # returns dataframe
    return df


def num_var_clean(num_var):
    """
    cleans numerical variables by dropping alphabetical characters and
    adjusting data format to float type
    """

    # restores dot format for float numbers
    num_var = num_var.str.replace(',', '.')

    # drops all non-numerical and non-dot characters in observations
    num_var = num_var.str.replace('[^0-9\\.]', '')
    print(num_var)

    # converts numeric variables to float type
    num_var = pd.to_numeric(num_var, float)

    # returns the cleaned variable
    return num_var


def string_clean(string_var):
    """
    strips string variables from redundant spaces
    """

    # strips spaces from var
    string_var = string_var.str.strip(' ')

    # returns cleaned string var
    return string_var


def cent_tend_stats(var, var_name):
    """
    prints central tendency statistics for given variable from dataframe
    """

    print(f"Central tendency statics: {var_name}")
    print(f"MEAN {var_name}: {var.mean().round(2)}")
    print(f"MEDIAN {var_name}: {var.median()}")
    print(f"MODE {var_name}: {var.mode()}")
    print(f"STD {var_name}: {var.std().round(2)}\n\n")


def histogram(df, var_name):
    """
    generates and saves a histogram for given variable
    """

    # generates histogram for variable
    histogram = df[var_name].hist()
    histogram.set_ylabel('Frequency')
    histogram.set_xlabel('Observations')

    # saves histogram to pdf
    fig = histogram.get_figure()
    fig.suptitle(f'Histogram {var_name}', fontweight='bold')
    fig.savefig('histogram.pdf')


def box_plot(df, var_name):
    """
    generates and saves a boxplot for given variable
    """

    # generates histogram for variable
    boxplot = df.boxplot(column=var_name)
    boxplot.set_ylabel('Observations')

    # saves boxplot to pdf
    fig = boxplot.get_figure()
    fig.suptitle(f'Boxplot {var_name}', fontweight='bold')
    fig.savefig('boxplot.pdf')


def regress(df, x_var, y_var):
    """
    scatter plots variables against each other and executes regression
    results are saved into one figure in pdf format
    """

    # drop observations with missing x and y values
    df_regression = df[[x_var, y_var]].dropna()

    # log transform GDP and Infant Mortality
    variables = [x_var, y_var]
    for var in variables:
        df_regression[var] = np.log(df_regression[var])

    print(df_regression)

    # title name is to long to contain in plot description
    title_name = f'Log-transformed regression plot {y_var} on {x_var}'

    # generate variables plot
    plot = df_regression.plot(x=x_var, y=y_var, kind='scatter', grid=True,
                              title=title_name)

    # generate regression plot
    # generates future warning due to changing functionalities in Python
    sns.regplot(x=x_var, y=y_var, data=df_regression)

    # name axes
    plt.ylabel(f'log {y_var}')
    plt.xlabel(f'log {x_var}')

    # saves regression and variable plots to pdf
    fig = plot.get_figure()
    fig.savefig('regression.pdf')


def json_save(df, index_var, save_title):
    """
    saves dataframe to json file using specified index variable
    file is saved under title entered in function
    """
    # open new file to save
    f = open(save_title, "w")

    # set variable as index
    df = df.set_index(index_var)

    # create JSON datafile and save it
    json_file = df.to_json(orient='index')
    f.write(json_file)


if __name__ == "__main__":
    """
    analyzes data from csv file and outputs central tendency and five number
    statistics, and saves histogram and boxplot for selected num_variables
    """

    # loads dataframe from csv
    df = load_file(INPUT_CSV)

    # keeps selected variables
    df = df[['Country', 'Region', 'Pop. Density (per sq. mi.)',
             'Infant mortality (per 1000 births)',
             'GDP ($ per capita) dollars']]

    # rename variables
    df.columns = ['Country', 'Region', 'Pop. Density', 'Infant Mortality',
                  'GDP']

    # groups of numeric and string variables
    num_variables = ['Pop. Density', 'Infant Mortality', 'GDP']
    string_variables = ['Country', 'Region']

    # cleans numeric variables
    for var in num_variables:
        df[var] = num_var_clean(df[var])

    # cleans numeric variables
    for var in string_variables:
        df[var] = string_clean(df[var])

    # drops false outliers (Suriname's GDP equals $400000)
    df = df[df.Country != 'Suriname']

    # prints central tendency statistics for all numeric variables
    for var in num_variables:
        cent_tend_stats(df[var], var)

    # generates and saves a histogram for GDP
    histogram(df, 'GDP')

    #  generates and saves a boxplot for Infant Mortality
    box_plot(df, 'Infant Mortality')

    # print summary statistics for Infant Mortality
    print('Summary Statistics Infant Mortality')
    print(df['Infant Mortality'].describe())

    # regresses and plots Infant Mortalitity on GDP, results are saved as pdf
    regress(df, 'GDP', 'Infant Mortality')

    # save dataframe as JSON file using country as index as clean_output.JSON
    json_save(df, 'Country', 'clean_output.JSON')
