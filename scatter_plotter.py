# this program will plot a scatter plot of the max number of infections vs
# the alert level

# NOTE: the program assumes that only one alert level is active, ie we do NOT have a
# vaccination and a lockdown.

import plotter
import numpy as np
import matplotlib.pyplot as plt
import time

plt.rcParams["axes.edgecolor"] = "white"  # Set axes color to white
plt.rcParams["xtick.color"] = "white"  # Set x-tick color to white
plt.rcParams["ytick.color"] = "white"  # Set y-tick color to white
plt.rcParams["text.color"] = "white"  # Set text color to white
plt.rcParams["axes.labelcolor"] = "white"  # Set axes labels color to white
plt.rcParams["axes.titlecolor"] = "white"  # Set title color to white

# colors = ["blue", "orange"]
colors = ["#a777e9", "#eaa984"]


##########################################################################################
# scattering vaccine vs lockdown
##########################################################################################

# import data
datapath = "2024-12-13-16.25.16"
parameters, results = plotter.load_data(datapath)
datapath = "2024-12-13-16.30.11"
next_parameters, next_results = plotter.load_data(datapath)
parameters.extend(next_parameters)
results.extend(next_results)


fig, ax = plt.subplots()

# plot max infections
for parameter, result in zip(parameters, results):
    S, I, R, D = result
    max_infections = np.max(I)
    vaccine_alert = parameter["vaccine_alert"]
    lockdown_alert = parameter["lockdown_alert"]

    lockdown_was_used = lockdown_alert < vaccine_alert
    alert_level = lockdown_alert if lockdown_was_used else vaccine_alert

    color = colors[0] if lockdown_was_used else colors[1]
    label = "Lockdown" if lockdown_was_used else "Vaccination"

    # ensure no duplicate labels
    active_labels = ax.get_legend_handles_labels()[1]
    label = label if label not in active_labels else ""

    ax.scatter(alert_level, max_infections, color=color, label=label)


# also plot the average number of max_infections for no effort
datapath = "no_vacc_or_lockdown_12-14_2"
parameters, results = plotter.load_data(datapath)
unused_alert_level = 100

max_infections_list = []
for parameter, result in zip(parameters, results):
    S, I, R, D = result
    max_infections = np.max(I)
    vaccine_alert = parameter["vaccine_alert"]
    lockdown_alert = parameter["lockdown_alert"]
    if vaccine_alert >= unused_alert_level and lockdown_alert >= unused_alert_level:
        max_infections_list.append(max_infections)

max_infections_list = np.array(max_infections_list)
mean_infections_no_effort = np.mean(max_infections_list)

# plot max infections without any intervention
ax.axhline(
    mean_infections_no_effort,
    color="white",
    label="No efforts",
    linestyle="dashed",
)

# shrink plot to make space for legend outside
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# add legend (outside plot)
ax.legend(framealpha=0, bbox_to_anchor=(1, 0.5))

ax.set_title("Highest number of infections vs \nwhen effort was introduced")
ax.set_xlabel("New infections per day")
ax.set_ylabel("Highest number of infected individuals")


current_time = time.strftime("%Y-%m-%d-%H.%M.%S")
plt.savefig(f"./plots/scatter/{current_time}.png", transparent=True, dpi=300)
# plt.show()
plt.close()
plt.clf()

##########################################################################################
# scattering different vaccine modes
##########################################################################################

# import data
datapath = "2024-12-14-11.48.52"
parameters, results = plotter.load_data(datapath)

fig, ax = plt.subplots()

# plot max infections
for parameter, result in zip(parameters, results):
    S, I, R, D = result
    max_infections = np.max(I)
    alert_level = parameter["vaccine_alert"]
    vaccine_mode = parameter["vaccine_mode"]
    random_was_used = vaccine_mode == "random"
    print(vaccine_mode)
    print(random_was_used)

    color = colors[0] if random_was_used else colors[1]
    label = "Random" if random_was_used else "Risk group"

    # ensure no duplicate labels
    active_labels = ax.get_legend_handles_labels()[1]
    label = label if label not in active_labels else ""

    ax.scatter(alert_level, max_infections, color=color, label=label)


# also plot the average number of max_infections for no effort
datapath = "no_vacc_or_lockdown_12-14_2"
parameters, results = plotter.load_data(datapath)
unused_alert_level = 100

max_infections_list = []
for parameter, result in zip(parameters, results):
    S, I, R, D = result
    max_infections = np.max(I)
    vaccine_alert = parameter["vaccine_alert"]
    lockdown_alert = parameter["lockdown_alert"]
    if vaccine_alert >= unused_alert_level and lockdown_alert >= unused_alert_level:
        max_infections_list.append(max_infections)

max_infections_list = np.array(max_infections_list)
mean_infections_no_effort = np.mean(max_infections_list)

# plot max infections without any intervention
ax.axhline(
    mean_infections_no_effort,
    color="white",
    label="No efforts",
    linestyle="dashed",
)

# shrink plot to make space for legend outside
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# add legend (outside plot)
ax.legend(framealpha=0, bbox_to_anchor=(1, 0.5))

ax.set_title("Highest number of infections vs \nwhen effort was introduced")
ax.set_xlabel("New infections per day")
ax.set_ylabel("Highest number of infected individuals")


current_time = time.strftime("%Y-%m-%d-%H.%M.%S")
plt.savefig(f"./plots/scatter/{current_time}.png", transparent=True, dpi=400)
# plt.show()
plt.close()
plt.clf()
