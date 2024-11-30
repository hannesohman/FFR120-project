import numpy as np
import time
from tkinter import *
import random as r


N_indiv = 1000  #* Antalet individer som ska simuleras


grid_height = 60
grid_width = 90

ratio = 10  #* Förhållandet mellan upplösningen på fönstret och upplösningen på rutnätet




tk = Tk()
tk.geometry(f'{grid_width*ratio}x{grid_height*ratio}')
tk.configure(background='#000000')

canvas = Canvas(tk, background='#ECECEC')
tk.attributes('-topmost', 0)
canvas.place(x=0, y=0, height=grid_height*ratio, width=grid_width*ratio)

# 
location_limits = {
    "kårhuset": (40,1,85,9),
    "fysikhuset": (65,21,88,33),
    "kemihuset": (78,35,89,59),
    "biblioteket": (52,47,75,57),
}


# Följande ritar upp rektanglar för områdena.
for key, val in location_limits.items():
    coords = [c*ratio for c in val]
    canvas.create_rectangle(coords)





def get_min_max(location):
    # Tar emot individernas tilldelade områden
    # Hämtar en individs gränser baserat på vilket rum den befinner sig i.
    # Returnerar fyrra kolumnvektorer med gränserna på individernas tilldelade område.

    min_x = np.zeros((N_indiv,1))
    min_y = np.zeros((N_indiv,1))
    max_x = np.zeros((N_indiv,1))
    max_y = np.zeros((N_indiv,1))

    for idx, loc in enumerate(location):
        x0, y0, x1, y1 = location_limits[loc[0]]
        min_x[idx] = x0 + 1
        min_y[idx] = y0 + 1
        max_x[idx] = x1 - 1
        max_y[idx] = y1 - 1

    return min_x, min_y, max_x, max_y


def random_location_coords(locations):
    # Tar emot individers tilldelade område
    # Anger en random slumpmässig startposition för en individ i det område individen tillhör
    # Returnerar sumpmässiga koordinater inom det tilldelade området

    x = np.zeros((N_indiv,1))
    y = np.zeros((N_indiv,1))

    for idx, loc in enumerate(locations):
        x0, y0, x1, y1 = location_limits[loc[0]]

        x[idx] = int((np.random.rand() * (x1 - x0) + x0)) 
        y[idx] = int((np.random.rand() * (y1 - y0) + y0))
    return x, y

def move(x, y):
    # Tar emot individers nuvarande koordinater.
    # Flyttar individen i x- och y-led med -1, 0, eller +1 steg
    # Returnerar de nya koordinaterna

    dx = np.random.choice([-1, 0, 1], (x.shape[0], 1))
    dy = np.random.choice([-1, 0, 1], (y.shape[0], 1))

    return x + dx, y + dy


def walls(nx, ny, min_x, min_y, max_x, max_y):
    # Tar emot individernas nya koordinater och gränserna på deras område
    # Applicerar gränserna på koordinaterna ifall de försöker flytta sig utanför området
    # Returnerar de nya koordinaterna

    nx[nx < min_x] = nx[nx < min_x] + 1
    nx[nx > max_x] = nx[nx > max_x] - 1

    ny[ny < min_y] = ny[ny < min_y] + 1
    ny[ny > max_y] = ny[ny > max_y] - 1

    return nx, ny








location0 = np.random.choice(list(location_limits.keys()),(N_indiv,1))

min_x, min_y, max_x, max_y = get_min_max(location0)

x0, y0 = random_location_coords(location0)

individuals = []

for coord_idx in range(x0.shape[0]):

    individuals.append(
        canvas.create_oval(
            x0[coord_idx][0]*ratio - 2,
            y0[coord_idx][0]*ratio - 2,
            x0[coord_idx][0]*ratio + 2,
            y0[coord_idx][0]*ratio + 2,
            outline='', fill="black"
        )
    )



location = location0
x = x0
y = y0


running = True

while running:
    nx, ny = move(x, y)

    for i, indiv in enumerate(individuals):
        canvas.coords(
            indiv,
            nx[i][0]*ratio - 2,
            ny[i][0]*ratio - 2,
            nx[i][0]*ratio + 2,
            ny[i][0]*ratio + 2
        )

    nx, ny = walls(nx, ny, min_x, min_y, max_x, max_y)

    x = nx
    y = ny

    

    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)


tk.update_idletasks()
tk.update()
tk.mainloop()
