# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:08:26 2022

@author: USER
"""

reskeys_raw = ['ZON','AM/SOL','R14.','V 8.','T 5.','Trad5','lgD-6.','lgP 7.',\
               'lgQv','lgQRT','XHI','ENG','LUM','CAPPA','ZON2','n_bar','n_e','Fe','II','III']
    
reskeys_eng = ['thermal','virial','kinetic','radiat','gravit','total','gained','surfL',\
               'vol_gains_pow','tot_gains_pow','viscous virial','virial balance','total balance']
    
reskeys = ['mass','logm','xm','zone','temp','trad','vel','rad','rho','press',\
           'cappa','lum','n_bar','n_e','XHI']

swdkeys = [('logT',5),('logTrad',6),('vel',4),('logR',3),('logRho',7),('logP',8),\
           ('cappa',12),('L',11),('logqv',9),('eng12',10)]
    
# swdkeys = ['time','zone','xm','logm','mass','logR','vel','logT','logTrad',\
#            'logRho','logP','logqv','eng12','L','cappa']
    
hydkeys = [('dm',1),('rad',2),('rho',3),('temp',4),('vel',5),('mass',6)]
    
abnkeys = [('H',4),('He',5),('C',6),('N',7),('O',8),('Ne',9),('Mg',11),\
           ('Si',13),('S',14),('Ar',15),('Ca',16),('Fe',17),('Ni',19)]