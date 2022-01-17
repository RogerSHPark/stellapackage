# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 11:01:36 2022

@author: USER
"""

import stellapkg as STL
import matplotlib.pyplot as plt
import numpy as np

root = 'C:/Users/USER/Desktop/'
STL.STLROOT.croot(root)

a = ['p200_Ni0_new','E1.0']

res = STL.parser.RESparser.res_data(a)
abn = STL.parser.ABNparser.abn_data(a)

times = res.data['obstime']

EKIN = np.zeros(len(times),dtype=float)
for i, t in enumerate(times):
    prof = res.get_profile(t)
    zone = np.where(abn.data['H']>0.01)[0]
    sum_ = 0
    for j in range(0,len(prof['EKIN'])):
        if prof['zone'][j] in zone:
            sum_ += prof['EKIN'][j]
    EKIN[i] = sum_
    
plt.figure()
plt.plot(times,np.log10(EKIN)+50.)