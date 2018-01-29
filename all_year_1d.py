#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 30. jun. 2017

@author: ELP
'''

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets,QtGui, QtCore
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

import readdata
import read_field


def plot(self): 
               
    plt.clf()        
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError: 
        print ("Choose the variable to print ")       
        messagebox = QtWidgets.QMessageBox.about(self, "Retry",
                                             'Choose variable,please') 
        return None 
     
    start = self.numday_box.value() 
    stop = self.numday_stop_box.value() 
    data_units = self.fh.variables[index].units                
    self.figure.patch.set_facecolor('white') 
    gs = gridspec.GridSpec(3,1) 
    gs.update(left=0.3, right=0.7,top = 0.94,bottom = 0.04,
               wspace=0.2,hspace=0.3) 
    
    self.ax00 = self.figure.add_subplot(gs[0]) # water         
    self.ax10 = self.figure.add_subplot(gs[1]) # bbl
    self.ax20 = self.figure.add_subplot(gs[2]) # sediment 
    
    for axis in (self.ax00,self.ax10,self.ax20):
        axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major')                
        axis.yaxis.grid(True,'major')    
    
    numcol = self.numcol_2d.value() # 
    
    # read chosen variable 
    z = np.array(self.fh.variables[index])
    z = np.array(z[:,:,numcol]) 
    
    self.ax00.set_title(index +', ' + data_units) 
    
    #Label y axis        
    self.ax00.set_ylabel('depth, m', 
                    fontsize= self.font_txt) 
    self.ax10.set_ylabel('depth, m', 
                    fontsize= self.font_txt)   
    self.ax20.set_ylabel('depth, cm', 
                    fontsize= self.font_txt)
    
    self.ax00.set_ylim(self.y1max,0) 
    
    #readdata.setmaxmin(self,self.ax00,z,type)
    
        
    self.ax00.axhspan(self.y1max,0,color='#dbf0fd',
                 alpha = 0.7,label = "water" )
     
    self.ax10.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    self.ax10.set_ylim(self.y2max, self.y1max)   
    self.ax10.axhspan(self.y2max, self.y1max,color='#c5d8e3',
                 alpha = 0.4, label = "bbl"  )                
    
    
    self.ax20.set_ylim(self.ysedmax, self.ysedmin) 

    self.ax20.axhspan(self.ysedmin,0,
                 color='#c5d8e3',alpha = 0.4,
                 label = "bbl"  )        
    self.ax20.axhspan(self.ysedmax,0,
                 color='#b08b52',alpha = 0.4,
                 label = "sediment"  )
    
    #if  self.change_limits_checkbox.isChecked():
    readdata.set_maxmin(self,z)

    for n in range(start,stop,10):#365 
        self.ax00.plot(z[n][0:self.ny2max],
              self.depth[0:self.ny2max],
              self.spr_aut,alpha = self.a_w, 
              linewidth = self.linewidth , zorder = 8) 

        self.ax10.plot(z[n][0:self.ny2max],
              self.depth[0:self.ny2max],
              self.spr_aut,alpha = self.a_w, 
              linewidth = self.linewidth , zorder = 8) 
    
        self.ax20.plot(z[n][self.nysedmin-1:],
              self.depth_sed[self.nysedmin-1:],
              self.spr_aut, alpha = self.a_w,
              linewidth = self.linewidth, zorder = 8)                          
   
    if self.fielddata_checkbox.isChecked():
        from read_field import field
        #array = readdata_qmain.ReadVar(
        #    self.filename,index,start,stop)
        index = str(self.qlistwidget.currentItem().text())
        field(index,self.ax00,self.ax10,self.ax20) 
        
                              
    self.canvas.draw()     
