#!/usr/bin/env python
# coding: utf-8

# In[1]:


#0. Imports, global variables and custom Class

import os
from pathlib import Path
from datetime import datetime


# In[2]:


#path to the Chrome data
CHROME_PATH = r'C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\chphlpgkkbolifaimnlloiipkdnihall'

#path to the desired backup/export folder
BACKUP_PATH = r'.\Backups'

#name of the text file to be saved
FILENAME = f"Onetab Backup {datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}" 
#old: 'Onetab_backup_'+ str(datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss'))


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
    returns the list of strings and the list of backups.
    
    strings,backups = read_backup()
        
    First we read the .log file and save its contents in the strings variable.
    strings is a list of strings. Each string can have one or multiple Onetab backups. 
    For example:
      strings=["backup_A", "'backup_b1''backup_b2''backup_b3'", "'backup_c1''backup_c2'"]
    In this case, there are 3 strings: the first has one backup, the second has three and the third has two.
    
    '''
    
    #selecting the most recent .log file in the onetab/chrome path
    p=Path(CHROME_PATH)
    file=sorted(p.glob("*.log"), key=os.path.getmtime, reverse=True)[0]
    
    #reading the file
    with open(file, encoding='utf8', errors="ignore") as f:
        strings=f.readlines()

    strings=[i.replace('\\','') for i in strings] #removing the annoying \\ chars inside x
    backups=[[i for i in j.split('\x00') if 'tabsMeta' in i] for j in [k for k in strings]]
    
    return [strings,backups]


#2. Data cleaning

def clean_data(x, _print=True):
    '''Gets a string containing a Onetab backup, cleans it 
    and returns a list of OneTabEntry objects and the ammount of objects.
    
    cleaned_backup,tab_count = clean_data(backup)
    
    My initial plan was to json.loads the log content so I could keep other information about the tabs,
     but I ended up having some issues with tabs that had ':' and '"' in its title, so I've scraped these plans
    Now the goal is just to get all saved tabs (url and titles)
    '''
    
    count=0
    if type(x) == type([]):
        x=''.join(x)
    x=x[x.find('"')+1:]
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


#3. Choosing the most up-to-date backup

def choosing_backup(backups):
    '''Gets the list of backups, chooses one backup to be considered the most up-to-date,
    cleans it and return the cleaned backup and the tab count.
    
    cleaned_backup_chosen,tab_count = choosing_backup(backups)
    
    We want to find the most up-to-date backup.
    Every new string is more up-to-date than the previous string.
    Every new backup inside a string is more up-to-date than the previous backup inside the same string.
    Sometimes a string might have 0 backups, and sometimes a backup might have 0 tabs.
    CONCLUSION: *The most up-to-date backup is the last not-null backup inside the last string that contains backups.*
    
    '''

    cleaned_data=[[clean_data(z,False) for z in j] for j in backups]

    #prints
    print(f'{len(backups)} Strings found:')
    for i in range(len(backups)):
        print(f'  String #{i} has {len(backups[i])} backups. Their tab count are: {[j[-1] for j in cleaned_data[i]]}')

    #finding the last not-null backup
    chosen=[]
    for data in cleaned_data[::-1]:
        for backup,count in data[::-1]:
            #print(count)
            if count>0:
                chosen=[backup,count]
                break
        if chosen:
            break
    print(f'\nThe backup chosen is the last not-null backup in the list. It has {chosen[-1]} tabs.')            
    
    return chosen


# In[7]:


#3. Creating a text file (containing the tabs) that can be imported to Onetab

def generate_string(cleaned_backup):
    '''Gets a clean backup and returns a Onetab-compatible string. 
    
    s = generate_string(cleaned_backup)
    '''
    
    s=''
    for i in cleaned_backup:
        s+='\n'.join([str(j) for j in i])
        s+='\n\n'
    print('Onetab-compatible string generated successfully.')
    return s

def save_txt(s):
    '''Gets a Onetab-compatible string and saves it in a text file.
    
    save_txt(s)
    '''    

    #creating backup folder is it doesn't exist
    if not Path(BACKUP_PATH).is_dir():
        Path(BACKUP_PATH).mkdir()
    #saving backup file
    with open(Path(BACKUP_PATH,FILENAME), mode='w',errors="ignore") as f:
        f.write(s)  
    #ending
    print(f'File "{FILENAME}" saved succesfully in the directory "{str(Path(BACKUP_PATH).resolve())}".')


# In[10]:


def main():
    strings,backups = read_backup()
    cleaned_backup_chosen,tab_count = choosing_backup(backups)
    s = generate_string(cleaned_backup_chosen)
    global FILENAME
    FILENAME += f' Tabs_{tab_count}.txt'
    save_txt(s)


# In[11]:


if __name__ == '__main__':
    main()

