#!/usr/bin/env python3

# this file is used to run the simulation, for different parameters.
#

from main import run_simulation
import numpy as np
import matplotlib.pyplot as plt


# parameters är en riktigt ful lista jag gjorde lite småtemporärt // Edvin
# parameterarna är:
# 0 - beta
# 1 - gamma
# 2 - theta
# 3 - alpha
# 4 - N_indiv
# 5 - simulation_days
# 6 - dt
# 7 - I0
# 8 - sus_mean
# 9 - sus_std
# 10 - vaccine_mode (STRING)
# 11 - vaccine_factor
# 12 - vaccine_time
# 13 - fraction_weakest
# 14 - (optional) silent mode (BOOL)
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
    "silent_mode": False,
}


S, I, R, D = run_simulation(parameters)


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
