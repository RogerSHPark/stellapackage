#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:47:02 2022

@author: shpark
"""

def integral(t,t0,n,s,gn,q,betaf,A,ti,tFS,betar,tRS):
    import numpy as np
    
    cf = 2.*pi/(n-s)**3.*gn**((5.-s)/(n-s))*q**((n-5.)/(n-s))*(n-3.)**2.*(n-5.)*betaf**(5.-s)*A**((5.-s)/(n-s))*(t+ti)**((2.*n+6.*s-n*s-15.)/(n-s))*np.heaviside(tFS-t,0.5)
    cr = 2.*pi*(A*gn/q)**((5.-n)/(n-s))*(n-5.)/(n-3.)*betar**(5.-n)*gn*((3.-s)/(n-s))**3.*(t+ti)**((2.*n+6.*s-n*s-15.)/(n-s))*np.heaviside(tRS-t,0.5)
    c = np.exp(t/t0)*(cf+cr)
    return c

import numpy as np
import stellapkg as STL
import matplotlib.pyplot as plt
import scipy.integrate as integrate

#supernova properties
delta = 2.
n = 6.
x0 = 0.195
Mej = 4.08*STL.physcons.MSUN
Esn = 0.65*1e51

#constants
betaf = 1.377
betar = 0.958
A = 0.62
kappa = 0.1
beta = 13.8
pi = STL.physcons.PI
c = STL.physcons.C

#CSM properties
MCSM = 0.01*STL.physcons.MSUN
RCSM_in = 1.0*1e13
RCSM_out = 5.0*1e13
s=2
eff = 0.05

#calculated values
q = MCSM/(4.*pi*(RCSM_out - RCSM_in))
vsn = ((10.*(n-5.)*Esn)/(3.*(n-3.)*Mej))**0.5/x0
gn = (2.*(5.-delta)*(n-5.)*Esn)**((n-3.)/2.)/((3.-delta)*(n-3.)*Mej)**((n-5.)/2.)/(4.*pi*(n-delta))
ti = RCSM_in/vsn
tFS = (((3.-s)*MCSM)/(4.*pi*betaf**(3.-s)*q**((n-3.)/(n-s))*(A*gn)**((3.-s)/(n-s))))**((n-s)/((n-3.)*(3.-s)))
tRS = (betar/vsn*(A*gn/q)**(1./(n-s))*((n-3.)*vsn**(n-3.)*Mej/(4.*pi*gn)+1.)*(1./n-3.))**((n-s)/(3.-s))
t0 = 4.*pi*q*kappa/(beta*c)*(MCSM/(MCSM+4.*pi*q*RCSM_in)-2.*RCSM_in/(3.*kappa*q))

print('q={}'.format(q))
print('vsn={}km/s'.format(vsn/1e5))
print('gn={}'.format(gn))
print('ti={}d'.format(ti/86400.))
print('tFS={}d'.format(tFS/86400.))
print('tRS={}d'.format(tRS/86400.))
print('t0={}d'.format(t0/86400.))

tt = STL.TTparser.tt_data('CO5.7_13R1.9E-4M0.9FN0.12MN_s/E1.6_350d/CO5.7_13R1.9E-4M0.9FN0.12MN_s')

time = np.array(tt.data['time'])
Mbol = np.array(tt.data['Mbol'])
Lbol = 10.**((Mbol - 71.197425 - 17.5)/(-2.5) - 0.5)

Ltot = np.zeros(len(time),dtype=float)
lum = np.zeros(len(time),dtype=float)
for i in range(0,len(lum)):
    t = time[i]*86400.
    lum[i] = 1./t0*np.exp(-1.*t/t0)*integrate.quad(integral,0,t,args=(t0,n,s,gn,q,betaf,A,ti,tFS,betar,tRS))[0]
    Ltot[i] = Lbol[i]+lum[i]
    
plt.figure()
plt.plot(time,np.log10(Lbol),label='56Ni only')
plt.plot(time,np.log10(Ltot),label='56Ni + CSM')
plt.plot(time,np.log10(lum),ls='--',label='CSM')
plt.ylim(40.5,42.5)
plt.grid(ls='--',c='grey',lw=0.4)
plt.legend()
plt.xlabel('Days since SN',fontsize=14)
plt.ylabel('logL',fontsize=14)
plt.tight_layout()

