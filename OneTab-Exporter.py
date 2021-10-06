#!/usr/bin/env python
# coding: utf-8

# In[1]:


#0. Imports, global variables and custom Class

import os
import re
from pathlib import Path
from datetime import datetime


# In[2]:


#path to the Chrome data
CHROME_PATH = r'C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\chphlpgkkbolifaimnlloiipkdnihall'

#path to the desired backup/export folder
EXPORT_PATH = r'.\Backups'

#name of the text file to be saved
FILENAME = 'Onetab_backup_'+ str(datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')) +'.txt'


# In[3]:


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


# In[4]:


#1. Locating the .log file, Reading it and finding the most up-to-date Onetab backup

def read_backup():
    '''Reads the .log file in the Onetab/Chrome data folder, and
    returns a list of strings, a list of backups and the most recent backup.
    strings,backups,chosen_backup = read_backup()
        
    First we read the .log file and save its contents in the strings variable.
    strings is a list of strings. Each string can have one or multiple Onetab backups. 
    For example:
      strings=["backup_A", "'backup_b1''backup_b2''backup_b3'", "'backup_c1''backup_c2'"]
    In this case, there are 3 strings: the first has one backup, the second has three and the third has two.
    We want to find the most up-to-date backup.
    We find the most up-to-date string by finding the string who has the highest "updateDate" timestamp value.
      * It usually ends up being the last string in strings
    There's no way to find the most up-to-date backup inside a string, though.
    But as of my testings, the most up-to-date backup usually is *THE LAST BACKUP INSIDE THE MOST UP-TO-DATE STRING*.
    
    This function explains a lot and returns a lot of stuff for testing purposes. 
    Help us figure out more about this obscure OneTab backup feature!
    '''
    
    #selecting the most recent .log file in the onetab/chrome path
    p=Path(CHROME_PATH)
    file=sorted(p.glob("*.log"), key=os.path.getmtime, reverse=True)[0]
    
    #reading the file
    with open(file, encoding='utf8', errors="ignore") as f:
        strings=f.readlines()

    #finding out the most up-to-date string (it's usually the last one)
    strings=[i.replace('\\','') for i in strings] #removing the annoying \\ chars inside x
    pattern=re.compile(r'"updateDate":(\d+)')
    try:
        timestamps = [max([int(i) for i in pattern.findall(j)]) for j in strings] #list of the highest timestamp value in each string
        index=timestamps.index(max(timestamps)) #index of the most up-to-date string, if regex fails use index=-1
    except Exception:
        index=-1
    #getting a list of backups
    backups=[[i for i in j.split('\x00') if 'tabsMeta' in i] for j in [k for k in strings]]

    #most up-to-date backup is the last backup inside the most up-to-date string, so it´s in backups[index][-1]

    #prints
    print(f'{len(backups)} Strings found:')
    for i in range(len(backups)):
        print(f'  String #{i} has {len(backups[i])} backups. Their tab count are: {[clean_data(z,False)[-1] for z in backups[i]]}')
    print(f'\nThe most up-to-date backup seems to be the last backup in String #{index}.')
    
    #returning the list of strings, the lists of backups and the most up-to-date backup
    return [strings,backups,backups[index][-1]]


# In[5]:


#2. Data cleaning

def clean_data(x, _print=True):
    '''Gets a string containing a Onetab backup, cleans it 
    and returns a list of OneTabEntry objects and the ammount of objects.
    
    clean_backup,tab_count = clean_data(chosen_backup)
    
    
    My initial plan was to json.loads the log content so I could keep other information about the tabs,
     but I ended up having some issues with tabs that had ':' and '"' in its title, so I've scraped these plans
    Now the goal is just to get all saved tabs (url and titles)
    '''
    
    count=0
    if type(x) == type([]):
        x=''.join(x)
    x=x[x.find('"')+1:x.find('ا')]
    y=x.split('"tabsMeta":')
    for i in range(len(y)):
        y[i]=y[i][1:y[i].find(']')]
        y[i]=y[i][1:-1].split("},{")
    y=y[1:]
    for i in range(len(y)):
        for j in range(len(y[i])):
            y[i][j]=OneTabEntry(y[i][j])
            count+=1
    if _print:
        print(f'Backup cleaned successfully. {count} tabs were found.')
    return y,count


# In[6]:


#3. Creating a text file (containing the tabs) that can be imported to Onetab

def generate_string(clean_backup):
    '''Gets a clean backup and returns a Onetab-compatible string. 
    
    s = generate_string(clean_backup)
    '''
    
    s=''
    for i in clean_backup:
        s+='\n'.join([str(j) for j in i])
        s+='\n\n'
    print('Onetab-compatible string generated successfully.')
    return s

def save_txt(s):
    '''Gets a Onetab-compatible string and saves it in a text file.
    
    save_txt(s)
    '''    

    #creating export folder is it doesn't exist
    if not Path(EXPORT_PATH).is_dir():
        Path(EXPORT_PATH).mkdir()
    #saving export file
    with open(Path(EXPORT_PATH,FILENAME), mode='w',errors="ignore") as f:
        f.write(s)  
    #ending
    print(f'File "{FILENAME}" saved succesfully in the directory "{str(Path(EXPORT_PATH).resolve())}".')


# In[7]:


def main():
    strings,backups,chosen_backup = read_backup()
    clean_backup,tab_count = clean_data(chosen_backup)
    s = generate_string(clean_backup)
    save_txt(s)


# In[8]:


if __name__ == '__main__':
    main()

