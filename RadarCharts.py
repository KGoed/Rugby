import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import plotly.express as px
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')
links = pd.read_csv('Links_2019.csv')
matches = pd.read_csv('Team_Stats_2019.csv')
players_stats = pd.read_csv('Player_Stats_2019_Cleaned.csv')
players = pd.read_csv('Players_2019.csv')


elton = players_stats[players_stats['Player'] == 'Elton Jantjies'].groupby('Player',as_index=False)[['Runs','Passes','Kicks From Hand']].sum()
flys = players_stats[players_stats['Number'] == 10].groupby('Player',as_index=False)[['Runs','Passes','Kicks From Hand']].sum()
flys = pd.merge(flys,players,on='Player')
my_list = ['Elton Jantjies','Handre Pollard','Jean-Luc du Plessis','Robert du Preez']
sa_flys = flys[flys['Player'].isin(my_list)]



# number of variable
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
ax.plot(angles, values, linewidth=1, linestyle='solid', color = 'red')
 
# Fill area
ax.fill(angles, values, 'b', alpha=0.1, color = 'red')
