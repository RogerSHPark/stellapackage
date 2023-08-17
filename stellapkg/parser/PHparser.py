# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 14:52:42 2022

@author: USER
"""

from stellapkg import STLROOT
import numpy as np
from stellapkg.utils import physcons

class ph_data():
    '''
    Loading .ph file : spectra data
    '''
    def __init__(self,*a):
        
        self._filename = STLROOT.get_filename(*a)+'.ph'
        print('reading from '+self._filename)
        
        data = self._get_data()
        self.data = data
    
    def __del__(self):
        print('ph file closed')
    
    def _get_data(self):
        '''
        spectral flux density data
        '''
        fname = self._filename
        f = open(fname,'r')
        
        content = f.readlines()
        freq = content[0].split()
        freq = np.array([10**float(i) for i in freq]) # frequency unit: Hz / sort: low->high
        
        wave = physcons.C/freq   # wavelength unit: cm / sort: long->short
        
        data = {'time':[], 'wv':[], 'freq':[], 'logLnu':[], 'Fnu':[], 'Fwv':[]}
        
        for i, line in enumerate(content[1:]):
            col = line.split()
            data['time'].append(float(col[0])) # time unit: day
            
            logLnu = np.array(col[3:],dtype=float)
            # Lnu unit: erg/s/Hz / sort: low nu->high nu
            data['logLnu'].append(np.flip(logLnu)) # Lnu sort: high nu->low nu
            
            Fnu_tmp = np.array([10**float(j)/(4*physcons.PI*(10*physcons.PC)**2) for j in logLnu]) 
            # Fnu unit: erg/s/cm^2/Hz / sort: low nu->high nu
            data['Fnu'].append(np.flip(Fnu_tmp)) # Fnu sort: high nu-> low nu
        
        wave = np.flip(wave) # wavelength sort: short->long
        Fnu = np.array(data['Fnu'])
        data['Fnu'] = Fnu
        
        Fwv = physcons.C/wave**2.*Fnu*1e-8 # Fwv unit: erg/s/cm^2/Aa / sort: short wv->long wv
        data['Fwv'] = Fwv
        
        wv = wave*1e8 # wavelength unit: Aa
        data['wv'] = wv
        data['freq'] = np.flip(freq) # frequency sort: high->nu
        
        return data
    
    
    def get_photm(self,filters=['ZTFg','ZTFr','ATLASc','ATLASo','u','g','r','i','z'],w1=2000,w2=13000):
        '''
        photometry other than UBVRI filters from intergrating spectrum directly
        ugriz filters from SDSS
        '''
        import speclite.filters
        
        wv = self.data['wv']
        Fwv = self.data['Fwv']
        time = self.data['time']
        
        ### input w1 and w2 specify the region within the filter is included
        ### but unnecesaary 
        # ind1 = np.max(np.where(wv<w1)[0])
        # ind2 = np.min(np.where(wv>w2)[0])+1
        # wv = wv[ind1:ind2]
        # Fwv = Fwv[:,ind1:ind2]

        photm = {k:[] for k in filters}
        filt = []
        
        for i, f in enumerate(filters):
            if f[:3] == 'ZTF':
                filt.append(f'ZTF-{f[3]}')
            elif f[:5] == 'ATLAS':
                filt.append(f'ATLAS-{f[5]}')
            else:
                filt.append(f'sdss2010-{f}')
                
        bands = speclite.filters.load_filters(*filt)
        mags = bands.get_ab_magnitudes(Fwv,wv)
        for i,f in enumerate(filt):
            photm[filters[i]] = np.array(mags[f])
            
        photm['time'] = np.array(time)
        
        return photm
    
    def get_profile(self,t1):
        '''
        Fnu and Fwv data of time t1
        '''
        time = self.data['time']
        time = np.array(time)
        Fnu = self.data['Fnu']
        Fwv = self.data['Fwv']
        
        if (t1 not in time):
            print(f'No data in {t1}d')
            if t1<np.min(time):
                t2 = np.min(time[time>t1])
                print(f'Try: {t2}d')
            elif t1>np.max(time):
                t2 = np.max(time[time<t1])
                print(f'Try: {t2}d')
            else:
                t2 = np.max(time[time<t1])
                t3 = np.min(time[time>t1])
                print(f'Try: {t2}d or {t3}d')
            return [], []
        
        Fnu = Fnu[time==t1][0]
        Fwv = Fwv[time==t1][0]              
        return Fnu, Fwv
