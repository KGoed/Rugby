import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')
links = pd.read_csv('Links_2019.csv')
matches = pd.read_csv('Team_Stats_2019.csv')
players_stats = pd.read_csv('Player_Stats_2019_Cleaned.csv')
players = pd.read_csv('Players_2019.csv')

players_stats['game_count'] = 1
flys = players_stats[players_stats['Number'] == 10].groupby('Player',as_index=False)[['Runs','Passes','Kicks From Hand','game_count']].sum()
flys = pd.merge(flys,players,on='Player')

flys['Runs'] = round(flys['Runs'] / flys['game_count'],1)
flys['Passes'] = round(flys['Passes'] / flys['game_count'],1)
flys['Kicks From Hand'] = round(flys['Kicks From Hand'] / flys['game_count'],1)

#my_list = ['Elton Jantjies','Handre Pollard','Jean-Luc du Plessis','Robert du Preez']
my_list = ['Elton Jantjies','Handre Pollard','Robert du Preez']

sa_flys = flys[flys['Player'].isin(my_list)][['Player','Runs','Passes','Kicks From Hand']]
sa_flys = sa_flys.reset_index(drop=True)


# number of variable
categories=list(sa_flys)[1:]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([5,10,15,20,25], ['5','10','15','20','25'], color="grey", size=7)
plt.ylim(0,25)

values=sa_flys.loc[0].drop('Player').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Elton")
ax.fill(angles, values, 'b', alpha=0.1)

values=sa_flys.loc[1].drop('Player').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Pollard")
ax.fill(angles, values, 'r', alpha=0.1)

values=sa_flys.loc[2].drop('Player').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="du Preez")
ax.fill(angles, values, 'r', alpha=0.1)

plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

