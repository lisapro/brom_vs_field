#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 
'''
Created on 14. des. 2016

@author: E.Protsenko
'''


from netCDF4 import Dataset,num2date

import main
import numpy as np
import math
from matplotlib import ticker
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
from PyQt5 import QtWidgets,QtGui, QtCore
import os, sys 

#getcontext().prec = 6 
majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   
#format y scales to be scalar 
minorLocator = mtick.MultipleLocator(1.)

app1 = QtWidgets.QApplication(sys.argv)
screen_rect = app1.desktop().screenGeometry()
width, height = screen_rect.width(), screen_rect.height()

rc('font', **{'sans-serif' : 'Arial', #for unicode text
                'family' : 'sans-serif'})  
      
def readdata_brom(self,fname): #,varname,fname
    
    self.fh = Dataset(fname)    
    self.time =  self.fh.variables['time'][:]
    self.time_units = self.fh.variables['time'].units
    self.lentime = len(self.time)  
    self.fh.close()
    
def read_num_col(self,fname):
    # Read all variables name from the file 
    # And add them to the qlistwidget        
    self.fh = Dataset(fname)    
    self.names_vars = [] 
    
    for names,vars in self.fh.variables.items():
        self.names_vars.append(names) 
    flux_list = []
    sink_list = []
    other_list = []        
    for name in self.names_vars: 
        if name[:4] == 'fick':
            flux_list.append(name) 
        elif name[:4] == 'sink':
            sink_list.append(name)
        elif name not in ['z','z2','kz','time','i']:    
            other_list.append(name)         
        
    # sort variables alphabetically non-case sensitive            
    self.sorted_names =  sorted(other_list, key=lambda s: s.lower())  
    self.sorted_names.extend(flux_list) 
    self.sorted_names.extend(sink_list)  
    
    #Read i variable to know number of columns     
    for names,vars in self.fh.variables.items():
        if 'i' in self.names_vars and names not in ['z','z2','time']:
            self.testvar = np.array(self.fh['i'][:]) 
            self.max_num_col = self.testvar.shape[0]     
            break  
           
def readdata2_brom(self,fname):  
    #print ('in readdata_brom')   
    self.fh = Dataset(fname)
    self.depth = self.fh.variables['z'][:]  
    
    if 'kz' in self.names_vars or 'Kz' in self.names_vars:    
        self.depth2 = self.fh.variables['z2'][:] 
        #middle points   
        self.kz =  self.fh.variables['Kz'][:,:] 
        self.lendepth2 = len(self.depth2)
        # bbl width depends on depth
        if self.lendepth2 < 50 :
            self.bbl = 0.3 #0.5 
        else :
            self.bbl = 0.5         
    self.time =  self.fh.variables['time'][:]
    self.time_units = self.fh.variables['time'].units
    #time_calendar = self.fh.variables['time'].calendar
    #print (time_calendar)
    self.dates = num2date(self.time[:],
                          units= self.time_units)   
                 
    #print (min(self.dates),max(self.dates))
    #time = dates 
    #if 'i' in self.names_vars: 
    #    self.dist = np.array(self.fh.variables['i']) 

def read_all_year_var(self,fname,varname1,varname2,varname3): 
    self.fh = Dataset(fname)  
    self.var1 = self.fh.variables[varname1][:]
    self.var2 = self.fh.variables[varname2][:]
    self.var3 = self.fh.variables[varname3][:]  
    return  self.var1,self.var2, self.var3      
    self.fh.close()
         
def colors(self):
    self.spr_aut ='#998970'
    self.wint =  '#8dc0e7'
    self.summ = '#d0576f' 
    self.a_w = 0.4 #alpha_wat alpha (transparency) for winter
    self.a_bbl = 0.3     
    self.a_s = 0.4 #alpha (transparency) for summer
    self.a_aut = 0.4 #alpha (transparency) for autumn and spring    
    self.wat_col = '#c9ecfd' 
 
    self.bbl_col = '#2873b8' 
    self.sed_col= '#916012'
    self.wat_col1 = '#c9ecfd'  
    self.bbl_col1 = '#ccd6de'
    self.sed_col1 = '#a3abb1'
        
    #define color maps 
    #self.cmap = plt.cm.jet #gnuplot#jet#gist_rainbow
    #self.cmap1 = plt.cm.rainbow 

    self.font_txt = 15 #(height / 190.)
    # text on figure 2 (Water; BBL, Sed) 
    self.xlabel_fontsize = 10
    #(height / 170.) #14 #axis labels      
    self.ticklabel_fontsize = 10 #(height / 190.) #14 #axis labels   
    self.linewidth = 0.7   
             
def axis_pos(self): # for plot with all var in one page 
    # disctances between x axes
    dx = 0.1 #(height / 30000.) #0.1
    dy = 14 #height/96
    
    #x and y positions of axes labels 
    self.labelaxis_x =  1.10     
    self.labelaxis1_y = 1.02    
    self.labelaxis2_y = 1.02 + dx
    self.labelaxis3_y = 1.02 + dx * 2.
    self.labelaxis4_y = 1.02 + dx * 3.
    self.labelaxis5_y = 1.02 + dx * 4.

    # positions of xaxes
    self.axis1 = 0
    self.axis2 = 0 + dy 
    self.axis3 = 0 + dy * 2
    self.axis4 = 0 + dy * 3
    self.axis5 = 0 + dy * 4  
  
def calculate_ywat(self):
    for n in range(0,(len(self.depth2)-1)):
        if self.depth2[n+1] - self.depth2[n] >= self.bbl:
            if n == self.lendepth2-2: # len(self.depth2):
                y1max = (self.depth2[n]-1)
                self.ny1min = (self.depth[0])
                self.y1max = y1max                                                     
                self.ny1max = n-1
                self.sediment = False 
                break  
        elif self.depth2[n+1] - self.depth2[n] < self.bbl:   
            self.y1max = (self.depth[n])                               
            self.ny1max = n 
            self.sediment = True
            break
          
def calculate_ybbl(self):
    for n in range(0,(len(self.depth2)-1)):        
        if self.kz[1,n,0] == 0:
            self.y2max = self.depth2[n]         
            self.ny2max = n  
            #print ('y2max' ,self.y2max)      
            break  
        if self.kz[1,n,0] != 0 and n == (len(self.depth2)-2):       
            self.y2max = self.depth2[n]         
            self.ny2max = n  
            #print ('no sediment' , self.kz[0,n,0],n)   
            
def y2max_fill_water(self):    
    for n in range(0,(len(self.depth2)-1)):
        if self.depth2[n+1] - self.depth2[n] >= self.bbl:
            pass
        elif self.depth2[n+1] - self.depth2[n] < self.bbl:
            self.y2max_fill_water = self.depth2[n] 
            self.nbblmin = n            
            break 
         
def calculate_ysed(self):
    for n in range(0,(len(self.depth_sed))):
        if self.kz[1,n,0] == 0:
            ysed = self.depth_sed[n] #0 cm depth             
            self.ysedmin =  ysed - 10
            self.ysedmax =  self.depth_sed[len(self.depth_sed)-1]        
            self.y3min = self.depth_sed[self.nbblmin+2]             
            break  
        else : 
            self.ysedmax =  max(self.depth_sed) 
           
def calc_nysedmin(self):
    m = 0      
    self.ysedmin = - 10           
    for n in (self.depth_sed):
        if n >= self.ysedmin :
            self.nysedmin = m 
            break
        else: 
            m = m+1
    return self.nysedmin    
 
         
def y_coords(self):       
    self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
    self.y2min_fill_bbl = self.y2max_fill_water = self.y1max
    self.ysedmax_fill_bbl = 0
    self.ysedmin_fill_sed = 0
    self.y1min = 0
    self.y2min = self.y2max - 2*(self.y2max - self.y1max)   
          
# calc depth in cm from sed/wat interface 
def depth_sed(self):
    to_float = []
    for item in self.depth:
        to_float.append(float(item)) #make a list of floats from tuple 
    depth_sed = [] # list for storing final depth data for sediment 
    v=0  
    for i in to_float:
        v = (i- self.y2max)*100  #convert depth from m to cm
        depth_sed.append(v)
        self.depth_sed = depth_sed
    to_float = []
    for item in self.depth2:
        to_float.append(float(item)) #make a list of floats from tuple 
    depth_sed2 = [] # list for storing final depth data for sediment 
    v=0  
    for i in to_float:
        v = (i- self.y2max)*100  #convert depth from m to cm
        depth_sed2.append(v)
        self.depth_sed2 = depth_sed2  
        #print ('in depth_sed2')     
            
'''         
def varmax(self,variable,vartype,start,stop): 
    if vartype == 'watdist': #water
        n = variable[start:stop,0:self.ny1max].max() 

    elif vartype == 'seddist' :#sediment dist 
        n = variable[start:stop,self.nysedmin:].max()
  
    elif vartype == 'wattime': #time plot water
        n = variable[0:self.ny1max,:].max()
      
    elif vartype == 'sedtime' : #time plot sediment
        n = variable[self.nysedmin-2:,:].max()

                                                                                         
    self.watmax =  n   
    return self.watmax
'''
        
     



# make "beautiful"  values to show on ticks  
def int_value(self,n,minv,maxv):
    num = self.num
         
    if (maxv - minv) >= num*10. and ( 
     maxv - minv) < num*100. :
        m = math.ceil(n/10)*10.
    elif ( maxv -  minv) >= num and (
         maxv -  minv) < 10.*num :
        m = math.ceil(n)        
    elif ( maxv -  minv) > num/10. and (
         maxv -  minv) < num :
        m = (math.ceil(n*10.))/10.        
    elif ( maxv -  minv) > num/100. and (
         maxv -  minv) < num/10. :
        m = (math.ceil(n*100.))/100.          
    elif ( maxv -  minv) > num/1000. and (
         maxv -  minv) < num/100. :
        m = (math.ceil(n*1000.))/1000.                      
    else :
        m = n  
          
    return m    


'''
# make "beautiful"  values to show on ticks 
def ticks(minv,maxv):    
        
    if (maxv - minv) >= 50000. and (
         maxv - minv) < 150000.  :
        ticks = np.arange(minv,maxv,50000) #+10000.        
    elif (maxv - minv) >= 10000. and (
         maxv - minv) < 50000.  :
        ticks = np.arange(minv,maxv,5000) #+5000.        
    elif (maxv - minv) > 3000. and (
       maxv - minv) < 10000.  : 
        ticks = np.arange(minv,maxv,1000) #+1000.        
    elif (maxv - minv) > 1500. and ( 
     maxv - minv) <= 3000. :
        #print('in 1500-3000')
        ticks = np.arange(minv,maxv,500) #+500.                        
    elif (maxv - minv) >= 1000. and ( 
     maxv - minv) <= 1500. :
        #print('in 1000-1500',maxv-minv)
        ticks = np.arange((math.trunc(minv/10)*10),maxv,200)           
    elif (maxv - minv) >= 300. and ( 
     maxv - minv) <= 1000. :
        #print('in 300-1000',maxv-minv)
        ticks = np.arange((math.trunc(minv/10)*10),maxv,100)   
        if minv < 100 :
            ticks = np.arange(0,maxv,100)   #+100.               
    elif (maxv - minv) >= 100. and ( 
     maxv - minv) < 300. :
        ticks = np.arange(minv-10,maxv,50) #+50. 
    elif (maxv - minv) > 50. and ( 
     maxv - minv) < 100. :
        ticks = np.arange(minv,maxv,10) #+10.        
    elif (maxv - minv) > 20. and ( 
     maxv - minv) <= 50. :
        ticks = np.arange(minv,maxv,5) #+5.
    elif (maxv - minv) > 3. and ( 
     maxv - minv) <= 20. :
        ticks = np.arange(minv,maxv,1) #+1.
    elif (maxv - minv) >= 1. and ( 
     maxv - minv) <= 3. :
        ticks = np.arange(minv,maxv,0.5) #+1.         
    elif (maxv - minv) > 0.2 and ( 
     maxv - minv) <= 1. :
        ticks = np.arange(minv,maxv,0.1) #+1.                  
    elif (maxv - minv) > 0.02 and ( 
     maxv - minv) <= 0.2 : 
        ticks = np.arange((math.trunc(minv/10)*10),maxv,0.01) 
    else : 
        ticks = [minv,maxv]    
        #+ (maxv - minv)/2.                  

    return ticks
'''
#function to define y limits  
'''
def y_lim1(self,axis): 
    self.xticks =(np.arange(0,100000))
    if axis in (self.ax00,self.ax10,self.ax20,
                self.ax30,self.ax40,self.ax50): #water
        axis.set_ylim([self.y2min, 0])
        axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major')                
        axis.yaxis.grid(True,'major') 

    elif axis in (self.ax01,self.ax11,self.ax21,
                  self.ax31,self.ax41,self.ax51): #BBL
        axis.set_ylim([self.y2max, self.y2min])
        axis.fill_between(self.xticks, self.y2max,
            self.y2min_fill_bbl,facecolor= self.bbl_col, 
            alpha=self.a_bbl)
        axis.yaxis.grid(True,'minor')
        axis.yaxis.grid(True,'major')   
        axis.xaxis.grid(True,'major')  
          
        # Set a property to on an artist object.
        # remove xticklabels          
        plt.setp(axis.get_xticklabels(), visible=False) 
        
    elif axis in (self.ax02,self.ax12,
            self.ax22,self.ax32,self.ax42,self.ax52): #sediment 
        axis.set_ylim([self.ysedmax, self.ysedmin]) 
        axis.fill_between(self.xticks, self.ysedmax_fill_bbl,
                          self.ysedmin,facecolor= self.bbl_col,
                          alpha=self.a_bbl)  
        axis.fill_between(self.xticks, self.ysedmax,
                          self.ysedmin_fill_sed,
                          facecolor= self.sed_col,
                          alpha=self.a_s)    
        axis.yaxis.set_major_locator(majorLocator)
        
        #define yticks
        axis.yaxis.set_major_formatter(majorFormatter)
        axis.yaxis.set_minor_locator(minorLocator)
        axis.yaxis.grid(True,'minor')
        axis.yaxis.grid(True,'major')
        axis.xaxis.grid(True,'major') 
'''             
'''                
def setmaxmin(self,axis,var,type):
    minv = varmin(self,var,type) #0 - water 
    maxv = varmax(self,var,type)
    axis.set_xlim([minv,maxv])  
    #tick = ticks(watmin,watmax)
    axis.set_xticks(np.arange(minv,maxv+((maxv - minv)/2.),
            ((maxv - minv)/2.)))      
'''

def set_maxmin(self,variable):
    if  self.change_limits_checkbox.isChecked():
        watmin = float(self.box_minwater.text())
        watmax = float(self.box_maxwater.text())     
        if watmin == watmax : 
            watmax += 0.01
            
        bblmin = float(self.box_minbbl.text())
        bblmax = float(self.box_maxbbl.text())
        if bblmin == bblmax : 
            bblmax += 0.01
                            
        sedmin = float(self.box_minsed.text())
        sedmax = float(self.box_maxsed.text())
        if sedmin == sedmax : 
            sedmax += 0.01 
 
    else: 
        
        watmin = variable[:,0:self.ny2max].min()               
        watmax = variable[:,0:self.ny2max].max() 
        bblmin = watmin       
        bblmax = watmax
        sedmin = variable[:,self.nysedmin:].min()          
        sedmax = variable[:,self.nysedmin:].max()  
        
    #rcParams['axes.formatter.limits'] = [0.01,1000]     
    from matplotlib.ticker import ScalarFormatter
    def fmt(x, pos):
        a, b = '{:.1e}'.format(x).split('e')
        b = int(b)
        return r'${} \cdot 10^{{{}}}$'.format(a, b) 
     
    if watmax < 0.01 or watmin > 10000 :
        for n in (self.ax00,self.ax10,self.ax20):
            n.xaxis.set_major_formatter(
            ticker.FormatStrFormatter('%0.1e'))    
            #self.ax00.set_major_formatter(xfmt)                    
    self.ax00.set_xlim(watmin,watmax) # water         
    self.ax10.set_xlim(bblmin,bblmax) # bbl
    self.ax20.set_xlim(sedmin,sedmax) # sediment 

def set_widget_styles(self):
    
    # Push buttons style
    for axis in (#self.time_prof_last_year, #self.time_prof_all,
                 self.fick_swi,self.fick_air, #self.dist_prof_button,
                 self.all_year_button,self.help_button):   
        axis.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')   
          
    self.help_button.setIcon(QtGui.QIcon('help.png'))   
    #self.help_button.setIconSize(QtCore.QSize(30,30))   
    # set zero border.
    #self.help_button.setStyleSheet('QPushButton{border: 0px solid;}')
        
    self.qlistwidget.setStyleSheet(
    'QListWidget{font: 25 px; background-color: #eadfda;  }')
     
    self.label_choose_var.setStyleSheet(
        'QLabel {border-width: 7px;'
        '  padding: 7px; font: bold 15px; }')        
    

def widget_layout(self): 
       
        #first line 
        
        self.grid.addWidget(self.toolbar,0,0,1,1)
        self.grid.addWidget(self.fick_air,0,1,1,1)        
        self.grid.addWidget(self.fick_swi,0,2,1,1)               
        self.grid.addWidget(self.time_groupBox,0,3,1,1)       
        self.grid.addWidget(self.cmap_groupBox ,0,4,2,1)     
        self.grid.addWidget(self.OptionsgroupBox ,0,5,2,1)  
                     
        #second line
        self.grid.addWidget(self.help_button,1,1,1,1)                                        
        self.grid.addWidget(self.all_year_button,1,2,1,1)    
        self.grid.addWidget(self.dist_groupBox,1,3,1,1)  
        
        #third line              
        self.grid.addWidget(self.canvas, 2, 1,1,8)     
        self.grid.addWidget(self.qlistwidget,2,0,2,1) 
        self.grid.addWidget(self.label_choose_var,1,0,1,1)  
     