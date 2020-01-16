import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import plotly.express as px

os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')
links = pd.read_csv('Links_2019.csv')
matches = pd.read_csv('Team_Stats_2019.csv')
players = pd.read_csv('Player_Stats_2019.csv')

match = links['Match_ID'][0]
match_stats = matches[matches['Match_ID'] == match]
player_stats = players[players['Match_ID'] == match]


player_stats[player_stats['Venue'] == 'Home']['Carries Metres'].sum(axis = 0, skipna = True)
player_stats[player_stats['Venue'] == 'Away']['Carries Metres'].sum(axis = 0, skipna = True)
match_stats['Metres carried']


player_stats[player_stats['Venue'] == 'Home']['Carries Metres']
player_stats[player_stats['Venue'] == 'Home']['Carries Metres'].plot.line()

player_stats[player_stats['Venue'] == 'Away'].plot.bar(x = 'Player', y = 'Carries Metres')

cm = players.groupby('Player')[['Carries Metres','Runs']].sum()
cm = cm.sort_values('Carries Metres',ascending = False).reset_index()

elton = players[players['Player'] == 'Elton Jantjies'].groupby('Player',as_index=False)[['Runs','Passes','Kicks From Hand']].sum()
flys = players[players['Number'] == 10].groupby('Player',as_index=False)[['Runs','Passes','Kicks From Hand']].sum()


# number of variable


import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


categories=list(elton)[1:]
N = len(categories)
 # We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
values=elton.loc[0].drop('Player').values.flatten().tolist()
values += values[:1]
values
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories, color='grey', size=8)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([100,200,300], ["100","200","300"], color="grey", size=7)
plt.ylim(0,400)
 
# Plot data
ax.plot(angles, values, linewidth=1, linestyle='solid')
 
# Fill area
ax.fill(angles, values, 'b', alpha=0.1)
