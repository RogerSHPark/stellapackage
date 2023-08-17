#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:50:09 2022

@author: shpark
"""

from stellapkg.parser.RESparser import res_data
from stellapkg.parser.SWDparser import swd_data

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.patheffects as mpe

def IPplot(*a,key,t1=0,t2=50,tarr=-1,xkey='logm',phots=True,propert=False,oplot=False,grid=True,tight=True,legend=True):
    
    reskeys = ['mass','logm','xm','zone','temp','trad','vel','rad','rho','press',\
            'cappa','n_bar','n_e','lum','XHI','rhoNm','nenb','kskt','ERAD']
    swdkeys = ['zone','xm','logR','swdvel','logT','logTrad','logRho','logP',\
            'logqv','eng12','L','swdcappa','logm','mass','logRhoNm']
    
    phots = phots and (not propert)
        
    if not oplot:
        plt.figure()
        
    if propert: 
        tunit = 'sec'
    else: 
        tunit = 'day'
        
    if key in reskeys:
        # dtype = 'res'
        print("Selected key in .res file")
        f = res_data(*a)
        if phots: 
            pts = f.get_phots()
        if propert:
            time = np.array(f.data['protime'])
        else:
            time = np.array(f.data['obstime'])
        if type(tarr) == int:
            time2 = time[np.where((time>=t1) & (time<=t2))[0]]
        else:
            time2 = tarr
        for i, t in enumerate(time2):
            prof = f.get_profile(t,propert=propert)
            mass = np.array(prof[xkey])
            var = np.array(prof[key])

            if key=='lum':
                plt.plot(mass,np.log10(var),color=cm.gist_rainbow(i/len(time2)),label='{0:.2e} '.format(t)+tunit,\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])                    
                plt.plot(mass,np.log10(-1.*var),ls='--',color=cm.gist_rainbow(i/len(time2)),\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])
            else:
                plt.plot(mass,np.log10(var),color=cm.gist_rainbow(i/len(time2)),label='{0:.2e} '.format(t)+tunit,\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])
            if phots:
                idx = np.argwhere(time==t)[0][0]
                mph = pts[xkey+'ph'][idx]
                varph = pts[key+'ph'][idx]   
                if key=='lum':
                    plt.plot(mph,np.log10(varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                    plt.plot(mph,np.log10(-1.*varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                else:
                    plt.plot(mph,np.log10(varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                    
    elif (key in swdkeys or key[:3]=='swd'):
        # dtype = 'swd'
        print("Selected key in .swd file")
        f = swd_data(*a)
        if phots: 
            pts = f.get_phots()
        time = np.array(f.grid['time'])
        if type(tarr) == int:
            time2 = time[np.where((time>=t1) & (time<=t2))[0]]
        else:
            time2 = tarr
        if key=='swdv': 
            key='vel'
        elif key=='swdk':
            key='cappa'
                
        for i, t in enumerate(time2):
            mass = f.grid[xkey]
            var = f.get_profile(t)[key]
            if key in ['vel','cappa']:
                plt.plot(mass,np.log10(var),color=cm.gist_rainbow(i/len(time2)),label='{0:.2e} day'.format(t),\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])
            elif key=='L':
                plt.plot(mass,np.log10(var),color=cm.gist_rainbow(i/len(time2)),label='{0:.2e} day'.format(t),\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])                    
                plt.plot(mass,np.log10(-1.*var),ls='--',color=cm.gist_rainbow(i/len(time2)),\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])
            else:    
                plt.plot(mass,var,color=cm.gist_rainbow(i/len(time2)),label='{0:.2e} day'.format(t),\
                     path_effects=[mpe.withStroke(linewidth=3,foreground='black')])
            if phots:
                idx = np.argwhere(time==t)[0][0]
                mph = pts[xkey+'ph'][idx]
                varph = pts[key+'ph'][idx]
                if key in ['vel','cappa']:
                    plt.plot(mph,np.log10(varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                elif key=='L':
                    plt.plot(mph,np.log10(varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                    plt.plot(mph,np.log10(-1.*varph),'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))
                else:
                    plt.plot(mph,varph,'*',markersize=10,markeredgecolor='black',color=cm.gist_rainbow(i/len(time2)))

    else:
        print(f'No key named {key} found')
        print('Available keys \n .res file: ',end='')
        print(*reskeys,sep=', ')
        print('.swd file: ',end='')
        print(*swdkeys,sep=', ')
        return
    
    if xkey not in ['logm','mass','zone']:
        print('Choose xkey from following: logm, mass, zone')
        print('mass: simple Mr; logm: log(1-Mr/Mtot); zone: mass shell number')
        return

    if not oplot:
        if xkey=='logm':
            plt.xticks(np.linspace(-5,0,11)); plt.xlim(0,-5) 
            plt.xlabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$',fontsize=15)
        elif xkey=='mass':
            plt.xticks(np.linspace(1.4,3.6,12)); plt.xlim(1.4,3.6)
            plt.xlabel(r'$M_{r}$',fontsize=15)
        elif xkey=='zone':
            plt.xticks(np.linspace(0,250,11)); plt.xlim(-5,255)
            plt.xlabel('Mass zone',fontsize=15)
            
        if key=='logR' or key=='rad': 
            plt.ylabel('logR',fontsize=15)
        elif key=='logT' or key=='temp': 
            plt.ylabel('logT',fontsize=15)
        elif key=='logTrad' or key=='trad': 
            plt.ylabel(r'$\log{T_\mathrm{rad}}$',fontsize=15)
        elif key=='vel': 
            plt.ylabel('logv',fontsize=15)
            plt.ylim(7.0,9.5)
        elif key=='logRhoNm' or key=='rhoNm':
            plt.ylabel(r'$\log{(\rho/\bar{\rho})}$',fontsize=15)
        elif key=='logRho' or key=='rho':
            plt.ylabel(r'$\log{\rho}$',fontsize=15)
        elif key=='logP' or key=='press':
            plt.ylabel('logP',fontsize=15)
        elif key=='cappa':
            plt.ylabel(r'$\log{\kappa}$',fontsize=15)
        elif key=='L' or key=='lum':
            plt.ylabel('logL',fontsize=15)
        elif key=='nenb':
            plt.ylabel(r'$\log{(n_\mathrm{e}/n_\mathrm{b})}$',fontsize=15)
        elif key in swdkeys:
            plt.ylabel(key,fontsize=15)
        else:
            plt.ylabel('$\log($'+key+'$)$',fontsize=15)
            
        if grid: plt.grid(ls='--',color='grey',lw=0.15)
    if legend: plt.legend(prop={'size':12})
    if tight: plt.tight_layout()
    

def KPHplot(*a,key,levels=[],xkey='logm',keylog=True,propert=False,logt=False,t1=0.,t2=15.,phots=False,rec=False,grid=True,tight=True,toffset=0.):
        
    reskeys = ['mass','logm','xm','zone','temp','trad','vel','rad','rho','press',\
            'cappa','n_bar','n_e','lum','XHI','rhoNm','nenb','kskt','ERAD']
        
    if key not in reskeys:
        print('Input must be one of these keys: ',end='')
        print(*reskeys,sep=', ')
        return
    
    if xkey not in ['logm','mass','zone']:
        print('Choose xkey from following: logm, mass, zone')
        print('mass: simple Mr; logm: log(1-Mr/Mtot); zone: mass shell number')
        return        
    
    f = res_data(*a)
    
    phots = phots and (not propert)
    
    if phots or rec:
        pts = f.get_phots(rec=rec)
    
    times = f.data['obstime']
    if propert: times = f.data['protime']
    
    tgrid = np.array(times)
    mgrid = f.get_profile(times[-1],propert=propert)[xkey]
    z = []
    
    if key=='lum':
        for t in times:
            prof = f.get_profile(t,propert=propert)
            var = np.array(prof[key])
            marr = np.array(prof[xkey])
            if marr[-1]<marr[0]:
                var = np.flip([var])[0]
                marr = np.flip([marr])[0]
            var = np.interp(mgrid,marr,var)
            z.append(var)
        z = np.array(z)
        if len(levels)==0:
            zn = z[np.where(tgrid>=t1) & (tgrid<=t2)[0]]
            zn1 = zn[np.where(zn>0)[0]]
            zn2 = np.abs(zn[np.where(zn<0)[0]])
            vmin = min(np.min(zn1),np.min(zn2))
            vmax = max(np.max(zn1),np.max(zn1))
            levels = np.linspace(np.log10(vmin),np.log10(vmax),21)
        z1 = np.log10(z)
        z2 = np.log10(-1.*z)
        z1 = np.transpose(z1)
        z2 = np.transpose(z2)
        
        fig, ax1 = plt.subplots()        
        ct1 = ax1.contour(tgrid-toffset,mgrid,z1,levels=levels,linewidths=0.3,colors='k')
        ct2 = ax1.contour(tgrid-toffset,mgrid,z2,levels=levels,linewidths=0.3,colors='k')
        ctf1 = ax1.contourf(tgrid-toffset,mgrid,z1,levels=levels,cmap=cm.Blues)
        ctf2 = ax1.contourf(tgrid-toffset,mgrid,z2,levels=levels,cmap=cm.Reds)
        cbar1 = fig.colorbar(ctf1)
        cbar1.ax.tick_params(labelsize=12)
        cbar2 = fig.colorbar(ctf2)
        cbar2.ax.tick_params(labelsize=12)
    else:
        for t in times:
            prof = f.get_profile(t,propert=propert)
            var = np.array(prof[key])
            logvar = np.log10(var)
            marr = np.array(prof[xkey])
            if marr[-1]<marr[0]:
                logvar = np.flip([logvar])[0]
                var = np.flip([var])[0]
                marr = np.flip([marr])[0]
            if keylog: 
                logvar = np.interp(mgrid,marr,logvar)
                z.append(logvar)
            else:
                var = np.interp(mgrid,marr,var)
                z.append(var)
        
        z = np.array(z)
        
        if len(levels)==0:
            zn = z[np.where((tgrid>=t1) & (tgrid<=t2))[0]]
            levels = np.linspace(np.min(zn),np.max(zn),21)

        z = np.transpose(z)

        fig, ax1 = plt.subplots()        
        ct = ax1.contour(tgrid-toffset,mgrid,z,levels=levels,linewidths=0.3,colors='k')
        ctf = ax1.contourf(tgrid-toffset,mgrid,z,levels=levels,cmap=cm.cool)
        cbar = fig.colorbar(ctf)
        cbar.ax.tick_params(labelsize=12)

    if phots:
        tph = np.array(pts['time'])
        mph = np.array(pts[xkey+'ph'])
        ax1.plot(tph-toffset,mph,marker='o',markersize=4,c='g',label=r'$\tau=2/3$')
             
    if rec:
        trec = np.array(pts['time'])
        mrec = np.array(pts[xkey+'rec'])
        ax1.plot(trec-toffset,mrec,marker='^',markersize=4,c='yellow',label=r'$X_{\mathrm{H I}}/X_{\mathrm{H}}=0.1$')
        
    
    ax1.set_xlim(t1,t2)
    if logt:
        ax1.set_xscale('log')
        if propert:
            ax1.set_xlim(max(1,t1),t2)
        else:
            ax1.set_xlim(max(0.001,t1),t2)
    ax1.set_xlabel('Time [day]',fontsize=15)
    if propert: ax1.set_xlabel('Time [sec]',fontsize=15)
    
    if xkey=='logm':
        ax1.set_yticks(np.linspace(0,-5,11))
        ax1.set_ylim(np.max(mgrid),np.min(mgrid))
        ax1.set_ylabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$',fontsize=15)
    elif xkey=='mass':
        # ax1.set_ylim(np.floor(10.*np.min(y))/10.,np.ceil(10.*np.max(y))/10.)
        ax1.set_ylim(np.min(mgrid),np.max(mgrid))
        ax1.set_ylabel(r'$M_{r}$',fontsize=15)
    else:
        ax1.set_ylim(0,250)
        ax1.set_yticks(np.linspace(0,250,11))
        ax1.set_ylabel('Mass zone',fontsize=15)
    
    if grid: ax1.grid(ls='--',c='white',lw=0.3)
    
    if key=='rad': 
        cbar.ax.set_ylabel('logR',fontsize=15)
    elif key=='temp': 
        cbar.ax.set_ylabel('logT',fontsize=15)
    elif key=='trad': 
        cbar.ax.set_ylabel(r'$\log{T_\mathrm{rad}}$',fontsize=15)
    elif key=='vel': 
        cbar.ax.set_ylabel('logv',fontsize=15)
    elif key=='rhoNm':
        cbar.ax.set_ylabel(r'$\log{(\rho/\bar{\rho})}$',fontsize=15)
    elif key=='rho':
        cbar.ax.set_ylabel(r'$\log{\rho}$',fontsize=15)
    elif key=='press':
        cbar.ax.set_ylabel('logP',fontsize=15)
    elif key=='cappa':
        cbar.ax.set_ylabel(r'$\log{\kappa}$',fontsize=15)
    elif key=='lum':
        cbar1.ax.set_ylabel('logL',fontsize=15)
        cbar2.ax.set_ylabel('log(-L)',fontsize=15)
    elif key=='nenb':
        cbar.ax.set_ylabel(r'$\log{(n_\mathrm{e}/n_\mathrm{b})}$',fontsize=15)
        if not keylog:
            cbar.ax.set_ylabel(r'$n_{\mathrm{e}}/n_{\mathrm{b}}$',fontsize=15)
    else:
        cbar.ax.set_ylabel('$\log($'+key+'$)$',fontsize=15)
        
    if tight: plt.tight_layout()
    if phots: plt.legend(prop={'size':12})