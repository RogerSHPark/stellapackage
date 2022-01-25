'''
Producing basic figures on initial structure information of the model
(chemical composition, density, temperature, velocity) 

'''

from stellapkg.parser.ABNparser import abn_data
from stellapkg.parser.HYDparser import hyd_data

import numpy as np
import matplotlib.pyplot as plt

def abnplot(*a,elems=['H','He','C','O','Fe','Ni'],labels=[],xkey='mass',ylog=True,oplot=False):
    '''
    Plotting chemical structure of the model
    
    elems : elements to include in the figure
            one or multiple from (H, He, C, N, O, Ne, Mg, Si, S, Ar, Ca, Fe, Ni)
            by default, (H, He, C, O, Fe, Ni) will be included
    labels : if not given, use elements' names
             if given, make sure to match the number of elements
    '''
    abn = abn_data(*a).data
    hyd = hyd_data(*a).data
    
    Mtot = np.max(hyd['mass'])
    if xkey=='logm':        xdat = np.log10(1.-hyd['mass']/(Mtot+1e-8))
    elif xkey=='mass':      xdat = hyd['mass']
    elif xkey=='zone':      xdat = hyd['zone']
    
    if len(elems)==0:
        keys = list(abn.keys())
        keys.remove('zone')
    else:
        keys = elems
        
    if len(labels)==0:
        labels = keys
    
    if not oplot: plt.figure()
    for i, k in enumerate(keys):
        label = labels[i]
        if ylog: 
            plt.plot(xdat,np.log10(abn[k]),label=label)
            plt.ylim(-4,0)
            plt.ylabel('logX')
        else:
            plt.plot(xdat,abn[k],label=label)
            plt.ylim(0,1)
            plt.ylabel('X')
            
    
    if xkey=='logm':    
        plt.xlim(0,-5)
        plt.xlabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$')
    elif xkey=='mass':  
        plt.xlim(np.min(hyd['mass'])-0.1,np.max(hyd['mass'])+0.1)                  
        plt.xlabel(r'$M_{r}$')
    elif xkey=='zone':  
        plt.xlim(0,250)
        plt.xlabel('Mass zone')
        
    if not oplot:
        plt.grid(ls='--',c='grey',lw=0.4)
    plt.legend()
    plt.tight_layout()
    

    
def hydplot(*a,xkey='logm',ykey='rho',label='',ylog=True,oplot=False):
    
    hyd = hyd_data(*a).data
    
    Mtot = np.max(hyd['mass'])
    
    if xkey=='logm':        
        xdat = np.log10(1.-hyd['mass']/(Mtot+1e-8))
    elif xkey=='mass':      
        xdat = hyd['mass']
    elif xkey=='zone':      
        xdat = hyd['zone']
    elif xkey=='rad':       
        xdat = hyd['rad']
    elif xkey=='logR':
        xdat = np.log10(hyd['rad'])

    
    if not oplot: plt.figure()
    if ylog:
        plt.plot(xdat,np.log10(hyd[ykey]),label=label)
    else:
        plt.plot(xdat,hyd[ykey],label=label)

        
    if ykey=='rho':
        plt.ylabel(r'$\rho$')
        if ylog:    plt.ylabel(r'$\log{\rho}$')
    elif ykey=='dm':
        plt.ylabel('dm')
        if ylog:    plt.ylabel(r'$\log{(dm)}$')
    elif ykey=='temp':
        plt.ylabel('T')
        if ylog:    plt.ylabel(r'$\log{T}$')
    elif ykey=='vel':
        plt.ylabel('V')
        if ylog:    plt.ylabel(r'$\log{V}$')


    if xkey=='logm':        
        plt.xlabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$')
        plt.xlim(0,-5)
    elif xkey=='mass':      
        plt.xlabel(r'$M_{r}$')
        plt.xlim(np.min(xdat),np.max(xdat))
    elif xkey=='zone':      
        plt.xlabel('Mass zone')
        plt.xlim(0,250)
    elif xkey=='rad':       
        plt.xlabel('R')
    elif xkey=='logR':
        plt.xlabel('logR')


    if not oplot:   plt.grid(ls='--',c='grey',lw=0.4)
    if label != '': plt.legend()
    plt.tight_layout()