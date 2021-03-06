import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce

#Set page to get stats from
page = requests.get('https://www.rugbypass.com/live/super-rugby/chiefs-vs-highlanders-at-fmg-stadium-waikato-on-15022019/2019/stats/')
#page

#Convert page into BS object
soup = BeautifulSoup(page.content,'html.parser')

#Get headings of team stats that are sourced from bar graphs
stat_bars_headings = []
for i in soup.find_all('div',class_='label'):
    stat_string = i.text.strip()
    if stat_string != '':
        stat_bars_headings.append(i.text.strip())
stat_bars_headings[1] = 'Score'
stat_bars_headings[0] = 'Team'
#stat_bars_headings

#Get home stats for teams from the bar graphs
stat_bars_home= []
for i in soup.find_all('div',class_='home'):
    stat_string = i.text.strip()
    if stat_string != '' and len(stat_string) < 4:
        stat_bars_home.append(i.text.strip())
home = stat_bars_home[0]
#stat_bars_home

#Get away stats for teams from the bar graphs
stat_bars_away= []
for i in soup.find_all('div',class_='away'):
    stat_string = i.text.strip()
    if stat_string != '' and len(stat_string) < 4:
        stat_bars_away.append(i.text.strip())
stat_bars_away[0], stat_bars_away[1] = stat_bars_away[1], stat_bars_away[0]
away = stat_bars_away[0]
#stat_bars_away

#Convert the statss into a dataframe
teams_list = []
teams_list.append(stat_bars_home)
teams_list.append(stat_bars_away)

teams = pd.DataFrame(teams_list)
teams.columns = stat_bars_headings
#teams


#Get headers of the pie graphs used for team stats
check_list = ['Possession','Tries','Passes','Tackles','Kicks in play','Conversions','Rucks won','Rucks lost']
pie_headers = ['Team']
for i in soup.find_all('div', class_= 'key-stats-group-graph'):
    headers = i.text.split(',')
    for item in headers:
        string_check = item.replace('"','')
        if string_check in check_list:
            pie_headers.append(string_check)
#pie_headers


#Get the team stats from the pie graphs used
pie_stats = []
   
pie_home = [home]
pie_away = [away]
counter = 0

for i in soup.find_all('div', class_= 'key-stats-group-graph'):
    headers = i.text.split(',')
    for items in headers:
        if items.find('"') == -1:
            if items.find(';') == -1:
                counter += 1
                if (counter % 2) == 0:
                    pie_home.append(items)
                else:
                    pie_away.append(items)
pie_stats.append(pie_home)
pie_stats.append(pie_away)
#pie_stats

#Convert pie graph stats into dataframe
teams_pies = pd.DataFrame(pie_stats)
teams_pies.columns = pie_headers
#teams_pies


#Create final data frame for all team stats
team__stats_final = pd.merge(teams,teams_pies,on='Team')

#Get headings of all player stats
players_headers = ['Team','Number','Name']
for i in soup.find_all('th', class_='stat-value'):
    players_headers.append(i.get('title'))
       
players_headers = list(dict.fromkeys(players_headers))
#players_headers

#Get all player stats
check = []
player_att_stats = []
player_def_stats = []
player_kick_stats = []
player_setplay_stats = []
player_dis_stats = []
stat_counter = 0
player_counter = 0

for i in soup.find_all('td'):
    if i.text != '':
        check.append(i.text.strip())
        stat_counter += 1
        if 0 <= player_counter < 23:
            if stat_counter == 12:
                player_counter += 1
                check.insert(0,home)
                player_att_stats.append(check)
                check = []
                stat_counter = 0
        if 23 <= player_counter < 46:
            if stat_counter == 5:
                check.insert(0,home)
                player_def_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 46 <= player_counter < 69:
            if stat_counter == 6:
                check.insert(0,home)
                player_kick_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 69 <= player_counter < 92:
            if stat_counter == 5:
                check.insert(0,home)
                player_setplay_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 92 <= player_counter < 115:
            if stat_counter == 5:
                check.insert(0,home)
                player_dis_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 115 <= player_counter < 138:
            if stat_counter == 12:
                check.insert(0,away)
                player_att_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 138 <= player_counter < 161:
            if stat_counter == 5:
                check.insert(0,away)
                player_def_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 161 <= player_counter < 184:
            if stat_counter == 6:
                check.insert(0,away)
                player_kick_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0
        if 184 <= player_counter < 207:
            if stat_counter == 5:
                check.insert(0,away)
                player_setplay_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0                
        if 207 <= player_counter < 230:
            if stat_counter == 5:
                check.insert(0,away)
                player_dis_stats.append(check)
                check = []
                player_counter += 1
                stat_counter = 0                   
                

#Convert into dataframes
pl_att = pd.DataFrame(player_att_stats)
pl_att.columns = players_headers[:13]
#pl_att

pl_def = pd.DataFrame(player_def_stats)
pl_def.columns = list(players_headers[i] for i in [0, 1, 2, 13, 14, 15])
#pl_def

pl_kick = pd.DataFrame(player_kick_stats)
pl_kick.columns = list(players_headers[i] for i in [0,1, 2, 16, 17, 18, 19])
#pl_kick

pl_sp = pd.DataFrame(player_setplay_stats)
pl_sp.columns = list(players_headers[i] for i in [0,1, 2, 20, 21, 22])
#pl_sp

pl_dis = pd.DataFrame(player_dis_stats)
pl_dis.columns = list(players_headers[i] for i in [0,1, 2, 23, 24, 25])
#pl_dis

data_frames = [pl_att, pl_def, pl_kick, pl_sp, pl_dis]
player_stats_final = reduce(lambda left,right: pd.merge(left,right,on=['Team','Number','Name']), data_frames)

#player_stats_final
#team__stats_final
