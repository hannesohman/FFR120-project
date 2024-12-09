#!/usr/bin/env python3

# this file is used to run the simulation, for different parameters.
#

from main import run_simulation
import numpy as np
import matplotlib.pyplot as plt


parameters = [
    1 / 1.8,
    1 / 14,
    0.0001,
    1 / 25,
    2000,
    300,
    0.1,
    2,
    1,
    0.2,
    "risk group",
    0.2,
    0.5,
]
S, I, R, D = run_simulation(*parameters)


days = np.linspace(0, simulation_days, num=S.size)
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
