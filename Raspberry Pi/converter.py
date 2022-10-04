# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 12:05:17 2022

@author: dstra
"""


a = ''
with open('code2.txt', 'r') as file :
    for line in file:
        a += line
    b = ''.join(a).strip()
    b = ''.join(b.splitlines())
        
def GPIOToBinary(GPIO):
    i = 0
    binary = []
    while i < len(GPIO):
        if GPIO[i] == '0':
            i += 1
        else:
            try:
                if GPIO[i+2] == '1':
                    binary.append('1')
                else: 
                    binary.append('0')
            except IndexError:
                break
            i += 3
    binary = ''.join(binary)
    return binary


def BinaryToText(binary):
    binint = int(binary, 2);
    byte = binint.bit_length() + 7 // 8
    binarray = binint.to_bytes(byte,'big')
    ascii_text = binarray.decode()
    text = ascii_text.strip('\x00')
    return text

binary = GPIOToBinary(b)
output = BinaryToText(binary)

print(output)