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
    dt = parameters["dt"]
    S = result[0]
    I = result[1]
    R = result[2]
    D = result[3]
    days = np.linspace(0, S.size * dt, num=S.size)
    plt.plot(days, S, c=[0.2, 0.4, 0.7], label="S")
    plt.plot(days, I, c=[0.7, 0.3, 0.2], label="I")
    plt.plot(days, R, c=[0.3, 0.7, 0.3], label="R")
    if vaccination_time is not None:
        plt.axvline(x=vaccination_time, color="black", ls="--", label="Vaccination")
    if lockdown_time is not None:
        plt.axvline(x=lockdown_time, color="black", ls="--", label="Lockdown")
    # deaths are not really showing anything for now
    # plt.plot(days, D, c=[0.6, 0.6, 0.6], label="D")

    plt.legend()
    plt.xlabel("Time (days)")
    plt.ylabel("Individuals")

    title = f'Lockdown at slope {parameters["lockdown_alert"]}, vaccination at slope {parameters["vaccine_alert"]}'
    plt.title(title)

    plt.savefig(f"./results/{foldername}/{filename}_plot.png")
    print(f"Saved ./results/{foldername}/{filename}_plot.png")
    plt.clf()
    plt.close()


dt = 0.1

parameters = {
    "beta": (1 / 0.15) * dt,  # Probability of becoming infected
    "gamma": (1 / 1.4) * dt,  # Probability of becoming recovered
    "theta": (0.001) * dt,  # Probability of dying
    "alpha": (1 / 2.5) * dt,  # Probability of becoming susceptible again
    "N_indiv": 2000,
    "simulation_days": 300,
    "dt": dt,
    "I0": 10,  # too low -> risk of disease dying out
    "sus_mean": 1,
    "sus_std": 0.2,
    "vaccine_mode": "risk group",
    "vaccine_factor": 0.2,
    "slope_days": 10,
    "vaccine_alert": 20,  # number of infected per day before vaccination
    "fraction_to_vaccinate": 0.5,
    "lockdown_time": 1,
    "lockdown_alert": 20,
    "display_graphics": False,
}

foldername = time.strftime("%Y-%m-%d-%H.%M.%S")
repeats = 4


# multiple vaccination times, no lockdown
min_alert = 0
max_alert = 60
num_steps = 30

vaccine_alerts = np.linspace(min_alert, max_alert, num=num_steps)
vaccine_alerts = np.round(vaccine_alerts, 0)
vaccine_alerts = vaccine_alerts[vaccine_alerts > 45]

for alert in vaccine_alerts:
    print(f"vaccine_alert: {alert}")
    for i in range(repeats):
        parameters["vaccine_alert"] = alert
        parameters["lockdown_alert"] = 10000
        filename = f"Vaccination_{alert}_{i+1}"

        result, vaccination_time, lockdown_time = run_simulation(parameters)
        save_results(result, parameters, foldername, filename)


# multiple lockdown times, no vaccination
lockdown_alerts = vaccine_alerts

for lockdown_alert in lockdown_alerts:
    for i in range(repeats):
        parameters["lockdown_alert"] = lockdown_alert
        parameters["vaccine_alert"] = 10000
        filename = f"Lockdown_{lockdown_alert}_{i+1}"

        result, vaccination_time, lockdown_time = run_simulation(parameters)
        save_results(result, parameters, foldername, filename)

# neither vaccination or lockdown

# for i in range(10):
#     parameters["lockdown_alert"] = 10000
#     parameters["vaccine_alert"] = 10000
#     filename = f"no_vaccine_no_lockdown_{i+1}"

#     result, vaccination_time, lockdown_time = run_simulation(parameters)
#     save_results(result, parameters, foldername, filename)

# both lockdown times and vaccination times

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
