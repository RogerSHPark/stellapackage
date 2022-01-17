# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 10:54:36 2022

@author: USER
"""

from stellapkg.parser.TTparser import tt_data
from stellapkg.parser.PHparser import ph_data
from stellapkg.parser.RESparser import res_data
from stellapkg.parser.SWDparser import swd_data

import matplotlib.pyplot as plt
import numpy as np

class Plotter():
    
    def __init__(self,a):
        self.a = a
        print('Loaded plotter')
        
    def __del__(self):
        print('Plotter closed')

    def LCplot(self,filters=['bol','U','B','V','R','I'],colors=['k','c','b','g','r','m'],ls='-',\
             xlim=True,x1=-0.5,x2=20,ylim=True,y1=-12,y2=-20,label=True,xlabel='Time [day]',\
             ylabel='Absolute magnitudes',oplot=False,grid=True,tight=True,legend=True):
        
        a = self.a
    
        ttfilt = ['bol','U','B','V','R','I']
        phfilt = ['ZTFg','ZTFr','u','g','r','i','z']
    
        for i, filt in enumerate(filters):
            if (filt not in ttfilt) and (filt not in phfilt):
                print(filt+" filter not available")
                print("Available filters: ", end=' ')
                print(*ttfilt, sep=', ', end=', ')
                print(*phfilt, sep=', ')
                return
            
        if len(colors)!=len(filters):
            print("Number of colors must match number of filters\n")
            print(f"Current: {len(colors)} colors, {len(filters)} filters")
            return
    
        if any(i in filters for i in ttfilt):
            ttm = tt_data(a)
        if any(i in filters for i in phfilt):
            phm = ph_data(a).get_photm()
    
        if not oplot: plt.figure()
      
        for i, filt in enumerate(filters):
            if filt in ttfilt:
                time = ttm.data['time']
                mag = ttm.data['M'+filt]
            if filt in phfilt:
                time = phm['time']
                mag = phm[filt]
            c = colors[i]
            plt.plot(time,mag,color=c,ls=ls,label=filt)
        if not oplot:
            if xlim: plt.xlim(x1,x2)
            if ylim: plt.ylim(y1,y2)
            if label:
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
            if grid: plt.grid(ls='--',color='grey',lw=0.5)
        if legend: plt.legend()
        if tight: plt.tight_layout()
                  
    def IPplot(self,t1,t2,key,xkey='logm',phots=True,propert=False,oplot=False,grid=True,tight=True,legend=True):
        
        from matplotlib import cm
        import matplotlib.patheffects as mpe
        
        a = self.a
        
        reskeys = ['mass','logm','xm','zone','temp','trad','vel','rad','rho','press',\
                'cappa','n_bar','n_e','lum','XHI','rhoNm','nenb']
        swdkeys = ['zone','xm','logR','vel','logT','logTrad','logRho','logP',\
                'logqv','eng12','L','cappa','logm','mass','logRhoNm']
        
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
            f = res_data(a)
            if phots: 
                pts = f.get_phots()
            if propert:
                time = np.array(f.data['protime'])
            else:
                time = np.array(f.data['obstime'])
            time2 = time[np.where((time>=t1) & (time<=t2))[0]]
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
                        
        elif key in swdkeys:
            # dtype = 'swd'
            print("Selected key in .swd file")
            f = swd_data(a)
            if phots: 
                pts = f.get_phots()
            time = np.array(f.grid['time'])
            time2 = time[np.where((time>=t1) & (time<=t2))[0]]
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
                plt.xlabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$',fontsize=12)
            elif xkey=='mass':
                plt.xticks(np.linspace(1.4,3.6,12)); plt.xlim(1.4,3.6)
                plt.xlabel(r'$M_{r}$',fontsize=12)
            elif xkey=='zone':
                plt.xticks(np.linspace(0,250,11)); plt.xlim(-5,255)
                plt.xlabel('Mass zone',fontsize=12)
                
            if key=='logR' or key=='rad': 
                plt.ylabel('logR',fontsize=12)
            elif key=='logT' or key=='temp': 
                plt.ylabel('logT',fontsize=12)
            elif key=='logTrad' or key=='trad': 
                plt.ylabel(r'$\log{T_\mathrm{rad}}$',fontsize=12)
            elif key=='vel': 
                plt.ylabel('logv',fontsize=12)
                plt.ylim(7.0,9.5)
            elif key=='logRhoNm' or key=='rhoNm':
                plt.ylabel(r'$\log{(\rho/\bar{\rho})}$',fontsize=12)
            elif key=='logRho' or key=='rho':
                plt.ylabel(r'$\log{\rho}$',fontsize=12)
            elif key=='logP' or key=='press':
                plt.ylabel('logP',fontsize=12)
            elif key=='cappa':
                plt.ylabel(r'$\log{\kappa}$',fontsize=12)
            elif key=='L' or key=='lum':
                plt.ylabel('logL',fontsize=12)
            elif key=='nenb':
                plt.ylabel(r'$\log{(n_\mathrm{e}/n_\mathrm{b})}$',fontsize=12)
            elif key in swdkeys:
                plt.ylabel(key,fontsize=12)
            else:
                plt.ylabel('$\log($'+key+'$)$',fontsize=12)
                
            if grid: plt.grid(ls='--',color='grey',lw=0.5)
        if legend: plt.legend()
        if tight: plt.tight_layout()
        
    def KPHplot(self,key,levels=[],xkey='logm',propert=False,logt=False,t1=0.,t2=15.,phots=False,grid=True,tight=True):
        
        from matplotlib import cm
        
        a = self.a
        
        reskeys = ['mass','logm','xm','zone','temp','trad','vel','rad','rho','press',\
                'cappa','n_bar','n_e','lum','XHI','rhoNm','nenb']
            
        if key not in reskeys:
            print('Input must be one of these keys: ',end='')
            print(*reskeys,sep=', ')
            return
        
        if xkey not in ['logm','mass','zone']:
            print('Choose xkey from following: logm, mass, zone')
            print('mass: simple Mr; logm: log(1-Mr/Mtot); zone: mass shell number')
            return        
        
        f = res_data(a)
        
        phots = phots and (not propert)
        
        if phots:
            pts = f.get_phots()
        
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
            ct1 = ax1.contour(tgrid,mgrid,z1,levels=levels,linewidths=0.3,colors='k')
            ct2 = ax1.contour(tgrid,mgrid,z2,levels=levels,linewidths=0.3,colors='k')
            ctf1 = ax1.contourf(tgrid,mgrid,z1,levels=levels,cmap=cm.Blues)
            ctf2 = ax1.contourf(tgrid,mgrid,z2,levels=levels,cmap=cm.Reds)
            cbar1 = fig.colorbar(ctf1)
            cbar2 = fig.colorbar(ctf2)
        else:
            for t in times:
                prof = f.get_profile(t,propert=propert)
                var = np.array(prof[key])
                logvar = np.log10(var)
                marr = np.array(prof[xkey])
                if marr[-1]<marr[0]:
                    logvar = np.flip([logvar])[0]
                    marr = np.flip([marr])[0]
                logvar = np.interp(mgrid,marr,logvar)
                z.append(logvar)
            
            z = np.array(z)
            
            if len(levels)==0:
                zn = z[np.where((tgrid>=t1) & (tgrid<=t2))[0]]
                levels = np.linspace(np.min(zn),np.max(zn),21)
    
            z = np.transpose(z)
    
            fig, ax1 = plt.subplots()        
            ct = ax1.contour(tgrid,mgrid,z,levels=levels,linewidths=0.3,colors='k')
            ctf = ax1.contourf(tgrid,mgrid,z,levels=levels,cmap=cm.viridis)
            cbar = fig.colorbar(ctf)

        if phots:
            tph = np.array(pts['time'])
            mph = np.array(pts[xkey+'ph'])
            ax1.plot(tph,mph,marker='o',markersize=4,c='r',label='Location of photosphere')
        
        ax1.set_xlim(t1,t2)
        if logt:
            ax1.set_xscale('log')
            if propert:
                ax1.set_xlim(max(1,t1),t2)
            else:
                ax1.set_xlim(max(0.001,t1),t2)
        ax1.set_xlabel('Time [day]',fontsize=12)
        if propert: ax1.set_xlabel('Time [sec]',fontsize=12)
        
        if xkey=='logm':
            ax1.set_yticks(np.linspace(0,-5,11))
            ax1.set_ylim(np.max(mgrid),np.min(mgrid))
            ax1.set_ylabel(r'$\log{(1-M_{r}/M_\mathrm{tot})}$',fontsize=12)
        elif xkey=='mass':
            # ax1.set_ylim(np.floor(10.*np.min(y))/10.,np.ceil(10.*np.max(y))/10.)
            ax1.set_ylim(np.min(mgrid),np.max(mgrid))
            ax1.set_ylabel(r'$M_{r}$',fontsize=12)
        else:
            ax1.set_ylim(0,250)
            ax1.set_yticks(np.linspace(0,250,11))
            ax1.set_ylabel('Mass zone',fontsize=12)
        
        if grid: ax1.grid(ls='--',c='white',lw=0.3)
        
        if key=='rad': 
            cbar.ax.set_ylabel('logR',fontsize=12)
        elif key=='temp': 
            cbar.ax.set_ylabel('logT',fontsize=12)
        elif key=='trad': 
            cbar.ax.set_ylabel(r'$\log{T_\mathrm{rad}}$',fontsize=12)
        elif key=='vel': 
            cbar.ax.set_ylabel('logv',fontsize=12)
        elif key=='rhoNm':
            cbar.ax.set_ylabel(r'$\log{(\rho/\bar{\rho})}$',fontsize=12)
        elif key=='rho':
            cbar.ax.set_ylabel(r'$\log{\rho}$',fontsize=12)
        elif key=='press':
            cbar.ax.set_ylabel('logP',fontsize=12)
        elif key=='cappa':
            cbar.ax.set_ylabel(r'$\log{\kappa}$',fontsize=12)
        elif key=='lum':
            cbar1.ax.set_ylabel('logL',fontsize=12)
            cbar2.ax.set_ylabel('log(-L)',fontsize=12)
        elif key=='nenb':
            cbar.ax.set_ylabel(r'$\log{(n_\mathrm{e}/n_\mathrm{b})}$',fontsize=12)
        else:
            plt.ylabel('$\log($'+key+'$)$',fontsize=12)
            
        if tight: plt.tight_layout()
        if phots: plt.legend()