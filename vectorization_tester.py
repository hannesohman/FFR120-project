#!/usr/bin/env python3

# file for testing if function behaves properly.
import numpy as np
import matplotlib.pyplot as plt
import time


from tkinter import *
from diffuse_spread_recover_vectorized import diffuse_spread_recover

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


# window_size = 600

# tk = Tk()
# tk.geometry(f'{window_size + 20}x{window_size + 20}')
# tk.configure(background='#000000')

# canvas = Canvas(tk, background='#ECECEC')  # Generate animation window.
# tk.attributes('-topmost', 0)
# canvas.place(x=10, y=10, height=window_size, width=window_size)


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

        print(f"{I0} {alpha} || {run} | {step} | S: {S[-1]} I: {I[-1]} R: {R[-1]}")

        # Update animation frame.
        # if step % N_skip == 0:
        #     canvas.delete('all')

        #     agents = []
        #     for j in range(N_part):
        #         if status[j] == 0:
        #             agent_color = '#1f77b4'
        #         elif  status[j] == 1:
        #             agent_color = '#d62728'
        #         else:
        #             agent_color = '#2ca02c'

        #         agents.append(
        #             canvas.create_oval(
        #                 (x[j] - ra) / L * window_size,
        #                 (y[j] - ra) / L * window_size,
        #                 (x[j] + ra) / L * window_size,
        #                 (y[j] + ra) / L * window_size,
        #                 outline='',
        #                 fill=agent_color,
        #             )
        #         )

        #     tk.title(f'Iteration {step}')
        #     tk.update_idletasks()
        #     tk.update()
        #     time.sleep(0.1)  # Increase to slow down the simulation.

        step += 1
        if I[-1] == 0 or step >= 500:
            running = False

    # tk.update_idletasks()
    # tk.update()
    # tk.mainloop()  # Release animation handle (close window to finish).

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

plt.show()
