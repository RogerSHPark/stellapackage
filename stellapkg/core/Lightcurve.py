#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:30:19 2022

@author: shpark
"""

from stellapkg.parser.TTparser import tt_data
from stellapkg.parser.PHparser import ph_data

import matplotlib.pyplot as plt
import numpy as np

def LCplot(*a,filters=['bol','U','B','V','R','I'],colors=['k','c','b','g','r','m'],ls='-',\
             xlim=True,x1=-0.5,x2=20,ylim=True,y1=-12,y2=-20,label=True,xlabel='Time [day]',\
             ylabel='Absolute magnitudes',oplot=False,grid=True,tight=True,legend=True):

    ttfilt = ['bol','U','B','V','R','I']
    phfilt = ['ZTFg','ZTFr','u','g','r','i','z']

    for i, filt in enumerate(filters):
        if (filt not in ttfilt) and (filt not in phfilt):
            print(filt+" filter not available")
            print("Available filters: ", end=' ')
            print(*ttfilt, sep=', ', end=', ')
            print(*phfilt, sep=', ')
            return
        
    if len(colors)!=len(filters):
        print("Number of colors must match number of filters\n")
        print(f"Current: {len(colors)} colors, {len(filters)} filters")
        return

    if any(i in filters for i in ttfilt):
        ttm = tt_data(*a)
    if any(i in filters for i in phfilt):
        phm = ph_data(*a).get_photm()

    if not oplot: plt.figure()
  
    for i, filt in enumerate(filters):
        if filt in ttfilt:
            time = ttm.data['time']
            mag = ttm.data['M'+filt]
        if filt in phfilt:
            time = phm['time']
            mag = phm[filt]
        c = colors[i]
        plt.plot(time,mag,color=c,ls=ls,label=filt)
    if not oplot:
        if xlim: plt.xlim(x1,x2)
        if ylim: plt.ylim(y1,y2)
        if label:
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
        if grid: plt.grid(ls='--',color='grey',lw=0.5)
    if legend: plt.legend()
    if tight: plt.tight_layout()