# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:30:43 2022

@author: dstra
"""
from datetime import datetime
import matplotlib.pyplot as pyplot
a = ''
with open('code2.txt', 'r') as file :
    for line in file:
        a += line
    a2 = a.split('\n')
    
b = ''
with open('code1.txt', 'r') as file :
    for line in file:
        b += line
    b2 = b.split('\n')


for i in range(len(b2)):
        b2[i] = b2[i].seconds + b2[i].microseconds/1000000.0

print('**Plotting results**')
pyplot.plot(b2, a2)
pyplot.axis([0, len(b2), -1, 2])
pyplot.show()