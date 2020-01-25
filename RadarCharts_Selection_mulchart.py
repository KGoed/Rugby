import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

#Set up values
stats_required = ['Runs','Passes','Kicks From Hand']
teams = []
position = ['10']
countries = ['JAP']
plys = []

charts = 'Multiple' 
#charts = 'Single'

cnt_list = {'BLU':'NZ',
            'BRU':'AUS',
            'BUL':'SA',
            'CHI':'NZ',
            'CRU':'NZ',
            'HIG':'NZ',
            'HUR':'NZ',
            'JAG':'ARG',
            'LIO':'SA',
            'REB':'AUS',
            'RED':'AUS',
            'SHA':'SA',
            'STO':'SA',
            'SUN':'JAP',
            'WAR':'AUS'
            }

col_list = {'BLU':'blue',
            'BRU':'gold',
            'BUL':'cornflowerblue',
            'CHI':'darkgoldenrod',
            'CRU':'darkred',
            'HIG':'green',
            'HUR':'yellow',
            'JAG':'orange',
            'LIO':'red',
            'REB':'navy',
            'RED':'firebrick',
            'SHA':'black',
            'STO':'midnightblue',
            'SUN':'lightsalmon',
            'WAR':'cyan'
            }

col_cnt_list = {'ARG':'blue',
            'AUS':'gold',
            'JAP':'red',
            'NZ':'black',
            'SA':'green'
            }
#Import stats
os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')
links = pd.read_csv('Links_2019.csv')
matches = pd.read_csv('Team_Stats_2019.csv')
players_stats = pd.read_csv('Player_Stats_2019_Cleaned.csv')
players = pd.read_csv('Players_2019.csv') #try not to need this
players_stats['game_count'] = 1
players_stats['Country'] = players_stats['Team'].apply(lambda x: cnt_list[x])
ply_team = players.set_index('Player')['Team'].to_dict()

full_stats = players_stats

if len(plys) > 0:
    full_stats = full_stats[full_stats['Player'].isin(plys)]

if len(teams) > 0:
    full_stats = full_stats[full_stats['Team'].isin(teams)]

if len(countries) > 0:
    full_stats = full_stats[full_stats['Country'].isin(countries)]

if len(position) > 0:
    full_stats = full_stats[full_stats['Number'].isin(position)]

full_stats = full_stats.drop(['Number','Team','Venue','Match_ID','Country'], axis = 1)
full_stats = full_stats.groupby('Player',as_index=False).sum()

for col in full_stats.columns:
    if col not in ('Player','game_count'):
        full_stats[col] = round(full_stats[col] / full_stats['game_count'],1)


#my_list = ['Elton Jantjies','Handre Pollard','Jean-Luc du Plessis','Robert du Preez']
stats_required.insert(0,'Player')
grph_stats = full_stats[stats_required]

# number of variable
categories=list(grph_stats)[1:]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

if charts == 'Multiple':
    for i in range(0,len(grph_stats)):
    # Initialise the spider plot
        ax = plt.subplot(111, polar=True)
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        plt.xticks(angles[:-1], categories)
         
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([5,10,15,20,25], ['5','10','15','20','25'], color="grey", size=7)
        plt.ylim(0,25)
         
        plyr = grph_stats.iloc[i]['Player']
        values= grph_stats.loc[i].drop('Player').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=plyr, color = col_list[ply_team[plyr]])
        ax.fill(angles, values, 'b', alpha=0.1, color = col_list[ply_team[plyr]])
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        save_string = 'graph'+str(i)+'.png'
        plt.savefig(save_string, bbox_inches='tight')
        plt.show()

else:
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([5,10,15,20,25], ['5','10','15','20','25'], color="grey", size=7)
    plt.ylim(0,25)  
    
    for i in range(0,len(grph_stats)):
        plyr = grph_stats.iloc[i]['Player']
        values= grph_stats.loc[i].drop('Player').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=plyr)
        ax.fill(angles, values, 'b', alpha=0.1)
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig('graph.png', bbox_inches='tight')
    plt.show()

    
    

