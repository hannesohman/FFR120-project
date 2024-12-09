import numpy as np
import time
from tkinter import *
import random as r
from diffuse_spread_recover_vectorized import *
import matplotlib.pyplot as plt


def get_min_max(location, location_info):
    # Tar emot individernas tilldelade områden
    # Hämtar en individs gränser baserat på vilket rum den befinner sig i.
    # Returnerar fyrra kolumnvektorer med gränserna på individernas tilldelade område.
    N_indiv = np.size(location, axis=0)
    min_x = np.zeros((N_indiv, 1))
    min_y = np.zeros((N_indiv, 1))
    max_x = np.zeros((N_indiv, 1))

    max_y = np.zeros((N_indiv, 1))

    for idx, loc in enumerate(location):
        x0, y0, x1, y1 = location_info[loc[0]][0]
        min_x[idx] = x0 + 1
        min_y[idx] = y0 + 1
        max_x[idx] = x1 - 1
        max_y[idx] = y1 - 1

    return min_x, min_y, max_x, max_y


def random_location_coords(location, location_info):
    # Tar emot individers tilldelade område
    # Anger en random slumpmässig startposition för en individ i det område individen tillhör
    # Returnerar sumpmässiga koordinater inom det tilldelade området
    N_indiv = np.size(location, axis=0)

    x = np.zeros((N_indiv, 1))
    y = np.zeros((N_indiv, 1))

    for idx, loc in enumerate(location):
        x0, y0, x1, y1 = location_info[loc[0]][0]

        x[idx] = int((np.random.rand() * (x1 - x0) + x0))
        y[idx] = int((np.random.rand() * (y1 - y0) + y0))
    return x, y


def move(x, y, d, status):
    # Tar emot individers nuvarande koordinater.
    # Flyttar individen i x- och y-led med -1, 0, eller +1 steg
    # Returnerar de nya koordinaterna

    dx = np.random.choice([-1, 0, 1], (x.shape[0], 1), p=[d / 2, 1 - d, d / 2])
    dy = np.random.choice([-1, 0, 1], (y.shape[0], 1), p=[d / 2, 1 - d, d / 2])

    dx[status == 3] = 0
    dy[status == 3] = 0

    return x + dx, y + dy


def walls(nx, ny, min_x, min_y, max_x, max_y):
    # Tar emot individernas nya koordinater och gränserna på deras område
    # Applicerar gränserna på koordinaterna ifall de försöker flytta sig utanför området
    # Returnerar de nya koordinaterna

    nx[nx < min_x] = min_x[nx < min_x]
    nx[nx > max_x] = max_x[nx > max_x]

    ny[ny < min_y] = min_y[ny < min_y]
    ny[ny > max_y] = max_y[ny > max_y]

    return nx, ny


def run_simulation(parameters):
    """
    Main function for running the simulation.
    Return the S,I,R values as numpy vectors, with time step dt over simulation_days

    Parameters:
    (beta, gamma, theta, alpha) - SIR parameters
    N_invid - number of agents
    simulation_days - how many days to simulate for
    dt - timestep (1/dt = number of steps per day)
    I0 - number of infected agents at t = 0
    diffusion_coeff - probability of agent movement
    sus_mean - suseptibility mean
    sus_std - suseptibility standard deviation
    vaccine_mode - how the vaccination is performed
    vaccine_factor - factor by which the vaccination decreases sus
    fraction_weakset - ???

    silent_mode - if true, run without showing simulation
    """
    beta = parameters["beta"]
    gamma = parameters["gamma"]
    theta = parameters["theta"]
    alpha = parameters["alpha"]
    N_indiv = parameters["N_indiv"]
    simulation_days = parameters["simulation_days"]
    dt = parameters["dt"]
    I0 = parameters["I0"]
    sus_mean = parameters["sus_mean"]
    sus_std = parameters["sus_std"]
    vaccine_mode = parameters["vaccine_mode"]
    vaccine_factor = parameters["vaccine_factor"]
    vaccine_time = parameters["vaccine_time"]
    fraction_weakest = parameters["fraction_weakest"]

    if "silent_mode" in parameters:
        silent_mode = parameters["silent_mode"]
    else:
        silent_mode = True

    day_steps = int(1 / dt)  # steps per day (used in for-loop)

    # adjust parameters for dt
    beta *= dt
    gamma *= dt
    theta *= dt
    alpha *= dt

    d = (
        0.6 * dt
    )  # Diffusion, sannolikheten att en individ förflyttar sig. Är lägre under föreläsningar och högre under lunch.

    g_h = 157  # Grid height   47, 94, 141,
    g_w = 309  # Grid width    96, 192, 288
    # grid förhållandet är 96 : 47 (309 : 157)

    ratio = (
        4  # * Förhållandet mellan upplösningen på fönstret och upplösningen på rutnätet
    )
    vaccination_time = None

    if not silent_mode:
        tk = Tk()
        tk.geometry(f"{g_w*ratio}x{g_h*ratio}")
        tk.configure(background="#000000")

        canvas = Canvas(tk, background="#ECECEC")
        tk.attributes("-topmost", 0)
        canvas.place(x=0, y=0, height=g_h * ratio, width=g_w * ratio)

    # positioner och gränser för platser på campus, sista siffran är en ratio med hur många av befolkningen som har det som sin "home_base"
    location_info = {
        "kårhuset": [(0.29 * g_w, 0.04 * g_h, 0.44 * g_w, 0.21 * g_h)   , 4],
        "vasa": [(0.83 * g_w, 0.57 * g_h, 0.99 * g_w, 0.81 * g_h)       , 10],
        "mc2": [(0.60 * g_w, 0.39 * g_h, 0.69 * g_w, 0.54 * g_h)        , 3],
        "fysikhuset": [(0.45 * g_w, 0.42 * g_h, 0.56 * g_w, 0.54 * g_h) , 8],
        "kemihuset": [(0.50 * g_w, 0.62 * g_h, 0.58 * g_w, 0.93 * g_h)  , 8],
        "biblioteket": [(0.39 * g_w, 0.83 * g_h, 0.48 * g_w, 0.94 * g_h), 2],
        "mattehuset": [(0.39 * g_w, 0.58 * g_h, 0.46 * g_w, 0.74 * g_h) , 2],
        "HA": [(0.27 * g_w, 0.76 * g_h, 0.35 * g_w, 0.81 * g_h)         , 3],
        "HB": [(0.15 * g_w, 0.76 * g_h, 0.26 * g_w, 0.81 * g_h)         , 3],
        "HC": [(0.05 * g_w, 0.76 * g_h, 0.14 * g_w, 0.81 * g_h)         , 3],
        "EDIT": [(0.06 * g_w, 0.52 * g_h, 0.15 * g_w, 0.74 * g_h)       , 8],
        "maskinhuset": [(0.17 * g_w, 0.51 * g_h, 0.34 * g_w, 0.73 * g_h), 12],
        "SB-huset": [(0.06 * g_w, 0.21 * g_h, 0.21 * g_w, 0.36 * g_h)   , 12],
    }

    if not silent_mode:
        # Följande ritar upp rektanglar för områdena.
        for key, val in location_info.items():
            coords = [c * ratio for c in val[0]]
            coords = [np.round(val) for val in coords]
            canvas.create_rectangle(coords)


    home_weights = [vals[1] for vals in location_info.values()]
    home_weights = [p / sum(home_weights) for p in home_weights]

    home_base = np.random.choice(list(location_info.keys()), (N_indiv, 1), p=home_weights)
    print(home_base)

    min_x, min_y, max_x, max_y = get_min_max(home_base, location_info)

    x0, y0 = random_location_coords(home_base, location_info)

    status = np.zeros((N_indiv, 1))
    status[:I0] = 1

    susceptibility = np.random.normal(sus_mean, sus_std, (N_indiv, 1))
    # no one has a lower suseptibility than 1
    # higher suseptibility -> higher risk of being infected
    susceptibility[susceptibility < 1] = 1

    individuals_dots = []
    if not silent_mode:
        for id in range(N_indiv):
            if status[id] == 0:
                agent_color = "#1f77b4"
            elif status[id] == 1:
                agent_color = "#d62728"
            else:
                agent_color = "#2ca02c"

            individuals_dots.append(
                canvas.create_oval(
                    x0[id][0] * ratio - 2,
                    y0[id][0] * ratio - 2,
                    x0[id][0] * ratio + 2,
                    y0[id][0] * ratio + 2,
                    outline="",
                    fill=agent_color,
                )
            )

    location = home_base
    x = x0
    y = y0

    p_schedule = 0.80

    S = []
    I = []
    R = []
    D = []

    running = True

    global_steps = 0

    vaccination = False

    print_progress = True

    for day in range(simulation_days):
        # step = 0

        for step in range(day_steps):
            S.append(np.size(np.where(status == 0)[0]))
            I.append(np.size(np.where(status == 1)[0]))
            R.append(np.size(np.where(status == 2)[0]))
            D.append(np.size(np.where(status == 3)[0]))

            if step == day_steps * 2 / 5:
                schedule = "kårhuset"  # Ska representer lunchtid
                d = 0.70 * dt
                location = switch_location(
                    location, schedule, p_schedule, location_info, N_indiv
                )
                x, y = random_location_coords(location, location_info)
                min_x, min_y, max_x, max_y = get_min_max(location, location_info)

            if step == day_steps * 3 / 5:
                schedule = "lecture"  # Ska representera föreläsningar
                d = 0.4 * dt
                location = home_base
                x, y = random_location_coords(location, location_info)
                min_x, min_y, max_x, max_y = get_min_max(location, location_info)

            if I[-1] > vaccine_time * N_indiv and not vaccination:
                print(f"Day: {day} Step: {step} ({day*day_steps + step}) | VACCINE!!!")
                # "all even" , "all random" , "risk group"
                susceptibility = vaccinate(
                    susceptibility,
                    N_indiv,
                    mode=vaccine_mode,
                    vaccine_factor=vaccine_factor,
                    fraction_weakest=fraction_weakest,
                )
                vaccination = True
                vaccination_time = global_steps

            nx, ny = move(x, y, d, status)  # Flytta inddividerna

            nx, ny = walls(nx, ny, min_x, min_y, max_x, max_y)

            status = spread(nx, ny, status, beta, susceptibility)
            status = recover_die(status, gamma, theta, N_indiv)
            status = reset(status, alpha, N_indiv)

            for id, indiv in enumerate(
                individuals_dots
            ):  # Rita deras nya position på grafiken
                if status[id] == 0:
                    agent_color = "#1f77b4"
                elif status[id] == 1:
                    agent_color = "#d62728"
                elif status[id] == 2:
                    agent_color = "#2ca02c"
                elif status[id] == 3:
                    agent_color = "#bbbbbb"

                canvas.coords(
                    indiv,
                    nx[id][0] * ratio - 2,
                    ny[id][0] * ratio - 2,
                    nx[id][0] * ratio + 2,
                    ny[id][0] * ratio + 2,
                )
                canvas.itemconfig(indiv, fill=agent_color)

            x = nx
            y = ny

            if not silent_mode:
                tk.update_idletasks()
                tk.update()
                time.sleep(0.0000001)
                # print(
                #    f"Day: {day} | Step: {step} | S:{S[-1]} | I:{I[-1]} | R:{R[-1]} | D:{D[-1]} |"
                # )
            if print_progress:
                total_steps = simulation_days * day_steps
                print_interval = 200

                if global_steps % int(total_steps / print_interval) == 0:
                    percent_done = round(100 * global_steps / total_steps, 2)
                    print(f"simulating... {percent_done}", end="\r")
            global_steps += 1

            if I[-1] == 0:  # or step == 600:
                running = False
                break
        if I[-1] == 0:  # or step == 600:
            running = False
            break
            # step += 1

    if not silent_mode:
        tk.update_idletasks()
        tk.update()
        tk.mainloop()
    S = np.array(S)
    I = np.array(I)
    R = np.array(R)
    D = np.array(D)

    return (S, I, R, D)


if __name__ == "__main__":
    parameters = {
        "beta": 1 / 1.8,
        "gamma": 1 / 14,
        "theta": 0.0001,
        "alpha": 1 / 25,
        "N_indiv": 2000,
        "simulation_days": 300,
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