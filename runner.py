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
    if vaccination_time is not None:
        plt.axvline(x=vaccination_time, color='black', ls="--", label="Vaccination")
    # deaths are not really showing anything for now
    # plt.plot(days, D, c=[0.6, 0.6, 0.6], label="D")

    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Individuals")

    title = f'Lockdown at {parameters["lockdown_time"]}, vaccination at {parameters["vaccine_time"]}'
    plt.title(title)

    plt.savefig(f"./results/{foldername}/{filename}_plot.png")
    print(f"Saved ./results/{foldername}/{filename}_plot.png")
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
    "vaccine_alert": 20,  # number of infected per day before vaccination
    "fraction_to_vaccinate": 0.5,
    "lockdown_time": 1,
    "display_graphics": False,
}

foldername = time.strftime("%Y-%m-%d-%H.%M.%S")
repeats = 4


# loop over multiple vaccination times, no lockdown

vaccine_alerts = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

for alert in vaccine_alerts:
    print(f"vaccine_alert: {alert}")
    for i in range(repeats):
        parameters["vaccine_time"] = alert
        parameters["lockdown_time"] = 1
        filename = f"Vaccination_{alert}_{i+1}"

        result, vaccination_time = run_simulation(parameters)
        save_results(result, parameters, foldername, filename)


# loop over multiple lockdown times no vaccination
lockdown_times = [val for val in vaccine_alerts if val != 1]

for lockdown_time in lockdown_times:
    for i in range(repeats):
        parameters["lockdown_time"] = lockdown_time
        parameters["vaccine_time"] = 1
        filename = f"Lockdown_{lockdown_time}_{i+1}"

        result, vaccination_time = run_simulation(parameters)
        save_results(result, parameters, foldername, filename)

# loop over both lockdown times and vaccination times

# runs = 4

# lockdown_times = np.round(np.linspace(0, max_infections, num=runs), decimals=2)
# vaccination_times = np.round(np.linspace(0, max_infections, num=runs), decimals=2)

# for lockdown_time in lockdown_times:
#     for vaccination_time in vaccination_times:
#         parameters["lockdown_time"] = lockdown_time
#         parameters["vaccination_time"] = vaccination_time
#         filename = f"Lock_{lockdown_time}_vacc_{vaccination_time}"
#         result = run_simulation(parameters)
#         save_results(result, parameters, foldername, filename)
#         print(
#             f"Lockdown time {lockdown_time}, vaccination time {vaccination_time} complete"
#         )
