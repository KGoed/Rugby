import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os

#Get all links for 2019 from csv file
link_url = 'https://www.rugbypass.com/super-rugby/matches/2019/'
link_page = requests.get(link_url)
link_soup = BeautifulSoup(link_page.content,'html.parser')
links = []
for item in link_soup.find_all('a',href = True):
    if item.text == 'Match Centre': 
        links.append(item['href'] + '/stats/')
links.pop(0)
links.pop()
#links

for item in link_soup.find_all('a',class_='link-box',href = True):
    links.append(item['href'] + '/stats/')

output = []   
for i in links:
    stg = []
    stg.append(i[43:-12].replace('-vs','').replace('-at','').replace('-on',''))
    stg.append(1)
    stg.append('')
    stg.append(i)
    output.append(stg)

links = pd.DataFrame(output) 
links.columns = ['Match_ID','Round','Status','URL']
links.to_csv('Links_2019.csv',index=False)
