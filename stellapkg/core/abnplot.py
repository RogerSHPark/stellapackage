#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 17:34:55 2022

@author: shpark
"""

from stellapkg.parser.ABNparser import abn_data
from stellapkg.parser.HYDparser import hyd_data

import numpy as np
import matplotlib.pyplot as plt

def abnplot(a,xkey='mass',ylog=True,oplot=False):
    
    abn = abn_data(a).data
    hyd = hyd_data(a).data
    
    Mtot = np.max(hyd['mass'])
    if xkey=='logm':        mass = np.log10(1.-hyd['mass']/(Mtot+1e-8))
    elif xkey=='mass':      mass = hyd['mass']
    elif xkey=='zone':      mass = hyd['zone']
    
    keys = list(abn.keys())
    keys.remove('zone')
    
    plt.figure()
    for k in keys:
        if ylog: 
            plt.plot(mass,np.log10(abn[k]),label=k)
            plt.ylim(-4,0)
            plt.ylabel('log(Mass Fraction)')
        else:
            plt.plot(mass,abn[k],label=k)
            plt.ylim(0,1)
            plt.ylabel('Mass Fraction')
            
    
    if xkey=='logm':    
        plt.xlim(0,-5)
        plt.xlabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$')
    elif xkey=='mass':  
        plt.xlim(np.min(hyd['mass'])-0.1,np.max(hyd['mass'])+0.1)                  
        plt.xlabel(r'$M_{r}$')
    elif xkey=='zone':  
        plt.xlim(0,250)
        plt.xlabel('Mass zone',fontsize=12)
        
    plt.tight_layout()
    plt.grid(ls='--',c='grey',lw=0.4)
    plt.legend()