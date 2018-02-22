#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 

'''
Created on 30. jun. 2017

@author: ELP
'''


import matplotlib.pyplot as plt
from PyQt5 import QtWidgets,QtGui, QtCore

import numpy as np
import readdata
import matplotlib.gridspec as gridspec



def fluxes(self,param): 
    plt.clf()     
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError:       
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry",'Choose variable,please') 
        return None           
    numcol = self.numcol_2d.value() # 
    start = self.numday_box.value() 
    stop = self.numday_stop_box.value() 
    selected_items = self.qlistwidget.selectedItems()
    
    tosed = '#d3b886'
    towater = "#c9ecfd" 
    linecolor = "#1da181" 
    var1 = str(selected_items[0].text())
    
    z = np.array(self.fh.variables[var1])
    z_units = self.fh.variables[var1].units
    
    zz =  z[:,:,numcol] #1column
    
    if len(selected_items)== 1:
        
        #print (zz.shape)
        gs = gridspec.GridSpec(1,1)
        ax00 = self.figure.add_subplot(gs[0])
        ax00.set_xlabel('Julian day')   
        if self.yearlines_checkbox.isChecked() == True:
            for n in range(start,stop):
                if n%365 == 0: 
                    ax00.axvline(n,
                    color='black',
                    linestyle = '--') 
        #if self.injlines_checkbox.isChecked()== True: 
        #        ax00.axvline(365,color='red', linewidth = 2,
        #                linestyle = '--',zorder = 10) 
        #        ax00.axvline(730,color='red',linewidth = 2,#1825 730
        #                linestyle = '--',zorder = 10)                            
    elif len(selected_items)== 2:
        gs = gridspec.GridSpec(2,1)
        
        ax00 = self.figure.add_subplot(gs[0])
        ax01 = self.figure.add_subplot(gs[1])
        ax01.set_xlabel('Julian day')  
        if self.yearlines_checkbox.isChecked() == True:
            for n in range(start,stop):
                if n%365 == 0: 
                    ax00.axvline(n,color='black',
                    linestyle = '--') 
                    ax01.axvline(n,color='black',
                    linestyle = '--') 
            # injection   
        '''if self.injlines_checkbox.isChecked()== True: 
                ax00.axvline(365,color='red', linewidth = 2,
                        linestyle = '--',zorder = 10) 
                ax00.axvline(730,color='red',linewidth = 2,#1825 730
                        linestyle = '--',zorder = 10)  
                  
                ax01.axvline(365,color='red', linewidth = 2,
                        linestyle = '--',zorder = 10) 
                ax01.axvline(730,color='red',linewidth = 2,
                        linestyle = '--',zorder = 10)   ''' 
                                                                   
        #print (str(selected_items[1].text()))
        var2 = str(selected_items[1].text())
        z2_units = self.fh.variables[var2].units
        z2 = np.array(self.fh.variables[str(selected_items[1].text())])
        zz2 =  z2[:,:,numcol] #1column
        ax01.set_title(var2+', '+ z2_units)
        ax01.set_ylabel('Fluxes') #Label y axis
        ax01.set_xlim(start,stop)
        ax01.axhline(0, color='black', linestyle = '--') 
        fick2 = []
        for n in range(start,stop): 
            # take values for fluxes at sed-vat interf
            fick2.append(zz2[n][self.nysedmin])   
        fick2 = np.array(fick2)     
        ax01.plot(self.time[start:stop],fick2, linewidth = 1 ,
                    color = linecolor, zorder = 10)  
        #if self.yearlines_checkbox.isChecked() == True:
        #    for n in range(start,stop):
        #        if n%365 == 0: 
        #            ax01.axvline(n,
        #            color='black', linestyle = '--')      
        ax01.fill_between(self.time[start:stop], fick2, 0,
                           where= fick2 >= 0. , 
                           color = tosed, label= u"down" )
        ax01.fill_between(self.time[start:stop],  fick2, 0 ,
                      where= fick2 < 0.,color = towater, label=u"up")            
        ax01.set_ylim(max(fick2),min(fick2)) 
        
    else : 
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry",'Choose 1 or 2 variables,please') 
        return None  
    
    
    ax00.set_title(var1+', '+ z_units )
    #                , fontweight='bold')
    ax00.set_ylabel('Fluxes') #Label y axis
    
    fick = []
    for n in range(start,stop): 
        # take values for fluxes at sed-vat interf
        if param == 'swi':
            fick.append(zz[n][self.nysedmin])
        elif param == 'air': 
            fick.append(zz[n][0])     
           
    fick = np.array(fick) 
    ax00.set_xlim(start,stop)
    #ax00.axhline(0, color='#877655', linestyle = '--') 

    ax00.plot(self.time[start:stop],fick, linewidth = 1 ,
              color = linecolor, zorder = 10)  

    ax00.fill_between(self.time[start:stop],fick,0,
                      where = fick >=0, color = tosed, label= u"down" )
    ax00.fill_between(self.time[start:stop],  fick, 0 ,
                      where= fick < 0.,color = towater, label=u"up")
    ax00.set_ylim(max(fick),min(fick)) 
    m = np.mean(fick)
    ax00.axhline(m,c = 'r', linestyle = '--',label = 'mean', zorder = 10)
    #ax.text(3, 8, 'boxed italics text in data coords', style='italic',
    #    bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    ax00.annotate('Mean Flux = {0:.2e}'.format(m),
                  bbox={'facecolor':'w', 'alpha':0.7,
                        'edgecolor':'none', 'pad':5},
                  fontweight='bold', xy =(start+50,m),
                   arrowprops=dict(arrowstyle="->"),
                   xytext=(start+70,m-(m/30.)),color = 'k',zorder = 10)
    self.canvas.draw()