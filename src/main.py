import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.interpolation import lagrange
from src.CubicSpline2 import *
from src.CubicSpline import *
import seaborn as sns


sns.set()

def set_lims_and_show(elevation_profile):
    plt.xlim(left=elevation_profile['D'].min() - 1000, right=elevation_profile['D'].max() + 1000)
    plt.ylim(bottom=elevation_profile['W'].min() - 1000, top=elevation_profile['W'].max() + 1000)
    plt.show()



elevation_profile = pd.read_csv("../data/2018_paths/GlebiaChallengera.csv")
elevation_profile.columns = ['D', 'W']
print(elevation_profile.keys())
print(elevation_profile.head())

#
elevation_profile.plot('D', 'W', linestyle='none', marker='o', markersize=1.5)
plt.title('Original elevation profile')
plt.xlabel('Distance [m]')
plt.ylabel('Height [m]')
plt.legend(['Height'])
set_lims_and_show(elevation_profile)



# Num of points to save
interval_size = 1
# Steps between intervals
steps = 25



cut_profile = pd.DataFrame(
    {'D': [],
     'W': []
     }
)
#Probe the profile for x intervals
for i in range(0, elevation_profile.shape[0], steps):
    if i+interval_size > elevation_profile.shape[0]:
        cut_profile = cut_profile.append(elevation_profile.iloc[i:])
        break
    else:
        cut_profile = cut_profile.append(elevation_profile.iloc[i:i + interval_size])


cut_profile.plot('D', 'W', linestyle='none', marker='o', markersize=1.5)
plt.title('Reduced elevation profile')
plt.xlabel('Distance [m]')
plt.ylabel('Height [m]')
plt.legend(['Height'])
set_lims_and_show(elevation_profile)


# Get the x axis values to list

x_list = np.array(cut_profile['D'].tolist())
y_list = np.array(cut_profile['W'].tolist())
y_res = np.array([])
x_res = np.array(elevation_profile['D'].tolist())

# LAGRANGE

start_time = time.time()


for i in range(len(x_res)):
    y_res = np.append(y_res, lagrange(x_res[i], x_list, y_list))

elapsed_time = time.time() - start_time
print(str(elapsed_time) + "s")

lagrange_profile = pd.DataFrame(
    {'D': x_res[:len(y_res)],
     'W': y_res
     }
)

print(lagrange_profile.head())
lagrange_profile.plot('D', 'W')
plt.title('Elevation profile interpolated with Lagrange\'s')
plt.xlabel('Distance [m]')
plt.ylabel('Height [m]')
plt.legend(['Height'])
set_lims_and_show(elevation_profile)




# SPLINES
#spline = Spline(x_list, y_list)
spline = CubicSpline(x_list, y_list)
y_res = np.array([])

start_time = time.time()
for i in x_res:
    y_res = np.append(y_res, spline.get(i))

elapsed_time = time.time() - start_time
print(str(elapsed_time) + "s")

spline_profile = pd.DataFrame(
    {'D': x_res[:len(y_res)],
     'W': y_res
     }
)

print(spline_profile.head())
spline_profile.plot('D', 'W')
plt.title('Elevation profile interpolated with splines method')
plt.xlabel('Distance [m]')
plt.ylabel('Height [m]')
plt.legend(['Height'])
set_lims_and_show(elevation_profile)



# Visualize everything on single graph
plt.plot(elevation_profile['D'].tolist(), elevation_profile['W'].tolist(), '.')
plt.plot(cut_profile['D'].tolist(), cut_profile['W'].tolist(), 'D', markersize=12)
plt.plot(spline_profile['D'].tolist(), spline_profile['W'].tolist(), linewidth='3')
plt.plot(lagrange_profile['D'].tolist(), lagrange_profile['W'].tolist(), '--')
plt.legend(['Original', 'Reduced', 'Splines', 'Langrange'])
set_lims_and_show(elevation_profile)
