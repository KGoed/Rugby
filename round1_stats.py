import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

os.chdir('C:\\Users\\zw894hp\\Documents\\Rugby\\Round1\\')

team_stats = pd.read_csv('Round1_Teams_2020.csv')
ply_stats = pd.read_csv('Round1_Players_2020.csv')

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

col_list = {'BLU':'blue',
            'BRU':'orange',
            'BUL':'blue',
            'CHI':'orange',
            'CRU':'red',
            'HIG':'green',
            'HUR':'orange',
            'JAG':'orange',
            'LIO':'red',
            'REB':'blue',
            'RED':'red',
            'SHA':'black',
            'STO':'midnightblue',
            'SUN':'red',
            'WAR':'blue'
            }



col_cnt_list = {'ARG':'blue',
            'AUS':'gold',
            'JAP':'red',
            'NZ':'black',
            'SA':'green'
            }


stats_required = team_stats.columns.tolist()
stats_required = ['Team',	'Score',	'Defenders beaten',	'Clean breaks',	'Offloads',	'Turnovers conceded',	'Missed tackles',	'Turnovers won',	'Conversions missed',	'Penalty goals',	'Penalty goals missed',	'Drop goals',	'Drop goals missed',	'Rucks won %',	'Mauls won',	'Lineouts lost',	'Scrums won',	'Scrums lost',	'Scrums won %',	'Penalties conceded',	'Possession',	'Territory',	'Tries',	'Passes',	'Tackles',	'Kicks in play',	'Conversions',	'Rucks won',	'Rucks lost', 'Match_ID']
stats_required = ['Team',
                  'Possession','Territory', #general
                  'Passes','Kicks in play','Offloads', #att
                  'Defenders beaten','Clean breaks', #att
                  'Missed tackles','Tackles', #def
                  'Turnovers conceded','Penalties conceded', #errors
                  'Turnovers won','Rucks won %','Scrums won %',
                  'Match_ID']

main_stats = team_stats[stats_required]




main_stats.rename(columns={'Rucks won %':'Rucks Won'}, inplace=True)
main_stats.rename(columns={'Scrums won %':'Scrums Won'}, inplace=True)

categories=list(main_stats)[1:]
categories.remove('Match_ID')
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

matches = list(dict.fromkeys(list(main_stats['Match_ID'])))

for m in matches:
    grph_stats = main_stats[main_stats['Match_ID']== m]
    grph_stats = grph_stats.reset_index(drop=True)

    for c in grph_stats.columns:
        if c not in ['Team','Match_ID']:
            total = grph_stats[c].sum(axis=0)
            grph_stats[c].loc[0] =   round(grph_stats[c].loc[0] / total * 100,0)
            grph_stats[c].loc[1] =   round(grph_stats[c].loc[1] / total * 100,0)
    
       
    #loop from here:
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30,40,50,60,70,80,90], ['','','','','','','','',''],color="grey", size=7)
    plt.ylim(0,90)  
    
    for i in range(0,len(grph_stats)):
        tm = grph_stats.iloc[i]['Team']
        values= grph_stats.loc[i].drop(['Team','Match_ID']).values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=tm, color = col_list[tm])
        ax.fill(angles, values, 'b', alpha=0.1, color = col_list[tm])
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    save_string = m +'.png'
    plt.savefig(save_string, bbox_inches='tight')
    plt.show()
    
    
    

    
    
    