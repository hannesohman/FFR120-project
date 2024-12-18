#!/usr/bin/env python3

# this will only be used to import data an plot it.
import os
import json
import numpy as np
import matplotlib.pyplot as plt


def load_data(foldername):
    """
    Load data given a folder name

    return a list of all S,I,R,D data and another list containing dict of parameters
    """
    data_path = f"./results/{foldername}/"
    filenames = os.listdir(data_path)

    # find all parameter and result files
    parameter_filepaths = [
        data_path + filename for filename in filenames if "param.json" in filename
    ]
    result_filepaths = [
        data_path + filename for filename in filenames if "result.txt" in filename
    ]

    # sort so that they appear in same order
    parameter_filepaths = sorted(parameter_filepaths)
    result_filepaths = sorted(result_filepaths)

    # convert into their respective data types
    parameters = []
    for parameter_filepath in parameter_filepaths:
        with open(parameter_filepath, "r") as file:
            parameter_data = json.load(file)
            parameters.append(parameter_data)

    results = []
    for result_filepath in result_filepaths:
        result_data = np.loadtxt(result_filepath)
        results.append(result_data)

    return parameters, results


parameters, results = load_data("2024-12-13-16.25.16")

# create a plot of infected individuals depending on when vaccination or lockdown was introduced
plotted_vaccine = False

plotted_lockdown = False
plotted_normal = False

threshold = 0.1

for parameter, result in zip(parameters, results):
    if parameter["vaccination_x"] != 0 and parameter["lockdown_x"] == 0:
        S, I, R, D = result
        days = np.linspace(0, parameter["simulation_days"], num=I.size)

        label = (
            None if plotted_vaccine else f"Vaccination at {threshold} infected fraction"
        )
        plt.plot(days, I / parameter["N_indiv"], label=label, color="orange")
        plotted_vaccine = True

    elif parameter["vaccination_x"] == 0 and parameter["lockdown_x"] != 0:
        S, I, R, D = result
        days = np.linspace(0, parameter["simulation_days"], num=I.size)

        label = (
            None if plotted_lockdown else f"Lockdown at {threshold} infected fraction"
        )
        plt.plot(days, I / parameter["N_indiv"], label=label, color="blue")
        plotted_lockdown = True

    elif parameter["vaccination_x"] == 0 and parameter["lockdown_x"] == 0:
        S, I, R, D = result
        days = np.linspace(0, parameter["simulation_days"], num=I.size)

        label = None if plotted_normal else f"No vaccination or lockdown"
        plt.plot(days, I / parameter["N_indiv"], label=label, color="green")
        plotted_normal = True

plt.legend()
plt.xlabel("Time (days)")
plt.ylabel("Infected individuals")
plt.title("Infected individuals")

plt.show()
