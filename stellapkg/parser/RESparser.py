# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:12:54 2022

@author: USER
"""

from stellapkg import STLROOT
from stellapkg.utils import physcons
from stellapkg.utils import STLkeys
from stellapkg.parser.ABNparser import abn_data
from stellapkg.parser.HYDparser import hyd_data

import numpy as np

class res_data():
    '''
    loading .res file
    '''    
    def __init__(self,*a):
        
        self._filename = STLROOT.get_filename(*a)+'.res'
        print('reading from '+self._filename)
        
        self._hyd = hyd_data(*a)
        self._abn = abn_data(*a)
        
        Mtot,data = self._get_data()
        self.data = data
        self._Mtot = Mtot
        
    def __del__(self):
        print('res file closed')        
        
    def _get_data(self):
        '''
        Raw profile data with obstime, proper time, step number, timestep info
        '''
        
        fname = self._filename
        f = open(fname,'r')
        lines = f.read().splitlines()
        Mtot = float(lines[5][42:48])
        
        starts = []
        ends = []
        estarts = []
        eends = []
        contents = dict(obstime=[], protime=[], data=[], nstep=[], stept=[], edata=[])
        
        for i, line in enumerate(lines):
            if line.startswith('%H:'):
                starts.append(i)
            elif line.startswith('%B:'):
                ends.append(i)
            elif line.startswith(" EFFECTIVE TEMPERATURE"):
                estarts.append(i)
            elif line.startswith(" THERMAL  ENERGY"):
                eends.append(i)
                
        for i, idx in enumerate(starts):
            if (ends[i] - starts[i]) == 5:
                del starts[i], ends[i]
                
        for i, idx in enumerate(starts):
            obst = lines[idx+3].split(' D ')[0].split('= ')[-1].strip()
            propt = lines[idx+3].split(' S ')[0].split('T= ')[-1].strip()
            stepused = lines[idx+3].split('STEP TRIED')[0].split('STEP USED=')[-1].strip()
            nstp = lines[idx+2][:11]
            contents["obstime"].append(float(obst))
            contents["protime"].append(float(propt))
            contents['nstep'].append(int(nstp))
            contents["stept"].append(float(stepused))
            contents["data"].append(lines[idx+4:ends[i]])
            
        for i, idx in enumerate(estarts):
            elines = lines[idx:eends[i]+1]
            if elines not in contents['edata']:
                contents["edata"].append(lines[idx:eends[i]+1])
        
        ###### OBSOLETE PART ############
        # line = contents['data'][0][0]
        
        # reskeys = []
        # for i in range(0,len(colspecs)):
        #     x0 = colspecs[i][0]
        #     x1 = colspecs[i][1]
        #     reskeys.append(line[x0:x1].strip())
        
        # for i, item in enumerate(contents["data"]):
        #     np.savetxt("tmp.txt", item, fmt='%s')
        #     contents["data"][i] = pd.read_fwf("tmp.txt", colspecs=colspecs)
        ####################################
        
        for i, item in enumerate(contents['data']):
            data = self._get_data_into_array(item)
            contents['data'][i] = data
            
        contents['edata'] = self._get_edata_into_array(contents['edata'])

        return Mtot,contents
    
    def _get_data_into_array(self,item):
        
        reskeys = STLkeys.reskeys_raw
        colspecs = ((0, 4), (4, 13), (13, 25), (25, 33), (33, 43), (43, 51), (51, 58),
                    (58, 65), (65, 72), (72, 79), (79, 89), (89, 99), (99, 109),
                    (109, 119), (119, 124), (124, 134), (134, 144), (144, 154),
                    (154, 164), (164, 174))
        data = {k:[] for k in reskeys}
        for line in item[1:]:
            for j, key in enumerate(reskeys):
                x0, x1 = colspecs[j]
                dataentry = line[x0:x1].strip()
                if (dataentry[4:6]=='-1') and (dataentry[4:6]!='E-'):
                    dataentry = dataentry[:4]+'E'+dataentry[4:]
                data[key].append(dataentry)
        for key in reskeys:
            if key[:3]=='ZON':
                data[key] = np.array(data[key],dtype=int)
            else:
                data[key] = np.array(data[key],dtype=float)
        return data
    
    def _get_edata_into_array(self,contents):
        
        reskeys = STLkeys.reskeys_eng
        data = {k:[] for k in reskeys}
        
        for i, item in enumerate(contents):
            data['vol_gains_pow'].append(float(item[1][36:50])/10.)
            data['surfL'].append(float(item[2][36:50])/10.)
            data['tot_gains_pow'].append(float(item[3][36:50])/10.)
            data['radiat'].append(float(item[4][31:50])/10.)
            data['total'].append(float(item[4][87:102])/10.)
            data['kinetic'].append(float(item[5][31:50])/10.)
            data['gained'].append(float(item[5][87:102])/10.)
            data['gravit'].append(float(item[6][31:50])/10.)
            data['viscous virial'].append(float(item[6][87:102])/10.)
            data['virial'].append(float(item[7][31:50])/10.)
            data['virial balance'].append(float(item[7][87:102])/10.)
            data['thermal'].append(float(item[8][31:50])/10.)
            data['total balance'].append(float(item[8][87:102])/10.)
        
        return data
            
    #### OBSOLETE ROUTINE FOR GETTING EDATA ###########
    # def get_edata(self):
    #     '''
    #     Time serial of various energies
    #     '''
    #     fname = self._filename
    #     f = open(fname,'r')
    #     lines1 = f.read().splitlines()
    #     cols = ['obstime','protime','thermal','virial','kinetic','radiat','gravit','total','gained',\
    #             'surfL','vol_gains_pow','tot_gains_pow','viscous virial','virial balance',\
    #             'total balance']
        
    #     starts = []
    #     ends = []
        
    #     data = {k:[] for k in cols}

    #     for i, line in enumerate(lines1):
    #         if line.startswith('%H:'):
    #             starts.append(i)
    #         elif line.startswith('%B:'):
    #             ends.append(i)
                
    #     for i, idx in enumerate(starts):
    #         obst = lines1[idx+3].split(' S ')[0].split('T= ')[-1].strip()
    #         propt = lines1[idx+3].split(' S ')[0].split('T= ')[-1].strip()
    #         data['obstime'].append(float(obst))
    #         data['protime'].append(float(propt))
        
    #     for i, idx in enumerate(lines1):
    #         if idx.startswith('   OB.T(D)'):
    #             data['thermal'].append(float(lines1[i-2][31:46])/10.)
    #             data['virial'].append(float(lines1[i-3][31:46])/10.)
    #             data['gravit'].append(float(lines1[i-4][31:46])/10.)
    #             data['kinetic'].append(float(lines1[i-5][31:55])/10.)
    #             data['radiat'].append(float(lines1[i-6][31:46])/10.)
    #             data['total'].append(float(lines1[i-6][87:102])/10.)
    #             data['gained'].append(float(lines1[i-5][87:102])/10.)
    #             data['viscous virial'].append(float(lines1[i-4][87:102])/10.)
    #             data['virial balance'].append(float(lines1[i-3][87:102])/10.)
    #             data['total balance'].append(float(lines1[i-2][87:102])/10.)
    #             data['surfL'].append(float(lines1[i-8][36:50])/10.)
    #             data['vol_gains_pow'].append(float(lines1[i-9][36:50])/10.)
    #             data['tot_gains_pow'].append(float(lines1[i-7][36:50])/10.)

    #     return data
    ###########################
                
    
    def get_profile(self,t1,propert=False):
        '''
        profile data at time t1
        '''
        data = self.data
        Mtot = self._Mtot
        
        time = data['obstime']
        if propert: 
            time = np.array(data['protime'])

        if (t1 not in time):
            print(f'No data in {t1}')
            if t1<np.min(time):
                t2 = np.min(time[time>t1])
                print(f'Try: {t2}')
            elif t1>np.max(time):
                t2 = np.max(time[time<t1])
                print(f'Try: {t2}')
            else:
                t2 = np.max(time[time<t1])
                t3 = np.min(time[time>t1])
                print(f'Try: {t2} or {t3}')
            return []        
        
        res = self._get_data_by_obstime(data,t1,propert=propert)

        mass = []
        for i in np.array(res["AM/SOL"]):
            if i < 0.:
                mass.append(Mtot+i)
            elif i <1e-1:
                masscut = np.trunc(100.*float(res["AM/SOL"][0]))/100.
                mass.append(masscut+i)           
            else:
                mass.append(i)
                
        mass = np.array(mass)
        logm = np.log10(1.-mass/Mtot)
        
        keys = STLkeys.reskeys
        datan = {k:[] for k in keys}
        
        datan['mass'] = mass
        datan['logm'] = logm
        datan['xm'] = res["AM/SOL"]
        datan['zone'] = res['ZON']
        datan['vel'] = res['V 8.']*10**8
        datan['rad'] = res['R14.']*10**14
        datan['rho'] = 10.**(res['lgD-6.']-6.)
        datan['press'] = 10.**(res['lgP 7.']+7.)
        datan['cappa'] = res['CAPPA']
        datan['n_bar'] = res['n_bar']
        datan['n_e'] = res['n_e']
        datan['lum'] = res['LUM']
        datan['XHI'] = res['XHI']
        
        temp = res['T 5.']*10.**5
        trad = res['Trad5']*10**5
        for i, item in enumerate(temp):
            if item==0:
                temp[i] = 10.
        
        for i, item in enumerate(trad):
            if item==0:
                trad[i] = 10.
        
        datan['temp'] = temp
        datan['trad'] = trad
        
        rhobar = Mtot*physcons.MSUN/(4.*physcons.PI*np.max(datan['rad'])**3./3.)
        datan['rhoNm'] = datan['rho']/rhobar
        datan['nenb'] = datan['n_e']/datan['n_bar']
        
        dMr = self._hyd.data['dm']*physcons.MSUN       
        vol = dMr[datan['zone']-1]/datan['rho']/1e51
        ERAD = 4.*physcons.SIG/physcons.C*datan['trad']**4.*vol
        ETHM = 1.5*(datan['n_bar']+datan['n_e'])*physcons.KB*datan['temp']*vol
        EKIN = 0.5*datan['vel']**2.*vol*datan['rho']
        EGRA = -1*physcons.G*np.array(datan['mass'])*vol*datan['rho']/datan['rad']
        datan['ERAD'] = ERAD; datan['ETHM'] = ETHM; datan['EKIN'] = EKIN; datan['EGRA'] = EGRA
        
        return datan

    def _get_data_by_obstime(self,contents, obstime,propert=False):
        '''private routine used in get_profile'''
        idx = np.argwhere(np.array(contents["obstime"]) == float(obstime))
        if propert: 
            idx = np.argwhere(np.array(contents["protime"]) == float(obstime))
        results = []
        for i in idx:
            results.append(contents["data"][i[0]])
        return results[0]    

        
    def get_phots(self,thm=False,propert=False):
        '''
        Compute photosperic properties from profile
        if thm=True, thermalization depth properties also included
        '''
        fname = self._filename
        data = self.data
        x = self._abn.data
        time = data['obstime']
        if propert: time = data['protime']

        reskeys = STLkeys.reskeys
        reskeys = [k+'ph' for k in reskeys]
        datan = {k:[] for k in reskeys}
        dict_ = {'tau':[], 'rhoNmph':[], 'nenbph':[]}
        datan.update(dict_)
        
        abnkeys = [_[0] for _ in STLkeys.abnkeys]
        Xph = {k:[] for k in abnkeys}

        datan['time'] = time

        if thm:
            keys2 = ['tau_thm','Mthm','lgMthm','Rthm','Tthm','Rhothm','Vthm','Kthm']
            dict2 = {k:[] for k in keys2}
            datan.update(dict2)
        
        for i, item in enumerate(time):
            prof = self.get_profile(item,propert=propert)
            zon = prof['zone']
            rho = prof['rho']
            rad = prof['rad']
            cappa = prof['cappa']
            tau = np.zeros((len(zon)),float)
            tau[-1] = 0.0
            for j in range(len(zon)-2,0,-1):
                tau[j] = tau[j+1] + cappa[j]*rho[j]*(rad[j+1]-rad[j])
            tau[0] = tau[1]
            for j in range(0,len(zon)-1):
                if tau[j]>=0.67 and tau[j+1]<0.67:
                    ntau = j
            zontau = zon[ntau]
            datan['tau'].append(tau)
            for k in list(datan.keys()):
                if k.endswith('ph'):
                    datan[k].append(prof[k[:-2]][ntau])
            for _ in abnkeys:
                Xph[_].append(x[_][zontau])
            
            if thm:
                thom_sc = 0.665e-24
                n_e = prof['n_e']
                cappa_sc = thom_sc*n_e/rho
                tau_th = np.zeros((len(zon)),float)
                tau_th[-1] = 0.
                for j in range(len(zon)-2,0,-1):
                    cpabs = cappa[j] - cappa_sc[j]
                    if cpabs < 0 : cpabs = 0.
                    tau_th[j] = tau_th[j+1] + (cpabs*cappa[j])**0.5*rho[j]*(rad[j+1]-rad[j])
                for j in range(0,len(zon)-1):
                    if tau_th[j] >= 0.67 and tau_th[j+1]<0.67:
                        ntau_th = j
                datan['tau_thm'].append(tau_th)
                datan['Mthm'].append(prof['mass'][ntau_th])
                datan['lgMthm'].append(prof['logm'][ntau_th])
                datan['Rthm'].append(rad[ntau_th])
                datan['Tthm'].append(prof['temp'][ntau_th])
                datan['Rhothm'].append(rho[ntau_th])
                datan['Vthm'].append(prof['vel'][ntau_th])
                datan['Kthm'].append(cappa[ntau_th])

        datan['Xph'] = Xph
        return datan
           
   
