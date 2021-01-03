# This was a quick, fun little python script created to graph the number of years of experience for a few skills I've gained over my career.
# This was meant to be a graph that could be added to a resume as something different/fun.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date

data_set = pd.DataFrame({'skills':['SQL Querying','Python','Storage','System Engineer','GitHub','JSON', 'Data Viz'],'years':[6,1,4,4,.5,.5,1]})
curr_time = date.today()
years_active = curr_time.year - 2009
x_ticks = np.arange(years_active+1)
use_color = 'dimgray'

ordered_data = data_set.sort_values(by='years')
skills_range=range(1,len(data_set.index)+1)

plt.hlines(y=skills_range, xmin=0, xmax=curr_time, colors=use_color)
plt.plot(ordered_data['years'], skills_range, "o", color=use_color)

plt.rcParams['text.color'] = use_color
plt.rcParams['axes.labelcolor'] = use_color
plt.rcParams['xtick.color'] = use_color
plt.rcParams['ytick.color'] = use_color

plt.yticks(skills_range, ordered_data['skills'])
plt.xticks(x_ticks)

sns.despine(top=True, right=True, left=True, bottom=True)

plt.show()
