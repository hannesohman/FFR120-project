#!/usr/bin/env python3

# this file is used to run the simulation for different parameters.

from main import run_simulation
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import os


def save_results(result, parameters, foldername, filename):
    """
    Saves parameters and results to filename, filename_parameters in a given folder
    Results has to be a ndarray of shape (4, N_indivd)
    """

    # create directory
    newpath = f"./results/{foldername}"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # save parameters
    with open(f"./results/{foldername}/{filename}_param.json", "w+") as file:
        json.dump(parameters, file)

    # save results
    np.savetxt(f"./results/{foldername}/{filename}_result.txt", result)

    # save a plot of results (not for final poster, only temporary use)
    S = result[0]
    I = result[1]
    R = result[2]
    D = result[3]
    days = np.linspace(0, parameters["simulation_days"], num=S.size)
    plt.plot(days, S, c=[0.2, 0.4, 0.7], label="S")
    plt.plot(days, I, c=[0.7, 0.3, 0.2], label="I")
    plt.plot(days, R, c=[0.3, 0.7, 0.3], label="R")
    # deaths are not really showing anything for now
    # plt.plot(days, D, c=[0.6, 0.6, 0.6], label="D")

    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Individuals")

    plt.savefig(f"./results/{foldername}/{filename}_plot.png")
    plt.clf()
    plt.close()


parameters = {
    "beta": 1 / 1.5,
    "gamma": 1 / 14,
    "theta": 0.0001,
    "alpha": 1 / 25,
    "N_indiv": 2000,
    "simulation_days": 300,
    "dt": 0.1,
    "I0": 10,  # too low -> risk of disease dying out
    "sus_mean": 1,
    "sus_std": 0.2,
    "vaccine_mode": "risk group",
    "vaccine_factor": 0.2,
    "vaccine_time": 0.1,  # fraction of infected population before vaccination
    "fraction_weakest": 0.5,
    "lockdown_time": 1,
    "silent_mode": True,
}

foldername = time.strftime("%Y-%m-%d_%H_%M_%S")
"""
# loop over multiple vaccination times, no lockdown
vaccination_times = np.linspace(0, 1, num=3)
vaccination_times = np.round(vaccination_times, decimals=2)  # round for cleanliness
for i, vaccination_time in enumerate(vaccination_times):
    parameters["vaccine_time"] = vaccination_time
    parameters["lockdown_time"] = 1
    filename = f"Vaccination_{vaccination_time}"

    result = run_simulation(parameters)
    save_results(result, parameters, foldername, filename)
"""

# loop over multiple lockdown times (fixed vaccination time at )
lockdown_times = np.linspace(0, 1, num=3)
lockdown_times = np.round(lockdown_times, decimals=2)  # round for cleanliness
for i, lockdown_time in enumerate(lockdown_times):
    parameters["lockdown_time"] = lockdown_time
    parameters["vaccination_time"] = 1
    filename = f"Lockdown_{lockdown_time}"

    result = run_simulation(parameters)
    save_results(result, parameters, foldername, filename)
