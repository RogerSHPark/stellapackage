# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:18:00 2022

@author: USER
"""

from stellapkg import STLROOT
from stellapkg.utils import physcons
from stellapkg.utils import STLkeys
from stellapkg.parser.ABNparser import abn_data
from stellapkg.parser.HYDparser import hyd_data

import numpy as np

class swd_data():
    '''
    loading .swd data
    '''
    def __init__(self,a):
        
        self._filename = STLROOT.get_filename(a)+'.swd'
        print('reading from '+self._filename)
        
        self._hyd = hyd_data(a)
        self._abn = abn_data(a)
        
        grid,data = self._get_data()
        self.grid = grid
        self.data = data
    
    def __del__(self):
        print('swd file closed')
        
    def _get_data(self):
        '''
        swd file provides internal profile at time epochs
        set by entry in .dat file
        '''
        fname = self._filename
        f = np.genfromtxt(fname,skip_header=0)
        h = self._hyd
        Mtot = max(h.data['mass'])
        self._Mtot = Mtot
        
        nlines = len(f[:,0])
        nzone = 249
        nblock = int(nlines/nzone)
        
        grid = {'time':[],'mass':[],'logm':[],'xm':[],'zone':[]}
        keys = [_[0] for _ in STLkeys.swdkeys]
        data = {_:[] for _ in keys}
        
        k=0
        
        grid['zone'] = f[0:nzone,1]
        
        logm = f[0:nzone,2]
        grid['xm'] = logm
        grid['logm'] = logm - np.log10(Mtot)
        grid['mass'] = Mtot - 10.**logm
        for i in range(0,nblock):
            grid['time'].append(f[k,0])
            for key_ in keys:
                j = [_[1] for _ in STLkeys.swdkeys if _[0]==key_][0]
                data[key_].append(f[k:k+nzone,j])
            k=k+nzone
            
        for key_ in keys:
            data[key_] = np.array(data[key_])
        data['logRho'] = data['logRho']-6.
        data['logP'] = data['logP']+7.
        data['L'] = data['L']*1e40

             
            # for j in [3,4,5,6,7,8,9,10,11,12]:
            #     if cols[j]=='logRho':
            #         data[cols[j]].append(f[k:k+nzone,j]-6.)
            #     elif cols[j]=='logP':
            #         data[cols[j]].append(f[k:k+nzone,j]+7.)
            #     elif cols[j]=='L':
            #         data[cols[j]].append(f[k:k+nzone,j]*1e40)
            #     else:
            #         data[cols[j]].append(f[k:k+nzone,j])
            # # rhobar = Mtot*physcons.MSUN/(4.*physcons.PI*10.**(3*np.max(data['logR'][i]))/3.)
            # data['logRhoNm'].append(data['logRho'][i]-np.log10(rhobar))
            
            # k = k + nzone
            
        return grid,data
    
    def get_profile(self,t1):
        
        time = self.grid['time']
        data = self.data
        Mtot = self._Mtot

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
            return []
        
        indx = np.argwhere(np.array(time)==t1)[0][0]
        keys = list(data.keys())
        datan = {k:data[k][indx] for k in keys}
        
        rhobar = Mtot*physcons.MSUN/(4.*physcons.PI*10.**(3*np.max(data['logR'][indx]))/3.)
        datan['logRhoNm'] = data['logRho'][indx] - np.log10(rhobar)
        
        return datan

        
    def get_phots(self):
        '''
        photospheric properties
        '''
        grid = self.grid
        data = self.data
        x = self._abn.data
        nzone = 249
        
        swdkeys = [_[0] for _ in STLkeys.swdkeys]
        swdkeys = [k+'ph' for k in swdkeys]
        datan = {k:[] for k in swdkeys}
        dict_ = {'time':[], 'tau':[], 'zoneph':[], 'massph':[], 'logmph':[]}
        datan.update(dict_)
        
        abnkeys = [_[0] for _ in STLkeys.abnkeys]
        Xph = {k:[] for k in abnkeys}
        
        tau = np.zeros((nzone),float)
        datan['time'] = data['time']
        for i, item in enumerate(data['time']):
            prof = self.get_profile(item)
            tau[nzone-1] = 0.0
            
            logR = data['logR'][i]
            logRho = data['logRho'][i]
            cappa = data['cappa'][i]
            for j in range(nzone-2,0,-1):
                tau[j] = tau[j+1] + cappa[j]*10.**logRho[j]*(10.**logR[j+1]-10.**logR[j])
            tau[0] = tau[1]
            for j in range(0,nzone-1):
                if tau[j]>=0.67 and tau[j+1]<0.67:
                    ntau = j
            datan['tau'].append(tau)
            datan['zoneph'].append(grid['zone'][ntau])
            datan['massph'].append(grid['mass'][ntau])
            datan['logmph'].append(grid['logm'][ntau])
            for k in swdkeys:
                datan[k].append(prof[k[:-2]][ntau])
            datan['logRhoNmph'].append(prof['logRhoNm'][ntau])
            
            for _ in abnkeys:
                Xph[_].append(x[_][ntau])

        datan['Xph'] = Xph
        
        return datan