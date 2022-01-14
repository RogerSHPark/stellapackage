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

class swd_profile():
    '''
    loading .swd data
    '''
    def __init__(self,a):
        
        self._filename = STLROOT.get_filename(a)+'.swd'
        print('reading from '+self._filename)
        
        self._hyd = hyd_data(a)
        self._abn = abn_data(a)
        
        time,data = self.get_data()
        self.time = time
        self.data = data
    
    def __del__(self):
        print('swd file closed')
        
    def get_data(self):
        '''
        swd file provides internal profile at time epochs
        set by entry in .dat file
        '''
        fname = self._filename
        f = np.genfromtxt(fname,skip_header=0)
        h = self._hyd
        Mtot = max(h.data['mass'])
        
        nlines = len(f[:,0])
        nzone = 249
        nblock = int(nlines/nzone)
        
        cols = ['time','zone','xm','logR','vel','logT','logTrad','logRho','logP',\
                'logqv','eng12','L','cappa','logm','mass']
        data = {k:[] for k in cols}
        time = []
        
        k=0
        
        data['zone'] = f[0:nzone,1]
        
        logm = f[0:nzone,2]
        data['xm'] = logm
        data['logm'] = logm - np.log10(Mtot)
        data['mass'] = Mtot - 10.**logm
        data['logRhoNm'] = []
        for i in range(0,nblock):
            time.append(f[k,0])
            data['time'].append(f[k,0])
            for j in [3,4,5,6,7,8,9,10,11,12]:
                if cols[j]=='logRho':
                    data[cols[j]].append(f[k:k+nzone,j]-6.)
                elif cols[j]=='logP':
                    data[cols[j]].append(f[k:k+nzone,j]+7.)
                elif cols[j]=='L':
                    data[cols[j]].append(f[k:k+nzone,j]*1e40)
                else:
                    data[cols[j]].append(f[k:k+nzone,j])
            rhobar = Mtot*physcons.MSUN/(4.*physcons.PI*10.**(3*np.max(data['logR'][i]))/3.)
            data['logRhoNm'].append(data['logRho'][i]-np.log10(rhobar))
            
            k = k + nzone
            
        return time,data
    
    def snapshot(self,t1):
        
        time = self.time
        data = self.data

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
        excl = ['time','zone','xm','logm','mass']
        keys = [k for k in keys if k not in excl]
        datan = {k:data[k][indx] for k in keys}
        
        return datan
        
    def get_phots(self):
        '''
        photospheric properties
        '''
        data = self.data
        x = self._abn.data
        nzone = 249
        
        cols = ['time','tau','zoneph','massph','logmph','logTph','logTradph','logRhoph',\
                'velph','cappaph','logRph','Lph','logPph','logRhoNmph']
            
        abnkeys = [_[0] for _ in STLkeys.abnkeys]
        Xph = {k:[] for k in abnkeys}
        
        datan = {k:[] for k in cols}
        tau = np.zeros((nzone),float)
        for i, item in enumerate(data['time']):
            tau[nzone-1] = 0.0
            datan['time'].append(item)
            
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
            datan['zoneph'].append(data['zone'][ntau])
            datan['massph'].append(data['mass'][ntau])
            datan['logmph'].append(data['logm'][ntau])
            datan['logTph'].append(data['logT'][i][ntau])
            datan['logTradph'].append(data['logTrad'][i][ntau])
            datan['logRhoph'].append(data['logRho'][i][ntau])
            datan['velph'].append(data['vel'][i][ntau])
            datan['cappaph'].append(data['cappa'][i][ntau])
            datan['logRph'].append(data['logR'][i][ntau])
            datan['Lph'].append(data['L'][i][ntau])
            datan['logPph'].append(data['logP'][i][ntau])
            datan['logRhoNmph'].append(data['logRhoNm'][i][ntau])
            
            
            for _ in abnkeys:
                Xph[_].append(x[_][ntau])

        datan['Xph'] = Xph
        
        return datan