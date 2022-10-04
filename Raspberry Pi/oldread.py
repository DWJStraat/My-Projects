# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:37:14 2022

@author: dstra
"""
import RPi.GPIO as GPIO


readerno = []
RECEIVE_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVE_PIN, GPIO.IN)


def byte():   
    i = 0
    reader = ''
    while i < 8 :
        read = (GPIO.input(RECEIVE_PIN))
        i += 1
        reader += str(read)
        readerint = int(reader, 2)
    return readerint
i = 0
while i < 8:
    read = byte()
    readerno.append(read)
    i += 1
print(readerno)
