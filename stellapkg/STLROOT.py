# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 22:49:26 2022

@author: USER
"""

ROOT = 'C:/Users/USER/Desktop/'
newROOT = None

def croot(a):
    global newROOT
    newROOT = a
    
def get_filename(a):
    global ROOT,newROOT
    if newROOT == None:
        fname = ROOT
    else:
        fname = newROOT
    for i in a:
        fname += i + '/'
    fname += a[0]
    return fname