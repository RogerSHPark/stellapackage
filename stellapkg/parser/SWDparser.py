# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:18:00 2022

@author: USER
"""

from stellapkg import STLROOT
import numpy as np
from stellapkg.utils import physcons

class swd_profile():
    '''
    loading .swd data
    '''
    def __init__(self,a):
        
        self._filename = STLROOT.get_filename(a)+'.swd'
        print('reading from '+self._filename)   
        
        time,logm,data = self.get_data()
        self.time = time
        self.logm = logm
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
        # x = star.read_file(fname[:-4]+'.abn',0)
        h = np.genfromtxt(fname[:-4]+'.hyd', skip_header=1)
        Mtot = max(h[:,6])
        
        nlines = len(f[:,0])
        nzone = 249
        nblock = int(nlines/nzone)
        # print(nlines,nzone,nblock)
        
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
            
        return time,logm,data
    
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
        fname = self._filename
        data = self.data
        x = np.genfromtxt(fname[:-4]+'.abn', skip_header=0)
        nzone = 249
        
        cols = ['time','tau','zoneph','massph','logmph','logTph','logTradph','logRhoph',\
                'velph','cappaph','logRph','Lph','logPph','logRhoNmph']
        Xph = {'H':[],'He':[],'C':[],'N':[],'O':[],'Ne':[],'Mg':[],'Si':[],\
               'S':[],'Ar':[],'Ca':[],'Fe':[],'Ni':[]}
        
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
            Xph['H'].append(x[ntau,4])
            Xph['He'].append(x[ntau,5])
            Xph['C'].append(x[ntau,6])
            Xph['N'].append(x[ntau,7])
            Xph['O'].append(x[ntau,8])
            Xph['Ne'].append(x[ntau,9])
            Xph['Mg'].append(x[ntau,11])
            Xph['Si'].append(x[ntau,13])
            Xph['S'].append(x[ntau,14])
            Xph['Ar'].append(x[ntau,15])
            Xph['Ca'].append(x[ntau,16])
            Xph['Fe'].append(x[ntau,17])
            Xph['Ni'].append(x[ntau,19])
        datan['Xph'] = Xph
        
        return datan