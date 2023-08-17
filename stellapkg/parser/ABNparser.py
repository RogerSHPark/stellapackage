# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:13:47 2022

@author: USER
"""

from stellapkg import STLROOT
from stellapkg.utils import STLkeys
import numpy as np

class abn_data():
    '''
    Loading .abn file
    '''    
    def __init__(self,*a):
        
        self._filename = STLROOT.get_filename(*a)+'.abn'
        print('reading from '+self._filename)

        data = self._get_data()
        self.data = data
    
    def __del__(self):
        print('abn file closed')
        
    def _get_data(self):

        fname = self._filename
        keys = STLkeys.abnkeys
        
        f = np.genfromtxt(fname, skip_header=0)

        data = {}
        data['zone'] = np.array(f[:,0],dtype=int)
        for i in keys:
            data[i[0]] = np.array(f[:,i[1]])

        return data
