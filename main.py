import numpy as np
import time
from tkinter import *
import random as r
from diffuse_spread_recover_vectorized import *
import matplotlib.pyplot as plt


N_indiv = 2000  #* Antalet individer som ska simuleras

I0 = 20

beta = 0.05     # Spread porbability
gamma = 0.007       # Revocery probability
theta = 0.0001   # Probability of dying
alpha = 0.01 # Probability of recovered becoming susceptible again

d = 0.06     # Diffusion, sannolikheten att en individ förflyttar sig. Är lägre under föreläsningar och högre under lunch.



g_h = 157  # Grid height   47, 94, 141,
g_w = 309  # Grid width    96, 192, 288
# grid förhållandet är 96 : 47 (309 : 157)

ratio = 4  # * Förhållandet mellan upplösningen på fönstret och upplösningen på rutnätet


tk = Tk()
tk.geometry(f"{g_w*ratio}x{g_h*ratio}")
tk.configure(background="#000000")

canvas = Canvas(tk, background="#ECECEC")
tk.attributes("-topmost", 0)
canvas.place(x=0, y=0, height=g_h * ratio, width=g_w * ratio)

#
location_info = {
    "kårhuset": (0.29 * g_w, 0.04 * g_h, 0.44 * g_w, 0.21 * g_h),
    "vasa": (0.83 * g_w, 0.57 * g_h, 0.99 * g_w, 0.81 * g_h),
    "mc2": (0.60 * g_w, 0.39 * g_h, 0.69 * g_w, 0.54 * g_h),
    "fysikhuset": (0.45 * g_w, 0.42 * g_h, 0.56 * g_w, 0.54 * g_h),
    "kemihuset": (0.50 * g_w, 0.62 * g_h, 0.58 * g_w, 0.93 * g_h),
    "biblioteket": (0.39 * g_w, 0.83 * g_h, 0.48 * g_w, 0.94 * g_h),
    "mattehuset": (0.39 * g_w, 0.58 * g_h, 0.46 * g_w, 0.74 * g_h),
    "HA": (0.27 * g_w, 0.76 * g_h, 0.35 * g_w, 0.81 * g_h),
    "HB": (0.15 * g_w, 0.76 * g_h, 0.26 * g_w, 0.81 * g_h),
    "HC": (0.05 * g_w, 0.76 * g_h, 0.14 * g_w, 0.81 * g_h),
    "EDIT": (0.06 * g_w, 0.52 * g_h, 0.15 * g_w, 0.74 * g_h),
    "maskinhuset": (0.17 * g_w, 0.51 * g_h, 0.34 * g_w, 0.73 * g_h),
    "SB-huset": (0.06 * g_w, 0.21 * g_h, 0.21 * g_w, 0.36 * g_h),
}


# Följande ritar upp rektanglar för områdena.
for key, val in location_info.items():
    coords = [c * ratio for c in val]
    coords = [np.round(val) for val in coords]
    canvas.create_rectangle(coords)


def get_min_max(location):
    # Tar emot individernas tilldelade områden
    # Hämtar en individs gränser baserat på vilket rum den befinner sig i.
    # Returnerar fyrra kolumnvektorer med gränserna på individernas tilldelade område.

    min_x = np.zeros((N_indiv, 1))
    min_y = np.zeros((N_indiv, 1))
    max_x = np.zeros((N_indiv, 1))

    max_y = np.zeros((N_indiv, 1))

    for idx, loc in enumerate(location):
        x0, y0, x1, y1 = location_info[loc[0]]
        min_x[idx] = x0 + 1
        min_y[idx] = y0 + 1
        max_x[idx] = x1 - 1
        max_y[idx] = y1 - 1

    return min_x, min_y, max_x, max_y


def random_location_coords(location):
    # Tar emot individers tilldelade område
    # Anger en random slumpmässig startposition för en individ i det område individen tillhör
    # Returnerar sumpmässiga koordinater inom det tilldelade området

    x = np.zeros((N_indiv, 1))
    y = np.zeros((N_indiv, 1))

    for idx, loc in enumerate(location):
        x0, y0, x1, y1 = location_info[loc[0]]

        x[idx] = int((np.random.rand() * (x1 - x0) + x0))
        y[idx] = int((np.random.rand() * (y1 - y0) + y0))
    return x, y

def move(x, y, d):
    # Tar emot individers nuvarande koordinater.
    # Flyttar individen i x- och y-led med -1, 0, eller +1 steg
    # Returnerar de nya koordinaterna

    dx = np.random.choice([-1, 0, 1], (x.shape[0], 1), p=[d/2, 1 - d, d/2])
    dy = np.random.choice([-1, 0, 1], (y.shape[0], 1), p=[d/2, 1 - d, d/2])

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


location0 = np.random.choice(list(location_info.keys()), (N_indiv, 1))

min_x, min_y, max_x, max_y = get_min_max(location0)

x0, y0 = random_location_coords(location0)

status = np.zeros((N_indiv,1))
status[:I0] = 1

susceptibility = np.random.normal(0.80, 0.2, (N_indiv, 1))
susceptibility[susceptibility > 1] = 1
print(susceptibility)


individuals_dots = []

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


location = location0
x = x0
y = y0

schedule = "lecture"
p_schedule = 0.80


S = []
I = []
R = []
D = []

running = True

simulation_days = 20
day_steps = 600

global_steps = 0

for day in range(simulation_days):
    # step = 0

    for step in range(day_steps):
        S.append(np.size(np.where(status == 0)[0]))
        I.append(np.size(np.where(status == 1)[0]))
        R.append(np.size(np.where(status == 2)[0]))
        D.append(np.size(np.where(status == 3)[0]))


        if step == day_steps * 2/5:
            schedule = "kårhuset"   # Ska representer lunchtid
            d = 0.70
            location = switch_location(location, schedule, p_schedule, location_info, N_indiv)
            x, y = random_location_coords(location)
            min_x, min_y, max_x, max_y = get_min_max(location)

        if step == day_steps * 3/5:
            schedule = "lecture"    # Ska representera föreläsningar
            d = 0.04
            location = np.random.choice(list(location_info.keys()),(N_indiv,1))
            x, y = random_location_coords(location)
            min_x, min_y, max_x, max_y = get_min_max(location)

        

        nx, ny = move(x, y, d)     # Flytta inddividerna

        nx, ny = walls(nx, ny, min_x, min_y, max_x, max_y)

        status = spread(nx, ny, status, beta, susceptibility)
        status = recover_die(status, gamma, theta, N_indiv)
        status = reset(status, alpha, N_indiv)





        for id, indiv in enumerate(individuals_dots): # Rita deras nya position på grafiken
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

        tk.update_idletasks()
        tk.update()
        time.sleep(0.0000001)

        print(f"Day: {day} | Step: {step} | S:{S[-1]} | I:{I[-1]} | R:{R[-1]} | D:{D[-1]} |")


        global_steps += 1

        if I[-1] == 0: # or step == 600:
            running = False
            break
    if I[-1] == 0: # or step == 600:
        running = False
        break
        # step += 1

        


tk.update_idletasks()
tk.update()
tk.mainloop()


plt.plot(range(global_steps), S, c=[0.2, 0.2, 0.5])
plt.plot(range(global_steps), I, c=[0.5, 0.3, 0.2])
plt.plot(range(global_steps), R, c=[0.3, 0.5, 0.3])
# plt.legend()
plt.xlabel("time")
plt.ylabel("S, I, R")

plt.show()