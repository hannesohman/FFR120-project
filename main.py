import numpy as np
import time
from tkinter import *
import random as r


N_indiv = 1000

window_height = 600
window_width = 900



tk = Tk()
tk.geometry(f'{window_width}x{window_height}')
tk.configure(background='#000000')

canvas = Canvas(tk, background='#ECECEC')  # Generate animation window.
tk.attributes('-topmost', 0)
canvas.place(x=0, y=0, height=window_height, width=window_width)


locations = {
    "kårhuset": (400,10,850,90),
    "fysikhuset": (650,210,880,330),
    "kemihuset": (780,350,890,590),
    "biblioteket": (520,470,750,570),
}

for key, val in locations.items():
    canvas.create_rectangle(*val)


def random_location_coords(location):
    x0, y0, x1, y1 = locations[location]

    x = np.random.rand() * (x1 - x0) + x0
    y = np.random.rand() * (y1 - y0) + y0
    return x, y


# TIME:     0     ->       40     ->   60      ->     100
# Schedule:   Föreläsning       Lunch      Föreläsning

# Kemi: []


class Individual:
    def __init__(self, location) -> None:
        self.suseptibility = np.random.rand()
        self.status = 0
        self.location = location
        x,y = random_location_coords(location)
        self.x = x
        self.y = y

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.point = canvas.create_oval(
            self.x - 2,
            self.y - 2,
            self.x + 2,
            self.y + 2,
            outline='', fill="black"
        )


indiv = []

for ind in range(N_indiv):
    loc = r.choice(list(locations.keys()))
    individ = Individual(loc)
    indiv.append(individ)
    individ.draw()



    # x = np.random.rand()
    # y = np.random.rand()

    # individuals.append(
    #     canvas.create_oval(
    #         x * (kårhuset[2] - kårhuset[0]) - 2 + kårhuset[0],
    #         y * (kårhuset[3] - kårhuset[1]) - 2 + kårhuset[1],
    #         x * (kårhuset[2] - kårhuset[0]) + 2 + kårhuset[0],
    #         y * (kårhuset[3] - kårhuset[1]) + 2 + kårhuset[1],
    #         outline='', fill="black"
    #     )
    # )



tk.update_idletasks()
tk.update()
tk.mainloop()  # Release animation handle (close window to finish).

