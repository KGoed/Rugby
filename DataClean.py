import os
import pandas as pd

os.chdir('C:\\Users\\zw894hp\\Documents\Rugby\\')

links_raw = pd.read_csv('Links_2019.csv')
matches_raw = pd.read_csv('Team_Stats_2019.csv')
players_raw = pd.read_csv('Player_Stats_2019.csv')

players_cleaned = players_raw
players_cleaned.loc[players_cleaned['Player'] == 'Jean-Luc Du Preez', 'Player'] = 'Jean-Luc du Preez'
players_cleaned.loc[players_cleaned['Player'] == 'Ernst Van Rhyn', 'Player'] = 'Ernst van Rhyn'
players_cleaned.loc[players_cleaned['Player'] == 'Gerhard Van Den Heever', 'Player'] = 'Gerhard van den Heever'
players_cleaned.loc[players_cleaned['Player'] == 'Ivan Van Zyl', 'Player'] = 'Ivan van Zyl'
players_cleaned.loc[players_cleaned['Player'] == 'Johan Du Toit', 'Player'] = 'Johan du Toit'
players_cleaned.loc[players_cleaned['Player'] == 'Marco Van Staden', 'Player'] = 'Marco van Staden'
players_cleaned.loc[players_cleaned['Player'] == 'Pieter-Steph Du Toit', 'Player'] = 'Pieter-Steph du Toit'
players_cleaned.loc[players_cleaned['Player'] == 'Ruben Van Heerden', 'Player'] = 'Ruben van Heerden'
players_cleaned.loc[players_cleaned['Player'] == 'Thomas Du Toit', 'Player'] = 'Thomas du Toit'
players_cleaned.loc[players_cleaned['Player'] == 'Wilhelm Van Der Sluys', 'Player'] = 'Wilhelm van der Sluys'
players_cleaned.loc[players_cleaned['Player'] == 'Armand Van Der Merwe', 'Player'] = 'Armand van der Merwe'

players_cleaned.loc[players_cleaned['Player'] == 'Angus Taavao-Matau', 'Player'] = 'Angus Ta'+"'"+'avao'
players_cleaned.loc[players_cleaned['Player'] == 'Du’Plessis Kirifi', 'Player'] = 'Du'+"'"+'Plessis Kirifi'
players_cleaned.loc[players_cleaned['Player'] == 'Du'+"'"+'Plessis Kirifi', 'Player'] = 'Du'+"'"+'Plessis Kirifi'
players_cleaned.loc[players_cleaned['Player'] == 'Isileli Tuungafasi', 'Player'] = 'Isileli Tu'+"'"+'ungafasi'
players_cleaned.loc[players_cleaned['Player'] == 'Jeff Toomaga-Allen', 'Player'] = 'Jeff To'+"'"+'omaga-Allen'
players_cleaned.loc[players_cleaned['Player'] == 'Kane Leaupepe', 'Player'] = 'Kane Le'+"'"+'aupepe'
players_cleaned.loc[players_cleaned['Player'] == 'Matt Toomua', 'Player'] = 'Matt To'+"'"+'omua'
players_cleaned.loc[players_cleaned['Player'] == 'Ofa Tuungafasi', 'Player'] = 'Ofa Tu'+"'"+'ungafasi'
players_cleaned.loc[players_cleaned['Player'] == 'Dalton Papali'+"'"+'i', 'Player'] = 'Dalton Papalii'
players_cleaned.loc[players_cleaned['Player'] == 'Les Leulua'+"'"+'iali'+"'"+'i-Makin', 'Player'] = 'Les Makin'
players_cleaned.loc[players_cleaned['Player'] == 'Leslie Leulua'+"'"+'iali'+"'"+'i-Mankin', 'Player'] = 'Les Makin'
players_cleaned.loc[players_cleaned['Player'] == 'Leslie Leulua'+"'"+'iali'+"'"+'i-Makin', 'Player'] = 'Les Makin'
                                                  
players_cleaned.loc[players_cleaned['Player'] == 'Coenraad Oosthuizen', 'Player'] = 'Coenie Oosthuizen'
players_cleaned.loc[players_cleaned['Player'] == 'Enrique Pieretto Heilan', 'Player'] = 'Enrique Pieretto'
players_cleaned.loc[players_cleaned['Player'] == 'Hershel Jantjies', 'Player'] = 'Herschel Jantjies'
players_cleaned.loc[players_cleaned['Player'] == 'Kieran Reid', 'Player'] = 'Kieran Read'
players_cleaned.loc[players_cleaned['Player'] == 'Mbongeni Mbonami', 'Player'] = 'Mbongeni Mbonambi'
players_cleaned.loc[players_cleaned['Player'] == 'Paripari Parkinson', 'Player'] = 'Pari Pari Parkinson'
players_cleaned.loc[players_cleaned['Player'] == 'Phillip Van Der Walt', 'Player'] = 'Philip Van Der Walt'
players_cleaned.loc[players_cleaned['Player'] == 'Rosko Specman', 'Player'] = 'Rosco Specman'
players_cleaned.loc[players_cleaned['Player'] == 'Sefanaia Naivalo', 'Player'] = 'Sefanaia Naivalu'
players_cleaned.loc[players_cleaned['Player'] == 'Daniel Du Preez', 'Player'] = 'Daniel du Preez'

#remove match: highlanders-bulls-forsyth-barr-stadium-07062019
#players as well
indexNames = players_cleaned[players_cleaned['Match_ID'] == 'highlanders-bulls-forsyth-barr-stadium-07062019'].index
players_cleaned.drop(indexNames , inplace=True)

#remove Alex Hodgman, Otere Black, from  stormers-sunwolves-newlands-08062019
#       Taleni Seu from brumbies-blues-gio-stadium-04052019
indexNames = players_cleaned[(players_cleaned['Match_ID'] == 'stormers-sunwolves-newlands-08062019') & (players_cleaned['Player'] == 'Alex Hodgman')].index
players_cleaned.drop(indexNames , inplace=True)
indexNames = players_cleaned[(players_cleaned['Match_ID'] == 'stormers-sunwolves-newlands-08062019') & (players_cleaned['Player'] == 'Otere Black')].index
players_cleaned.drop(indexNames , inplace=True)
indexNames = players_cleaned[(players_cleaned['Match_ID'] == 'brumbies-blues-gio-stadium-04052019') & (players_cleaned['Player'] == 'Taleni Seu')].index
players_cleaned.drop(indexNames , inplace=True)

players = players_cleaned[['Player','Team']]
players = players.drop_duplicates()

def get_country(team):
    switcher={
        'CHI' : 'NZ',
        'HIG' : 'NZ',
        'BRU' : 'AUS',
        'REB' : 'AUS',
        'BLU' : 'NZ',
        'CRU' : 'NZ',
        'WAR' : 'AUS',
        'HUR' : 'NZ',
        'SUN' : 'JP',
        'SHA' : 'SA',
        'BUL' : 'SA',
        'STO' : 'SA',
        'JAG' : 'ARG',
        'LIO' : 'SA',
        'RED' : 'AUS',}
    return switcher.get(team,"Invalid")
    
    
players['Country'] = players['Team'].map(get_country)

players.to_csv('Players_2019.csv',index=False)
players_cleaned.to_csv('Player_Stats_2019_Cleaned.csv',index=False)