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
    # hitta alla (unika) positioner med infekterade
    all_infected_pos = np.array([x[status == 1], y[status == 1]]).T
    infected_positions, infected_counts = np.unique(
        all_infected_pos, axis=0, return_counts=True
    )
    infected_counts = np.array(infected_counts)

    # hitta alla agenter (index) som befinner sig på en infekterad position
    # konvertera alla positioner (x,y) till EN siffra (y*y_max + x) typ
    coord_shape = (np.max(x).astype(np.int64) + 1, np.max(y).astype(np.int64) + 1)
    infected_positions = (
        infected_positions[:, 0].astype(np.int64),
        infected_positions[:, 1].astype(np.int64),
    )
    positions = (x.astype(np.int64), y.astype(np.int64))

    raveled_infected_pos = np.ravel_multi_index(infected_positions, coord_shape)
    raveled_pos = np.ravel_multi_index(positions, coord_shape).flatten()

    # skapa en mask för agenter som befinner sig på en infekterad position
    concerned_agent_mask = np.isin(raveled_pos, raveled_infected_pos)
    concerned_agent_mask = concerned_agent_mask[:, np.newaxis]

    # medans det fortfarande finns infekterade kvar som har en risk att smitta,
    # smitta vidare.

    while np.size(infected_positions) >= 1:
        N_indiv = np.size(status)
        successful_infection = np.asarray(
            np.random.rand(N_indiv, 1) < beta * susceptibility
        )
        # all suseptible with successful infections get infected
        status[(status == 0) & successful_infection & concerned_agent_mask] = 1

        # now, remove one agent from every place (they have had the chance to infect)
        # and retry again
        infected_counts -= 1
        infected_x = infected_positions[0][infected_counts != 0]
        infected_y = infected_positions[1][infected_counts != 0]
        infected_positions = (infected_x, infected_y)

        infected_counts = infected_counts[infected_counts != 0]

        # update which agents are exposed
        raveled_infected_pos = np.ravel_multi_index(infected_positions, coord_shape)
        raveled_pos = np.ravel_multi_index(positions, coord_shape).flatten()

        # skapa en mask för agenter som befinner sig på en infekterad position
        concerned_agent_mask = np.isin(raveled_pos, raveled_infected_pos)
        concerned_agent_mask = concerned_agent_mask[:, np.newaxis]
    return status


def recover_die(status, gamma, theta, N_indiv):
    recover_draw = np.random.rand(N_indiv, 1)
    status = np.where((recover_draw < theta) & (status == 1), 3, status)
    status = np.where((recover_draw < gamma) & (status == 1), 2, status)
    return status


def reset(status, alpha, N_indiv):
    reset_draw = np.random.rand(N_indiv, 1)
    status = np.where((reset_draw < alpha) & (status == 2), 0, status)
    return status


def vaccinate(
    susceptibility,
    N_indiv,
    mode="all even",
    vaccine_factor=0.2,
    fraction_to_vaccinate=0.5,
):
    # print(vaccine_factor, fraction_to_vaccinate, mode)

    if mode == "all even":
        susceptibility *= vaccine_factor
    elif mode == "random":
        index = np.random.permutation(N_indiv)[: int(fraction_to_vaccinate * N_indiv)]
        susceptibility[index] *= vaccine_factor

    elif mode == "risk group":
        sorted_suscep = np.sort(susceptibility, axis=0)[::-1]
        # print(sorted_suscep)
        # print(len(sorted_suscep))
        index_cut = int(len(sorted_suscep) * fraction_to_vaccinate)
        # print(index_cut)
        weak_limit = sorted_suscep[index_cut]
        # print(weak_limit)
        # print(f"mean suseptibility before: {np.mean(susceptibility)}")
        susceptibility[susceptibility >= weak_limit] *= vaccine_factor
        # print(f"mean suseptibility after: {np.mean(susceptibility)}")
    else:
        print(f"Not a valid mode: {mode}")
    return susceptibility


def switch_location(location, schedule, p_schedule, location_info, N_indiv):
    sched_index = list(location_info.keys()).index(schedule)

    p_weights = [(1 - p_schedule) / (len(location_info) - 1) for loc in location_info]
    p_weights[sched_index] = p_schedule

    location = np.random.choice(list(location_info.keys()), (N_indiv, 1), p=p_weights)
    return location


def calc_infected_slope(I, latest_consider):
    if len(I) > latest_consider:
        grad = np.gradient(I[-latest_consider:])
        mean_slope = np.mean(grad)
        return mean_slope
    else:
        return 0
