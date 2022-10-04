# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:17:18 2022

@author: dstra
"""
from datetime import datetime
import RPi.GPIO as GPIO


reader = [[],[]]
RECEIVE_PIN = 4

cumulative_time = 0
beginning_time = datetime.now()

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVE_PIN, GPIO.IN)
i = 0
while i < 250:
    time= datetime.now()
    timestring = time.strftime('%f')
    reader[0].append(timestring)
    a = GPIO.input(RECEIVE_PIN)
    b = str(a)
    reader[1].append(b)
    i+=1


print(reader)

with open('code1.txt', 'w') as file:
    file.write('\n'.join(reader[0]))

with open('code2.txt', 'w') as file:
    file.write('\n'.join(reader[1]))