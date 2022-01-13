# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:46:25 2022

@author: USER
"""

from stellapkg import STLROOT
from stellapkg.utils import STLkeys
import numpy as np

class hyd_data():
    '''
    Loading .hyd file
    '''    
    def __init__(self,a):
        
        self._filename = STLROOT.get_filename(a)+'.hyd'
        print('reading from '+self._filename)
        
        header = self._get_header()
        data = self._get_data()
        self.header = header
        self.data = data
    
    def __del__(self):
        print('hyd file closed')
        
    def _get_header(self):
        
        fname = self._filename
        f = open(fname,'r')
        
        line = f.readline().split()
        line = np.array(line,dtype=float)
        header = {'nzone':int(line[1]), 'Mcut':line[2], 'Rcut':line[3], 'Rhocut':line[4]}
        return header
        
    def _get_data(self):

        fname = self._filename
        keys = STLkeys.hydkeys
        
        f = np.genfromtxt(fname, skip_header=1)
        
        data = {}
        data['zone'] = np.array(f[:,0],dtype=int)
        for i in keys:
            data[i[0]] = np.array(f[:,i[1]])

        return data