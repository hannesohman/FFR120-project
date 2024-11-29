#!/usr/bin/env python3

# file for testing if function behaves properly.
import numpy as np
import matplotlib.pyplot as plt
import time


from diffuse_spread_recover_vectorized import diffuse_spread_recover

# from diffuse_spread_recover import diffuse_spread_recover


N_part = 1000  # Total agent population.
d = 0.95  # Diffusion probability. beta = 0.05  # Infection spreading probability.
gamma = 0.001  # Recovery probability.
beta = 0.05  # Infection spreading probability.
alpha = 0.005  # Porbability that a recovered agent becomes suseptible again
L = 200  # Side of the lattice.

I0 = 10  # Initial number of infected agents.

# Initialize agents position.
x = np.random.randint(L, size=N_part)
y = np.random.randint(L, size=N_part)

# Initialize agents status.
status = np.zeros(N_part)
status[0:I0] = 1


N_skip = 1  # Visualize status every N_skip steps.
ra = 0.5  # Radius of the circle representing the agents.

starttime = time.time()
for run in range(5):
    running = True  # Flag to control the loop.
    step = 0

    # Initialize agents position.
    x = np.random.randint(L, size=N_part)
    y = np.random.randint(L, size=N_part)

    # Initialize agents status.
    status = np.zeros(N_part)
    status[0:I0] = 1

    S = []  # Keeps track of the susceptible agents.
    I = []  # Keeps track of the infectious agents.
    R = []  # Keeps track of the recovered agents.
    S.append(N_part - I0)
    I.append(I0)
    R.append(0)

    while running:
        x, y, status = diffuse_spread_recover(x, y, status, d, beta, gamma, L, alpha)

        S.append(np.size(np.where(status == 0)[0]))
        I.append(np.size(np.where(status == 1)[0]))
        R.append(np.size(np.where(status == 2)[0]))

        # if step % 100 == 0:
        #     print(f"{I0} {alpha} || {run} | {step} | S: {S[-1]} I: {I[-1]} R: {R[-1]}")

        step += 1
        if I[-1] == 0 or step >= 5000:
            running = False

    t = np.array(np.arange(len(S)))
    S_agents = np.array(S)
    I_agents = np.array(I)
    R_agents = np.array(R)

    plt.figure("3_P1")
    plt.title(f"I0: {I0} , alpha: {alpha}")
    plt.plot(t, S_agents, c=[0.2, 0.2, 0.5 + run * 0.12])
    plt.plot(t, I_agents, c=[0.5 + run * 0.12, 0.3 + run * 0.12, 0.2])
    plt.plot(t, R_agents, c=[0.3, 0.5 + run * 0.12, 0.3])
    # plt.legend()
    plt.xlabel("time")
    plt.ylabel("S, I, R")
print(f"finished in {round(time.time() - starttime,1)} s")
plt.show()
