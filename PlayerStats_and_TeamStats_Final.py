import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
import os
import time

#Get all links for 2019
os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')
full_matches = pd.read_csv('Links_2019.csv')
matches = full_matches['URL'].loc[full_matches['Status'] != 'No Stats']

#url = matches[0]
#url2 = matches[71]
for url in matches:
    match_id = url[43:-12].replace('-vs','').replace('-at','').replace('-on','')
    #time.sleep(2)
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')   
    
    tables = soup.find_all('table')
    home = soup.find('div', class_='team-abrev home').text
    away = soup.find('div', class_='team-abrev away').text
    home_score = soup.find('div', class_='home team-home-score').text.strip()
    away_score = soup.find('div', class_='away team-away-score').text.strip()

    #Team Stats 
    t_headings = ['Team','Score']
    t_home =[home,home_score]
    t_away = [away,away_score]
    
    for x in soup.find_all('div', class_='titles'):
        for y in x:
            if y != ' ':
                if str(y.get('class')).replace('[','').replace(']','').replace("'",'').replace("'",'') == 'label':
                    t_headings.append(y.text)
                if str(y.get('class')).replace('[','').replace(']','').replace("'",'').replace("'",'') == 'home':
                    t_home.append(y.text)
                if str(y.get('class')).replace('[','').replace(']','').replace("'",'').replace("'",'') == 'away':
                    t_away.append(y.text)               
    t_stg = [t_home]
    t_stg.append(t_away)
    team_stg = pd.DataFrame(t_stg, columns = t_headings)
    
    check_list = ['Possession','Tries','Passes','Tackles','Kicks in play','Conversions','Rucks won','Rucks lost']
    pie_headers = ['Team']
    for i in soup.find_all('div', class_= 'key-stats-group-graph'):
        headers = i.text.split(',')
        for item in headers:
            string_check = item.replace('"','')
            if string_check in check_list:
                pie_headers.append(string_check)
    
    #Get the team stats from the pie graphs used
    pie_stats = []
    pie_home = [home]
    pie_away = [away]
    counter = 0
    
    for i in soup.find_all('div', class_= 'key-stats-group-graph'):
        if i.text.find('Drop') == -1:
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
    
    team_stats_stg = pd.merge(team_stg,teams_pies,on='Team')
    team_stats_stg['Match_ID'] = match_id
    
    if 'team_stats_final' not in locals():
        team_stats_final = team_stats_stg
    else:
        team_stats_final = team_stats_final.append(team_stats_stg, sort = False)

     #Players Stat
    def get_table(t):
        table_rows = t.find_all('tr')
           
        l = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td]
            l.append(row)
            
        h = []
        for i in table_rows:
            th = i.find_all('th')
            col = [i.text.strip() for i in th]
            h.append(col)
        
        thrs = []
        for i in table_rows:
            thr = i.find_all('th')
            col = [i.get('title') for i in thr]
            thrs.append(col)
            
        headers = h[0]
        headers[0] = 'Number'
        
        act_headers = thrs[0]
        act_headers[0] = 'Number'
        act_headers[1] = 'Player'
        df = pd.DataFrame(l, columns = act_headers)
        df = df.dropna()
        return df
    
    home_attacking = get_table(tables[0])
    home_defence = get_table(tables[1])
    home_kicking = get_table(tables[2])
    home_setplay = get_table(tables[3])
    home_discipline = get_table(tables[4])
    away_attacking = get_table(tables[5])
    away_defence = get_table(tables[6])
    away_kicking = get_table(tables[7])
    away_setplay = get_table(tables[8])
    away_discipline = get_table(tables[9])
    
    home_attacking['Player'] = home_attacking['Player'].str.strip()
    home_defence['Player'] = home_defence['Player'].str.strip()
    home_kicking['Player'] = home_kicking['Player'].str.strip()
    home_setplay['Player'] = home_setplay['Player'].str.strip()
    home_discipline['Player'] = home_discipline['Player'].str.strip()
    away_attacking['Player'] = away_attacking['Player'].str.strip()
    away_defence['Player'] = away_defence['Player'].str.strip()
    away_kicking['Player'] = away_kicking['Player'].str.strip()
    away_setplay['Player'] = away_setplay['Player'].str.strip()
    away_discipline['Player'] = away_discipline['Player'].str.strip()
    
    data_frames = [home_attacking, home_defence, home_kicking, home_setplay, home_discipline]
    home_stats = reduce(lambda left,right: pd.merge(left,right,on=['Number','Player']), data_frames)
    
    data_frames = [away_attacking, away_defence, away_kicking, away_setplay, away_discipline]
    away_stats = reduce(lambda left,right: pd.merge(left,right,on=['Number','Player']), data_frames)
    
    home_stats['Team'] = home
    home_stats['Venue'] = 'Home'
    home_stats['Match_ID'] = match_id
    away_stats['Team'] = away
    away_stats['Venue'] = 'Away'
    away_stats['Match_ID'] = match_id
    
    player_stats_stg = home_stats
    player_stats_stg = player_stats_stg.append(away_stats)
    
    if 'Try Scored' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Try Scored':'Tries'},inplace= True)
    if 'Ball Carry Meters' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Ball Carry Meters':'Carries Metres'},inplace= True)
    if 'Ball Carry' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Ball Carry':'Runs'},inplace= True)
    if 'Beat Defender' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Beat Defender':'Defenders Beaten'},inplace= True)
    if 'Line Break' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Line Break':'Clean Breaks'},inplace= True)
    if 'Total Turnovers Conceded' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Total Turnovers Conceded':'Turnovers Conceded'},inplace= True)
    if 'Points Scored' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Points Scored':'Points'},inplace= True)
    if 'Tackle Made' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Tackle Made':'Tackles'},inplace= True)
    if 'Tackle Missed' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Tackle Missed':'Missed Tackles'},inplace= True)
    if 'Total Turnovers Gained' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Total Turnovers Gained':'Turnover Won'},inplace= True)
    if 'Conversion Successful' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Conversion Successful':'Conversion Goals'},inplace= True)
    if 'Penalty Goal Successful' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Penalty Goal Successful':'Penalty Goals'},inplace= True)
    if 'Drop Kick Successful' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Drop Kick Successful':'Drop Goals Converted'},inplace= True)
    if 'Lineout Won Own Throw' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Lineout Won Own Throw':'Lineout Throw Won Clean'},inplace= True)
    if 'Red Card' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Red Card':'Red Cards'},inplace= True)
    if 'Yellow Card' in player_stats_stg.columns:
        player_stats_stg.rename(columns={'Yellow Card':'Yellow Cards'},inplace= True)
        
    if 'player_stats_final' not in locals():
        player_stats_final = player_stats_stg
    else:
        player_stats_final = player_stats_final.append(player_stats_stg, sort = False)
        
player_stats_final.to_csv('Player_Stats_2019.csv',index=False)
team_stats_final.to_csv('Team_Stats_2019.csv',index=False)
