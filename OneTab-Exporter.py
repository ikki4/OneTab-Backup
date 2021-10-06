#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
from datetime import datetime


#path to the Chrome data
CHROME_PATH = r'C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\chphlpgkkbolifaimnlloiipkdnihall'
#path to the desired backup/export folder
EXPORT_PATH = r'.\Backups'

class OneTabEntry:
    '''Gets a string "s" containing the tab's "id", "url" and "title", and creates an object that have 
    "id", "url" and "title" as attributes, and a method that returns a string "url | title", 
    just like OneTab's Import/Export feature.'''
    def __init__(self, s):
        self.id = s[s.find('"id":')+6:s.find('"url":')-2]
        self.url = s[s.find('"url":')+7:s.find('"title":')-2]
        self.title = s[s.find('"title":')+9:-1]
    def __str__(self): 
        return f"{self.url} | {self.title}"

def main():
    #1. locate OneTab's log file

    p=Path(CHROME_PATH)

    #selecting the most recent .log file in the onetab_path
    file=sorted(p.glob("*.log"), key=os.path.getmtime, reverse=True)[0]

    #2. Reading the .log file

    with open(file, encoding='utf8', errors="ignore") as f:
        x=f.readlines()

    #checking if x has a list of backups or a string with multiple backups
    #in case it's a string, it must be converted to a list of backups
    if len(x)==1:
        x=x[0].replace('\\','').split('\x00')
        x=[i for i in x if 'tabsMeta' in i]

    #finding most recent tabs backup, it's usually in the end of the list
    x.reverse()
    for backup in x:
        if 'tabsMeta' in backup:
            x=backup
            break

    #3. Data cleaning

    #My initial plan was to json.loads the log content so I could keep other information about the tabs,
    #but I ended up having some issues with tabs that had ':' and '"' in its title, so I've scraped these plans
    #Now the goal is just get all saved tabs (url and titles)
    #x and y are placeholders used on the data cleaning

    x=x[x.find('"')+1:x.find('ุง')].replace('\\','')
    y=x.split('"tabsMeta":')
    for i in range(len(y)):
        y[i]=y[i][1:y[i].find(']')]
        y[i]=y[i][1:-1].split("},{")
    groups=y[1:] #tab groups

    #4. Creating OneTabEntry objects

    for i in range(len(groups)):
        for j in range(len(groups[i])):
            #print(y[i][j])
            groups[i][j]=OneTabEntry(groups[i][j])

    #5. Creating a txt file (containing the tabs) that can be imported to Onetab

    s=''
    for group in groups:
        s+='\n'.join([str(tab_obj) for tab_obj in group])
        s+='\n\n'

    filename='Onetab_backup_'+str(datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss'))+'.txt'

    #creating export folder is it doesn't exist
    if not Path(EXPORT_PATH).is_dir():
        Path(EXPORT_PATH).mkdir()

    #saving export file
    with open(Path(EXPORT_PATH,filename), mode='w', errors="ignore") as f:
        f.write(s)
        
if __name__ == '__main__':
    main()
