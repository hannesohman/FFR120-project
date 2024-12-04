#!/usr/bin/env python3

import numpy as np

# an attempt to redo the dsr algorithm faster


def diffuse_spread_recover(x, y, status, d, beta, gamma, L, alpha):
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

    # vectorized diffusion step.
    agent_diffuses = np.random.rand(N) < d
    x_diffuses = np.random.rand(N) < 0.5
    y_diffuses = np.invert(x_diffuses)
    move_direction = np.sign(np.random.rand(N) - 0.5)

    x = np.where(agent_diffuses & x_diffuses, x + move_direction, x)
    y = np.where(agent_diffuses & y_diffuses, y + move_direction, y)

    # Enforce pbc.
    # TODO change to reflective boundaries.
    x = x % L
    y = y % L

    # Recovered to suseptible with probability alpha.
    # vectorized version:
    recover_draw = np.random.random(N)
    status = np.where((status == 2) & (recover_draw < alpha), 0, status)

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
    recover_draw = np.random.rand(N)
    status = np.where((recover_draw < gamma) & (status == 1), 2, status)

    return x, y, status




def spread(x, y, status, beta, susceptibility):
    infected = np.where(status == 1)[0]

    for i in infected:
        # Check whether other particles share the same position.

        same_x = np.where(x == x[i])
        same_y = np.where(y == y[i])
        same_cell = np.intersect1d(same_x, same_y)
        for j in same_cell:
            if status[j] == 0:
                if np.random.rand()*susceptibility[j] < beta:
                    status[j] = 1
    return status


def recover_die(status, gamma, theta, N_indiv):
    recover_draw = np.random.rand(N_indiv,1)
    status = np.where((recover_draw < gamma) & (status == 1), 2, status)
    status = np.where((recover_draw < theta) & (status == 1), 3, status)
    return status

def reset(status, alpha, N_indiv):
    reset_draw = np.random.rand(N_indiv,1)
    status = np.where((reset_draw < alpha) & (status == 2), 0, status)
    return status

def switch_location(location, schedule, p_schedule, location_info, N_indiv):
    sched_index = list(location_info.keys()).index(schedule)

    p_weights = [(1-p_schedule) / (len(location_info) - 1) for loc in location_info]
    p_weights[sched_index] = p_schedule

    location = np.random.choice(list(location_info.keys()),(N_indiv,1), p=p_weights)
    return location