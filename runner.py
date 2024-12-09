#!/usr/bin/env python3

# this file is used to run the simulation, for different parameters.
#

from main import run_simulation
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import os


def save_results(results, parameters, foldername, filename):
    """
    Saves parameters and results to filename, filename_parameters in a given folder
    Results has to be a ndarray of shape (4, N_indivd)
    """

    # create directory
    newpath = f"./results/{foldername}"
    if not os.path.exists(newpath):
        print(f"making {newpath}")
        os.makedirs(newpath)

    # save parameters
    with open(f"./results/{foldername}/{filename}_parameters.json", "w+") as file:
        json.dump(parameters, file)

    # save results
    np.savetxt(f"./results/{foldername}/{filename}_results.txt", results)


parameters = {
    "beta": 1 / 1.8,
    "gamma": 1 / 14,
    "theta": 0.0001,
    "alpha": 1 / 25,
    "N_indiv": 2000,
    "simulation_days": 30,
    "dt": 0.1,
    "I0": 2,
    "sus_mean": 1,
    "sus_std": 0.2,
    "vaccine_mode": "risk group",
    "vaccine_factor": 0.2,
    "vaccine_time": 0.3,
    "fraction_weakest": 0.5,
}


result = run_simulation(parameters)
foldername = time.strftime("%Y-%m-%d_%H_%M_%S")
filename = "test"
save_results(result, parameters, foldername, filename)


S = results[0]
I = results[1]
R = results[2]
D = results[3]
days = np.linspace(0, parameters["simulation_days"], num=S.size)
plt.plot(days, S, c=[0.2, 0.4, 0.7], label="S")
plt.plot(days, I, c=[0.7, 0.3, 0.2], label="I")
plt.plot(days, R, c=[0.3, 0.7, 0.3], label="R")
plt.plot(days, D, c=[0.6, 0.6, 0.6], label="D")


plt.legend()
plt.xlabel("time")
plt.ylabel("S, I, R, D")

plt.show()


"""
# "original" parameters
N_indiv = 2000  # * Antalet individer som ska simuleras
simulation_days = 300
dt = 0.1  # time step (measured in days)
I0 = 2  # Start value of I

# SIR params = beta, gamma, theta, alpha
beta = 1 / 1.8
gamma = 1 / 14
theta = 0.0001
alpha = 1 / 25
sus_mean = 1
sus_std = 0.2
vaccine_mode = "risk group"
vaccine_factor = 0.20  # factor by which the vaccination decreases suseptability
vaccine_factor = 1.0  # factor by which the vaccination decreases suseptability
fraction_weakest = 0.5
"""
"""
"""
