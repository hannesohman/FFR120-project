#!/usr/bin/env python3


def diffuse_spread_recover(x, y, status, d, beta, gamma, L):
    """
    Function performing the diffusion step, the infection step, and the
    recovery step happening in one turn for a population of agents in a box with length L.

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
