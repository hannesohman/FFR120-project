import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *

N_part = 1000  # Total agent population.
d = 0.95  # Diffusion probability.
beta = 0.05  # Infection spreading probability.
gamma = 0.001  # Recovery probability.
alpha = 0.005  # Porbability that a recovered agent becomes suseptible again
L = 200  # Side of the lattice.

I0 = 10  # Initial number of infected agents.

# Initialize agents position.
x = np.random.randint(L, size=N_part)
y = np.random.randint(L, size=N_part)

# Initialize agents status.
status = np.zeros(N_part)
status[0:I0] = 1


def diffuse_spread_recover(x, y, status, d, beta, gamma, L):
    """
    Function performing the diffusion step, the infection step, and the
    recovery step happening in one turn for a population of agents.

    Parameters
    ==========
    x, y : Agents' positions.
    status : Agents' status.
    d : Diffusion probability.
    beta : Infection probability.
    gamma : Recovery probability.
    L : Side of the square lattice.
    """

    N = np.size(x)

    # Diffusion step.
    diffuse = np.random.rand(N)
    move = np.random.randint(4, size=N)
    for i in range(N):
        if diffuse[i] < d:
            if move[i] == 0:
                x[i] = x[i] - 1
            elif move[i] == 1:
                y[i] = y[i] - 1
            elif move[i] == 2:
                x[i] = x[i] + 1
            else:
                # move[i] == 3
                y[i] = y[i] + 1

    # Enforce pbc.
    x = x % L
    y = y % L

    # Recovered to suseptilbe.
    recovered = np.where(status == 2)[0]
    for r in recovered:
        # Check whether the recoverec becomes suseptible again.
        if np.random.rand() < alpha:
            status[r] = 0

    # Spreading disease step.
    infected = np.where(status == 1)[0]

    for i in infected:
        # Check whether other particles share the same position.
        same_x = np.where(x == x[i])
        same_y = np.where(y == y[i])
        same_cell = np.intersect1d(same_x, same_y)
        for j in same_cell:
            if status[j] == 0:
                if np.random.rand() < beta:
                    status[j] = 1

    # Recover step.
    for i in infected:
        # Check whether the infected recovers.
        if np.random.rand() < gamma:
            status[i] = 2

    return x, y, status


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
        x, y, status = diffuse_spread_recover(x, y, status, d, beta, gamma, L)

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
