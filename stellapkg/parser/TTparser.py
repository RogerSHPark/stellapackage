# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 14:43:10 2022

@author: USER
"""

from stellapkg import STLROOT

class tt_data():
    '''
    Loading .tt file
    '''    
    def __init__(self,a):
        
        self._filename = STLROOT.get_filename(a)+'.tt'
        print('reading from '+self._filename)
        
        data = self._get_data()
        self.data = data

    
    def __del__(self):
        print('tt file closed')
        
    def _get_data(self):
        '''
        bol,U,B,V,R,I : magnitudes
        Tbb, Rbb : blackbody-fitted temperatures of the spectra and corresponding radii
        Teff : effective temperature
        Rlast_sc, R(tau2/3) : photospheric radii
        gdepos : energy deposited by gamma ray
        '''
        
        fname = self._filename
        f = open(fname,'r')
        content = f.readlines()
        cols = content[84].split()
        
        data = {k:[] for k in cols}

        for i in range(85,len(content)):
            for j in range(0,len(cols)):
                data[cols[j]].append(float(content[i].split()[j]))

        return data