# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 22:49:26 2022

@author: USER
"""

# ROOT = 'C:/Users/USER/Desktop/'
ROOT = '/home/shpark/stella/stella_install/sboproject/run/'
newROOT = None

def croot(a):
    global newROOT
    newROOT = a
    
def get_filename(*a):
    global ROOT,newROOT

    if newROOT == None:
        fname = ROOT
    else:
        fname = newROOT
    
    if a[0].split(sep='.')[-1] in ['res','swd','tt','ph','hyd','abn']:
        a_ = a[0].split(sep=fname)[-1]
        fname += a_[:-len(a_.split(sep='.')[-1])-1]
    else:        
        for i in a:
            fname += i + '/'
        fname = fname[:-1]
        
    return fname