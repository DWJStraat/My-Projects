# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 12:05:11 2022

@author: dstra
"""

import csv
translated = []
with open('Draconic.csv', 'r') as words:
    reader = csv.reader(words)
    draconic = {rows[0].upper():rows[1].upper() for rows in reader}

    common = {v:k for k, v in draconic.items()}

language = input('Translate to [D]raconic or [C]ommon?\n').upper()

if language == 'D':
    string = input('Enter your sentence:\n').upper()
    string = string.split()
    for i in string:
        try:
            translated.append(common[i]) 
        except: 
            translated.append(i)
if language == 'C':
    print('Enter your sentence below:\n', '-'*50)
    string = input().upper()
    string = string.split()
    for i in string:
        try:
            translated.append(draconic[i]) 
        except: 
            translated.append(i)

output = ' '.join(translated).capitalize()
print(output)
    
