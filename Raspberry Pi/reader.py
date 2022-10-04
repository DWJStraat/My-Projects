# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:11:52 2022

@author: dstra
"""
import RPi.GPIO as GPIO
from datetime import datetime


MAX_DURATION = 5
RECEIVE_PIN = 4
reading = False
RECEIVED_SIGNAL= []

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVE_PIN, GPIO.IN)
count = 0
inputlist = []
cumulative_time = 0
beginning_time = datetime.now()

while cumulative_time < MAX_DURATION and reading == True:
    time_delta = datetime.now() - beginning_time
    if GPIO.input(RECEIVE_PIN) == 1        :
        collectin = True
    if RECEIVED_SIGNAL.len() == 8:
        collectin = False
        reading = False
    while collectin == True:
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        
    cumulative_time = time_delta.seconds

print(RECEIVED_SIGNAL)
    
    
