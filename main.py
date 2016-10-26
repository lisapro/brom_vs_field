#!/usr/bin/python
# Filename: readfile.py
# Import standard (i.e., non GOTM-GUI) modules.
import os,sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QSpinBox,QLabel
#from numpy import nan
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#import numpy as np
#from readfile import *
from netCDF4 import Dataset
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import style
import matplotlib.ticker as mtick
from decimal import*
getcontext().prec = 6 
majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   #format y scales to be scalar 
minorLocator = mtick.MultipleLocator(1.)
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rc('xtick', direction = 'out')
mpl.rc('xtick.major',pad = 0 ) 

from PyQt4.QtGui import QSpinBox,QLabel


class Window(QtGui.QDialog):
    background = 'white'
    #ysedmin = calculate_sedmin()
    #ysedmax = calculate_sedmax()    #10#depth[len(depth[:])-1]#110.1

    xticks =(np.arange(0,100000))
    xticks1 =(np.arange(0,100))

    wat_color = '#ffffff' # colors for filling water,bbl and sediment 
    bbl_color = '#ccd6de' # for plot 1,2,3,4,5,1_1,2_2,etc.
    sed_color = '#a3abb1' #'#7a8085' #666b6f '#'#916012'
        
    wat_color1 = '#c9ecfd' #colors for filling water, bbl and sediment 
    bbl_color1 = '#2873b8' # for fig1 and fig2 ( plot 6,6_1)
    sed_color1 = '#916012'    
    
    alpha_wat = 0.3 # saturation of color (from 0 to 1) 
    alpha_bbl = 0.3
    alpha_sed = 0.5
    alpha_autumn = 0.5
    spring_autumn ='#998970'#'#cecebd'#'#ffffd1'#'#e5e5d2'  
    winter = '#8dc0e7' 
    summer = '#d0576f' 
    linewidth = 0.5
    alpha = 0.5
    markersize= 13 #25    
#positions for different axes, sharing one subplot
    axis1 = 0
    axis2 = 27
    axis3 = 53
    axis4 = 79
    axis5 = 105

    labelaxis_x =  1.10 #positions of labels 
    labelaxis1_y = 1.02
    labelaxis2_y = 1.15
    labelaxis3_y = 1.26
    labelaxis4_y = 1.38
    labelaxis5_y = 1.48
    xlabel_fontsize = 14
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('like.png'))
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.figure = plt.figure(figsize = (30,10))

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Create buttons connected to 'plot' and 'plot1' method
        self.button1 = QtGui.QPushButton(' PO4,SO4,O2 annual')  
        self.button1.setStyleSheet('QPushButton {background-color: #faebd7;}')    
        self.button1_1 = QtGui.QPushButton('add PO4,SO4,O2 field data')   
        self.button1_1.setStyleSheet('QPushButton {background-color: #d8ebff;}')                       
        self.button2 = QtGui.QPushButton('T,S,Kz annual')   
        self.button2.setStyleSheet('QPushButton {background-color: #faebd7;}')       
        self.button2_1 = QtGui.QPushButton('add T,S,Kz field data')
        self.button2_1.setStyleSheet('QPushButton {background-color: #d8ebff;}')                       
        self.button3 = QtGui.QPushButton(' NO2,NO3,NH4 annual') 
        self.button3.setStyleSheet('QPushButton {background-color: #faebd7;}')  #color: red;              
        self.button3_1 = QtGui.QPushButton('add NO2,NO3,NH4 field data')          
        self.button3_1.setStyleSheet('QPushButton {background-color: #d8ebff;}')         
        self.button4 = QtGui.QPushButton(' Si,pH annual')  
        self.button4.setStyleSheet('QPushButton {background-color: #faebd7;}')  #color: red;                
        self.button4_1 = QtGui.QPushButton('add Si,pH field data')   
        self.button4_1.setStyleSheet('QPushButton {background-color: #d8ebff;}')                      
        self.button5 = QtGui.QPushButton('Mn,Fe,H2S annual')  
        self.button5.setStyleSheet('QPushButton {background-color: #faebd7;}')  #color: red;              
        self.button5_1 = QtGui.QPushButton('add Mn,Fe,H2S field data')   
        self.button5_1.setStyleSheet('QPushButton {background-color: #d8ebff;}')                 
#        self.openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)        
        self.openFile = QtGui.QPushButton('   ')
        self.openFile.setStyleSheet('QPushButton {background-color: #c7d2d2;}')                  
#        self.numday = QtGui.QPushButton('Choose day to plot')    
        self.numdaySpinBox = QSpinBox()
        self.Daylabel = QLabel('Choose day to plot:')
        self.numdaySpinBox.setRange(1, 366)
        self.numdaySpinBox.setValue(100)        
        
        self.button6 = QtGui.QPushButton('All(1) chosen day')  
        self.button6.setStyleSheet('QPushButton {background-color: #b3cc99 ;}')  #color: red;              
        self.button6_1 = QtGui.QPushButton('All(2) chosen day')   
        self.button6_1.setStyleSheet('QPushButton {background-color: #b3cc99 ;}')
                                   
        self.openFile.setShortcut('Ctrl+O')
#        self.openFile.setStatusTip('Open new File')
#        self.openFile.triggered.connect(self.showDialog)
                                    

        self.button1.clicked.connect(self.plot1) #Plot PO4,SO4,o2 
        self.button1_1.clicked.connect(self.plot1_field) #Plot field data for PO4,SO4,o2         
        self.button2.clicked.connect(self.plot2) #Plot T,S,Kz
        self.button2_1.clicked.connect(self.plot2_field)
        self.button3.clicked.connect(self.plot3) #Plot NO2,NO3,NH4   
        self.button3_1.clicked.connect(self.plot3_field)
        self.button4.clicked.connect(self.plot4) #Plot Si,pH 
        self.button4_1.clicked.connect(self.plot4_field) #Plot Si,pH      
        self.button5.clicked.connect(self.plot5) #Plot Mn,Fe,O2  
        self.button5_1.clicked.connect(self.plot5_field) #Plot Mn,Fe,O2          
        self.button6.clicked.connect(self.plot6) #  
        self.button6_1.clicked.connect(self.plot6_1) #               
#        self.openFile.clicked.connect(self.showDialog) #Plot PO4,SO4,o2                                        
#        self.numdaySpinBox = QSpinBox()
#        self.Daylabel = QLabel('Choose day to plot:')
#        self.numdaySpinBox.setRange(1, 366)
#        self.numdaySpinBox.setValue(100)      

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,2,1,8)
         
            
            
        layout.addWidget(self.canvas,1,2,1,8)      #position y,position x, length y,length x 
        
        layout.addWidget(self.button1,3,2,1,1) 
        layout.addWidget(self.button1_1,3,3,1,1)      
                  
        layout.addWidget(self.button2,4,2,1,1)
        layout.addWidget(self.button2_1,4,3,1,1)   
             
        layout.addWidget(self.button3,3,4,1,1)   
        layout.addWidget(self.button3_1,3,5,1,1)  
                         
        layout.addWidget(self.button4,4,4,1,1)         
        layout.addWidget(self.button4_1,4,5,1,1)   
                
        layout.addWidget(self.button5,3,6,1,1)  
        layout.addWidget(self.button5_1,3,7,1,2) 
                 
#        layout.addWidget(self.button6,4,4,1,1)   
        layout.addWidget(self.openFile,4,6,1,1)      
        layout.addWidget(self.Daylabel,4,7,1,1)   
        layout.addWidget(self.numdaySpinBox,4,8,1,1)  

        layout.addWidget(self.button6,3,9,1,1)         
        layout.addWidget(self.button6_1,4,9,1,1)
                                  
        self.setLayout(layout)        
        
      
    def showDialog(self):   
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
                                                  'Open netcdf ',
                                                  os.getcwd(),
                                                  "netcdf (*.nc);; all (*)"))            
        fh = Dataset(fname)
  
        self.depth = fh.variables['z'][:] 
        self.depth2 = fh.variables['z2'][:] #middle points
        self.alk =  fh.variables['Alk'][:,:]
        self.temp =  fh.variables['T'][:,:]
        self.sal =  fh.variables['S'][:,:]
        self.kz =  fh.variables['Kz'][:,:]
        self.dic =  fh.variables['DIC'][:,:]
        self.phy =  fh.variables['Phy'][:,:]
        self.het =  fh.variables['Het'][:,:]
        self.no3 =  fh.variables['NO3'][:,:]
        self.po4 =  fh.variables['PO4'][:,:]
        self.nh4 =  fh.variables['NH4'][:,:]
        self.pon =  fh.variables['PON'][:,:]
        self.don =  fh.variables['DON'][:,:]
        self.o2  =  fh.variables['O2'][:,:]
        self.mn2 =  fh.variables['Mn2'][:,:]
        self.mn3 =  fh.variables['Mn3'][:,:]
        self.mn4 =  fh.variables['Mn4'][:,:]
        self.h2s =  fh.variables['H2S'][:,:]
        self.mns =  fh.variables['MnS'][:,:]
        self.mnco3 =  fh.variables['MnCO3'][:,:]
        self.fe2 =  fh.variables['Fe2'][:,:]
        self.fe3 =  fh.variables['Fe3'][:,:]
        self.fes =  fh.variables['FeS'][:,:]
        self.feco3 =  fh.variables['FeCO3'][:,:]
        self.no2 =  fh.variables['NO2'][:,:]
        self.s0 =  fh.variables['S0'][:,:]
        self.s2o3 =  fh.variables['S2O3'][:,:]
        self.so4 =  fh.variables['SO4'][:,:]
        self.si =  fh.variables['Si'][:,:]
        self.si_part =  fh.variables['Sipart'][:,:]
        self.baae =  fh.variables['Baae'][:,:]
        self.bhae =  fh.variables['Bhae'][:,:]
        self.baan =  fh.variables['Baan'][:,:]
        self.bhan =  fh.variables['Bhan'][:,:]
        self.caco3 =  fh.variables['CaCO3'][:,:]
        self.fes2 =  fh.variables['FeS2'][:,:]
        self.ch4 =  fh.variables['CH4'][:,:]
        self.ph =  fh.variables['pH'][:,:]
        self.pco2 =  fh.variables['pCO2'][:,:]
        self.om_ca =  fh.variables['Om_Ca'][:,:]
        self.om_ar =  fh.variables['Om_Ar'][:,:]
        self.co3 =  fh.variables['CO3'][:,:]
        self.ca =  fh.variables['Ca'][:,:]
        self.time =  fh.variables['time'][:]
        
        self.calculate_watmax()
        self.calculate_nwatmax()
        self.calculate_bblmax()
        self.calculate_nbblmax()
        self.y2max_fill_water()
        self.y2min()
        self.y_coords()
        self.depth_sed()
        self.depth_sed2()
        self.calculate_sedmin()          
        self.calculate_sedmax()   
        self.maxmin()
        self.read_fielddata()        
        fh.close()
                
    def calculate_watmax(self):
        for n in range(0,(len(self.depth2)-1)):
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:    
                y1max = (self.depth2[n])
                self.y1max = y1max                               
#                return self.y1max
                break
            
#        self.y1max = 50# (len(self.depth2)) #y1max   
#        return self.y1max  
        
    def calculate_nwatmax(self):
        for n in range(0,(len(self.depth2)-1)):
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:    
                self.ny1max = n                               
                return self.ny1max
                break
      
    def calculate_bblmax(self):
        for n in range(0,(len(self.depth2)-1)):
            if self.kz[1,n] == 0:
                self.y2max = self.depth2[n]         
                return self.y2max
                break        
    def calculate_nbblmax(self):
        for n in range(0,(len(self.depth2)-1)):
            if self.kz[1,n] == 0:
                self.ny2max = n         
                return self.ny2max 
                break  
         
    def y2max_fill_water(self):
        for n in range(0,(len(self.depth2)-1)):
    #        if depth[_]-depth[_?]
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:
    #            watmax =  depth[n],depth[n]-depth[n+1],n
                self.y2max_fill_water = self.depth2[n]            
                return self.y2max_fill_water
                break
        
    #    y1max = calculate_watmax()
    #    ny1max = calculate_nwatmax()
    #y2min = y1max #109 #depth[len(depth[:])-19]#108.5
    #y2max = calculate_bblmax() #110.0 #(sed_wat interface)#depth[len(depth[:])-13]#
    #ny2max = calculate_nbblmax()
    
    def y_coords(self):       
#        self.y2min = self.y2max - 2*(self.y2max - self.y1max)   #calculate the position of y2min, for catching part of BBL 
        self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
        self.y2min_fill_bbl = self.y2max_fill_water = self.y1max #y2max_fill_water() #109.5 #BBL-water interface
        self.ysedmax_fill_bbl = 0
        self.ysedmin_fill_sed = 0
        self.y1min = 0
        
    def y2min(self):    
        y2min = self.y2max - 2*(self.y2max - self.y1max)          
        self.y2min = y2min
        #calculate the position of y2min, for catching part of BBL 
#y2max = 110 #(sed_wat interface)

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
#            return depth_sed

    def depth_sed2(self):
        to_float2 = []
        for item in self.depth2:
            to_float2.append(float(item)) #make a list of floats from tuple 
        depth_sed2 = [] # list for storing final depth data for sediment 
        v2=0  
        for i in to_float2:
            v2 = (i- self.y2max)*100  #convert depth from m to cm
            depth_sed2.append(v2) 
            self.depth_sed2 = depth_sed2
#            return depth_sed2
                        
    def calculate_sedmin(self):
        for n in range(0,(len(self.depth_sed)-1)):
            if self.kz[1,n] == 0:
                ysed = self.depth_sed[n]  
                self.ysedmin =  ysed - 10                 
#                return ysedmin
                break   
        
    def calculate_sedmax(self):
        for n in range(0,(len(self.depth_sed)-1)):
            if self.kz[1,n] == 0:
                ysed = self.depth_sed[n]    
                self.ysedmax =  ysed + 10                
                break  
        
    def y_lim(self,axis): #function to define y limits 
        if axis in (self.ax00,self.ax10,self.ax20):   #water          
            axis.set_ylim([self.y2min, 0])
#            axis.fill_between(self.xticks, self.y1max, self.y1min, facecolor= self.wat_color, alpha=self.alpha_wat)
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')   
        elif axis in (self.ax01,self.ax11,self.ax21):  #BBL
            axis.set_ylim([self.y2max, self.y2min])
#            axis.fill_between(self.xticks, self.y2max_fill_water, self.y2min, facecolor= self.wat_color, alpha=self.alpha_wat) 
            axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl, facecolor= self.bbl_color, alpha=self.alpha_bbl)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')   
            axis.xaxis.grid(True,'major')    
            plt.setp(axis.get_xticklabels(), visible=False)                                           
        elif axis in (self.ax02,self.ax12,self.ax22): #sediment 
            axis.set_ylim([self.ysedmax, self.ysedmin])   #[y3max, y3min]   
            axis.fill_between(self.xticks, self.ysedmax_fill_bbl, self.ysedmin, facecolor= self.bbl_color, alpha=self.alpha_bbl)  
            axis.fill_between(self.xticks, self.ysedmax, self.ysedmin_fill_sed, facecolor= self.sed_color, alpha=self.alpha_sed)    
            axis.yaxis.set_major_locator(majorLocator)   #define yticks
            axis.yaxis.set_major_formatter(majorFormatter)
            axis.yaxis.set_minor_locator(minorLocator)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')
            axis.xaxis.grid(True,'major')  
                           
    def y_lim1(self,axis): #function to define y limits 
        if axis in (self.ax00,self.ax10,self.ax20,self.ax30,self.ax40,self.ax50):   #water
            axis.set_ylim([self.y2min, 0])
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')  
#            axis.fill_between(self.xticks1, self.y1max, self.y1min, facecolor= self.wat_color1, alpha=self.alpha_wat)
        elif axis in (self.ax01,self.ax11,self.ax21,self.ax31,self.ax41,self.ax51):  #BBL
            axis.set_ylim([self.y2max, self.y2min])
            axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl, facecolor= self.bbl_color1, alpha=self.alpha_bbl)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')   
            axis.xaxis.grid(True,'major')              
#            axis.fill_between(self.xticks1, self.y2max_fill_water, self.y2min, facecolor= self.wat_color, alpha= self.alpha_wat) 
#            axis.fill_between(self.xticks1, self.y2max, self.y2min_fill_bbl, facecolor= self.bbl_color, alpha= self.alpha_bbl)
            plt.setp(axis.get_xticklabels(), visible=False) 
        elif axis in (self.ax02,self.ax12,self.ax22,self.ax32,self.ax42,self.ax52): #sediment 
            axis.set_ylim([self.ysedmax, self.ysedmin])   #[y3max, y3min]   
            axis.fill_between(self.xticks, self.ysedmax_fill_bbl, self.ysedmin, facecolor= self.bbl_color1, alpha=self.alpha_bbl)  
            axis.fill_between(self.xticks, self.ysedmax, self.ysedmin_fill_sed, facecolor= self.sed_color1, alpha=self.alpha_sed)    
            axis.yaxis.set_major_locator(majorLocator)   #define yticks
            axis.yaxis.set_major_formatter(majorFormatter)
            axis.yaxis.set_minor_locator(minorLocator)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')
            axis.xaxis.grid(True,'major')  

           
    def spines(self,axis):         
        for spinename, spine in axis.spines.iteritems():
            if spinename != 'top':
                spine.set_visible(False)                
        for axis in (self.ax00_1,self.ax02_1,self.ax10_1,self.ax12_1,self.ax20_1,
                    self.ax22_1,self.ax30_1,self.ax32_1,self.ax40_1,self.ax42_1,self.ax50_1,self.ax52_1):
            axis.spines['top'].set_position(('outward', self.axis1))
            axis.spines['top'].set_color('g')                   
        for axis in (self.ax00_2,self.ax02_2,self.ax10_2,self.ax12_2,self.ax20_2,self.ax22_2,self.ax30_2,
                      self.ax32_2,self.ax40_2,self.ax42_2,self.ax50_2,self.ax52_2):    
            axis.spines['top'].set_position(('outward', self.axis2))
            axis.spines['top'].set_color('r')   
        for axis in (self.ax00_3,self.ax02_3,self.ax10_3,self.ax12_3,self.ax30_3,self.ax32_3,
                      self.ax40_3,self.ax42_3,self.ax50_3,self.ax52_3,self.ax20_3,self.ax22_3,):  #  
            axis.spines['top'].set_position(('outward', self.axis3))
            axis.spines['top'].set_color('b') 
        for axis in (self.ax10_4,self.ax12_4,self.ax30_4,self.ax32_4,self.ax40_4,self.ax42_4,self.ax50_4,self.ax52_4):    #ax20_4,
            axis.spines['top'].set_position(('outward', self.axis4))
            axis.spines['top'].set_color('m')     
        for axis in (self.ax30_5, self.ax32_5) :    
            axis.spines['top'].set_position(('outward', self.axis5))
            axis.spines['top'].set_color('c')
        for axis in (self.ax00,self.ax01,self.ax02,self.ax01_1,self.ax01_2,self.ax01_3,self.ax10,#,#ax01_4,
                          self.ax11,self.ax11_1,self.ax11_2,self.ax11_3,self.ax11_4,self.ax12,self.ax20,
                          self.ax21,self.ax21_1,self.ax21_2,self.ax22,self.ax30,self.ax21_3,#ax21_4,
                          self.ax31,self.ax31_1,self.ax31_2,self.ax31_3,self.ax31_4,self.ax31_5,self.ax32,self.ax40,
                          self.ax41,self.ax41_1,self.ax41_2,self.ax41_3,self.ax41_4,self.ax42,self.ax50,self.ax51,
                          self.ax51_1,self.ax51_2,self.ax51_3,self.ax51_4,self.ax52):  
            plt.setp(axis.get_xticklabels(), visible=False)                                                

    def watmax(self,variable):
        n = variable[:,self.y1min:self.ny2max].max()#+ ((variable[:,y1min:y2max].max())/10))
        
        
        if n > 28000:
            n = 30000#np.ceil(n)        
        if n > 27000:
            n = 28000#np.ceil(n)
        if n > 26000:
            n = 27000#np.ceil(n)
        if n > 25000:
            n = 26000#np.ceil(n)
        elif n > 22500:
            n = 25000#np.ceil(n)              
        elif n > 20000:
            n = 22500#np.ceil(n)            
        elif n > 10000:
            n = 20000#np.ceil(n)    
        elif n > 7000 and n <= 10000:  
            n = 10000                     
        elif n > 5000 and n <= 7000:  
            n =7000 
        elif n > 2000 and n <= 5000:  
            n = 5000                                  
        elif n > 1000 and n <= 2000:  
            n = 2000        
        elif n > 500 and n <= 1000:  
            n = 1000 
        elif n > 350 and n <= 500:  
            n = 500                       
        elif n > 200 and n <= 350:  
            n = 350          
        elif n > 100 and n <= 200:  
            n = 200   
            
        elif n > 50 and n <= 100:
            n = 100    
        elif n > 25 and n <= 50:
            n = 50                             
        elif n > 10 and n <= 25:
            n = 25    
             
        elif n > 5 and n <= 10:
            n = 10
        elif n > 2.5 and n <= 5:
            n = 5      
        elif n > 1 and n <= 2.5:
            n = 2.5                     
        elif n > 0.5 and n <= 1:
            n = 1                     
        elif n > 0.05 and n <= 0.5:
            n = 0.5           
        elif n > 0.005 and n <= 0.05:
            n = 0.05         
        elif n > 0.0005 and n <= 0.005:
            n = 0.005
        elif n > 0.00005 and  n  <= 0.0005 :
            n = 0.0005   
        elif n <= 0.00005  :
            n = 0.00005               
        return n 

    def watmin(self,variable):
        n = np.round(variable[:,0:self.ny2max].min())
            
        if n >= 28000:
            n = 28000 #np.ceil(n)        
        if n >= 27000 and n < 28000:
            n = 27000#np.ceil(n)
        if n >= 26000 and n < 27000:
            n = 26000#np.ceil(n)
        if n >= 25000 and n < 26000:
            n = 25000#np.ceil(n)
        elif n >= 22500 and n < 25000 :
            n = 22500#np.ceil(n)              
        elif n >= 20000 and n < 22500:
            n = 20000#np.ceil(n)            
        elif n >= 10000 and n < 20000:
            n = 10000#np.ceil(n)    
        elif n >= 7000 and n < 10000:  
            n = 7000                     
        elif n >= 5000 and n < 7000:  
            n =5000         
        elif n >= 1000 and n < 5000:  
            n = 1000        
        elif n >= 500 and n < 1000:  
            n = 500 
        elif n >= 350 and n < 500:  
            n = 350                       
        elif n >= 200 and n < 350:  
            n = 200          
        elif n >= 100 and n < 200:  
            n = 100   
            
        elif n >= 50 and n < 100:
            n = 50    
        elif n >= 25 and n < 50:
            n = 25                             
        elif n >= 10 and n < 25:
            n = 10    
             
        elif n >= 6 and n < 10:
            n = 6
        elif n >= 5 and n < 6:
            n = 5            
        elif n >= 2.5 and n < 5:
            n = 2.5     
        elif n >= 1 and n < 2.5:
            n = 1                     
        elif n >=  0.5 and n <1:
            n = 0.5                     
        elif n >= 0.05 and n < 0.5:
            n = 0.05           
        elif n >=  0.005 and n <0.05:
            n = 0.005         
        elif n >=  0.0005 and n <= 0.005:
            n = 0.0005
        elif n >=  0.00005 and  n  <0.0005 :
            n = 0.00005   
           
#        return n         
                
        return n
    
    def sedmax(self,variable):
        n = np.ceil(variable[:,self.ny2min:].max())# + ((variable[:,ysedmin:ysedmax].max()))) #np.ceil   
        
        if n > 28000:
            n = 30000#np.ceil(n)        
        if n > 27000:
            n = 28000#np.ceil(n)
        if n > 26000:
            n = 27000#np.ceil(n)
        if n > 25000:
            n = 26000#np.ceil(n)
        elif n > 22500:
            n = 25000#np.ceil(n)              
        elif n > 20000:
            n = 22500#np.ceil(n)            
        elif n > 10000:
            n = 20000#np.ceil(n)    
        elif n > 7000 and n <= 10000:  
            n = 10000                     
        elif n > 5000 and n <= 7000:  
            n =7000         
        elif n > 2000 and n <= 5000:  
            n = 5000                                  
        elif n > 1000 and n <= 2000:  
            n = 2000          
        elif n > 500 and n <= 1000:  
            n = 1000 
        elif n > 350 and n <= 500:  
            n = 500                       
        elif n > 200 and n <= 350:  
            n = 350          
        elif n > 100 and n <= 200:  
            n = 200   
            
        elif n > 50 and n <= 100:
            n = 100    
        elif n > 25 and n <= 50:
            n = 50                             
        elif n > 10 and n <= 25:
            n = 25    
             
        elif n > 5 and n <= 10:
            n = 10
        elif n > 2.5 and n <= 5:
            n = 5      
        elif n > 1 and n <= 2.5:
            n = 2.5                     
        elif n > 0.5 and n <= 1:
            n = 1                     
        elif n > 0.05 and n <= 0.5:
            n = 0.5           
        elif n > 0.005 and n <= 0.05:
            n = 0.05         
        elif n > 0.0005 and n <= 0.005:
            n = 0.005
        elif n > 0.00005 and  n  <= 0.0005 :
            n = 0.0005   
        elif n <= 0.00005  :
            n = 0.00005               
        return n 
       
    def sedmin(self,variable):
        n = variable[:,self.ny2min:].min()
        if n >= 28000:
            n = 28000 #np.ceil(n)        
        if n >= 27000 and n < 28000:
            n = 27000#np.ceil(n)
        if n >= 26000 and n < 27000:
            n = 26000#np.ceil(n)
        if n >= 25000 and n < 26000:
            n = 25000#np.ceil(n)
        elif n >= 22500 and n < 25000 :
            n = 22500#np.ceil(n)              
        elif n >= 20000 and n < 22500:
            n = 20000#np.ceil(n)            
        elif n >= 10000 and n < 20000:
            n = 10000#np.ceil(n)    
        elif n >= 7000 and n < 10000:  
            n = 7000                     
        elif n >= 5000 and n < 7000:  
            n =5000         
        elif n >= 1000 and n < 5000:  
            n = 1000        
        elif n >= 500 and n < 1000:  
            n = 500 
        elif n >= 350 and n < 500:  
            n = 350                       
        elif n >= 200 and n < 350:  
            n = 200          
        elif n >= 100 and n < 200:  
            n = 100   
            
        elif n >= 50 and n < 100:
            n = 50    
        elif n >= 25 and n < 50:
            n = 25                             
        elif n >= 10 and n < 25:
            n = 10    
             
        elif n >= 10 and n < 25:
            n = 10    
             
        elif n >= 6 and n < 10:
            n = 6
        elif n >= 5 and n < 6:
            n = 5 
            
        elif n >= 2.5 and n < 5:
            n = 2.5     
        elif n >= 1 and n < 2.5:
            n = 1                     
        elif n >=  0.5 and n <1:
            n = 0.5                     
        elif n >= 0.05 and n < 0.5:
            n = 0.05           
        elif n >=  0.005 and n <0.05:
            n = 0.005         
        elif n >=  0.0005 and n <= 0.005:
            n = 0.0005
        elif n >=  0.00005 and  n  <0.0005 :
            n = 0.00005           
        
        
        
        
        return n
    
    def maxmin(self):
        self.kzmin = self.watmin(self.kz)
        self.kzmax = self.watmax(self.kz)
        self.sed_kzmin = self.watmin(self.kz)
        self.sed_kzmax = self.watmax(self.kz)        
        self.salmin = self.watmin(self.sal)
        self.salmax  = self.watmax(self.sal) 
        self.sed_salmin = self.sedmin(self.sal)
        self.sed_salmax = self.sedmax(self.sal)
        self.tempmin = self.watmin(self.temp)
        self.tempmax  = self.watmax(self.temp)
        self.po4max = self.watmax(self.po4) 
        self.po4min = self.watmin(self.po4)
        self.sed_po4min = self.sedmin(self.po4) 
        self.sed_po4max = self.sedmax(self.po4)  
        self.ponmax = self.watmax(self.pon) 
        self.ponmin = self.watmin(self.pon)
        self.sed_ponmin = self.sedmin(self.pon) 
        self.sed_ponmax = self.sedmax(self.pon)        
        self.donmax = self.watmax(self.don) 
        self.donmin = self.watmin(self.don)
        self.sed_donmin = self.sedmin(self.don) 
        self.sed_donmax = self.sedmax(self.don)         
        self.so4min = self.watmin(self.so4)
        self.so4max = self.watmax(self.so4)
        self.sed_so4min = self.sedmin(self.so4)
        self.sed_so4max = self.sedmax(self.so4) 
        self.o2min = self.watmin(self.o2)
        self.o2max = self.watmax(self.o2)            
        self.sed_o2min = self.sedmin(self.o2)            
        self.sed_o2max = self.sedmax(self.o2)
        self.no2min = self.watmin(self.no2)
        self.no2max = self.watmax(self.no2)
        self.sed_no2min = self.sedmin(self.no2)
        self.sed_no2max = self.sedmax(self.no2)
        self.no3min = self.watmin(self.no3)
        self.no3max = self.watmax(self.no3)
        self.sed_no3min = self.sedmin(self.no3)
        self.sed_no3max = self.sedmax(self.no3)             
        self.nh4min = self.watmin(self.nh4)
        self.nh4max = self.watmax(self.nh4)
        self.sed_nh4min = self.sedmin(self.nh4)
        self.sed_nh4max = self.sedmax(self.nh4)        
        self.simin = self.watmin(self.si)
        self.simax = self.watmax(self.si)   
        self.sed_simin = self.sedmin(self.si)
        self.sed_simax = self.sedmax(self.si)   
        self.phmin = self.watmin(self.ph)
        self.phmax = self.watmax(self.ph)   
        self.sed_phmin = self.sedmin(self.ph)
        self.sed_phmax = self.sedmax(self.ph) 

        self.fe2min = self.watmin(self.fe2)
        self.fe2max = self.watmax(self.fe2)
        self.sed_fe2min = self.sedmin(self.fe2)
        self.sed_fe2max = self.sedmax(self.fe2)      

        self.fe3min = self.watmin(self.fe3)
        self.fe3max = self.watmax(self.fe3)
        self.sed_fe3min = self.sedmin(self.fe3)
        self.sed_fe3max = self.sedmax(self.fe3) 

        self.fesmin = self.watmin(self.fes)
        self.fesmax = self.watmax(self.fes)
        self.sed_fesmin = self.sedmin(self.fes)
        self.sed_fesmax = self.sedmax(self.fes) 

        self.fes2min = self.watmin(self.fes2)
        self.fes2max = self.watmax(self.fes2)
        self.sed_fes2min = self.sedmin(self.fes2)
        self.sed_fes2max = self.sedmax(self.fes2) 
                  
        self.h2smin = self.watmin(self.h2s)
        self.h2smax = self.watmax(self.h2s)
        self.sed_h2smin = self.sedmin(self.h2s)
        self.sed_h2smax = self.sedmax(self.h2s)
        
        self.mn2min = self.watmin(self.mn2)
        self.mn2max = self.watmax(self.mn2)
        self.sed_mn2min = self.sedmin(self.mn2)
        self.sed_mn2max = self.sedmax(self.mn2)       

        self.mn3min = self.watmin(self.mn3)
        self.mn3max = self.watmax(self.mn3)
        self.sed_mn3min = self.sedmin(self.mn3)
        self.sed_mn3max = self.sedmax(self.mn3) 

        self.mn4min = self.watmin(self.mn4)
        self.mn4max = self.watmax(self.mn4)
        self.sed_mn4min = self.sedmin(self.mn4)
        self.sed_mn4max = self.sedmax(self.mn4) 
        
        self.mnsmin = self.watmin(self.mns)
        self.mnsmax = self.watmax(self.mns)
        self.sed_mnsmin = self.sedmin(self.mns)
        self.sed_mnsmax = self.sedmax(self.mns) 
        
        self.mnco3min = self.watmin(self.mnco3)
        self.mnco3max = self.watmax(self.mnco3)
        self.sed_mnco3min = self.sedmin(self.mnco3)
        self.sed_mnco3max = self.sedmax(self.mnco3) 
        
        self.s0min = self.watmin(self.s0)
        self.s0max = self.watmax(self.s0)
        self.sed_s0min = self.sedmin(self.s0)
        self.sed_s0max = self.sedmax(self.s0) 
        
        self.s2o3min = self.watmin(self.s2o3)
        self.s2o3max = self.watmax(self.s2o3)
        self.sed_s2o3min = self.sedmin(self.s2o3)
        self.sed_s2o3max = self.sedmax(self.s2o3) 
          
        self.baanmin = self.watmin(self.baan)
        self.baanmax = self.watmax(self.baan)
        self.sed_baanmin = self.sedmin(self.baan)
        self.sed_baanmax = self.sedmax(self.baan)              

        self.baaemin = self.watmin(self.baae)
        self.baaemax = self.watmax(self.baae)
        self.sed_baaemin = self.sedmin(self.baae)
        self.sed_baaemax = self.sedmax(self.baae)
        
        self.bhaemin = self.watmin(self.bhae)
        self.bhaemax = self.watmax(self.bhae)
        self.sed_bhaemin = self.sedmin(self.bhae)
        self.sed_bhaemax = self.sedmax(self.bhae)        
        
        self.bhanmin = self.watmin(self.bhan)
        self.bhanmax = self.watmax(self.bhan)
        self.sed_bhanmin = self.sedmin(self.bhan)
        self.sed_bhanmax = self.sedmax(self.bhan)        
        
        self.phymin = self.watmin(self.phy)
        self.phymax = self.watmax(self.phy)
        self.sed_phymin = self.sedmin(self.phy)
        self.sed_phymax = self.sedmax(self.phy)        
        
        self.hetmin = self.watmin(self.het)
        self.hetmax = self.watmax(self.het)
        self.sed_hetmin = self.sedmin(self.het)
        self.sed_hetmax = self.sedmax(self.het)        

        self.simin = self.watmin(self.si)
        self.simax = self.watmax(self.si)
        self.sed_simin = self.sedmin(self.si)
        self.sed_simax = self.sedmax(self.si)     
        
        self.si_partmin = self.watmin(self.si_part)
        self.si_partmax = self.watmax(self.si_part)
        self.sed_si_partmin = self.sedmin(self.si_part)
        self.sed_si_partmax = self.sedmax(self.si_part)        
        
        self.phmin = self.watmin(self.ph)
        self.phmax = self.watmax(self.ph)
        self.sed_phmin = self.sedmin(self.ph)
        self.sed_phmax = self.sedmax(self.ph)          
        
        self.alkmin = self.watmin(self.alk)
        self.alkmax = self.watmax(self.alk)
        self.sed_alkmin = self.sedmin(self.alk)
        self.sed_alkmax = self.sedmax(self.alk)  
        
        self.dicmin = self.watmin(self.dic)
        self.dicmax = self.watmax(self.dic)
        self.sed_dicmin = self.sedmin(self.dic)
        self.sed_dicmax = self.sedmax(self.dic)          

        self.pco2min = self.watmin(self.pco2)
        self.pco2max = self.watmax(self.pco2)
        self.sed_pco2min = self.sedmin(self.pco2)
        self.sed_pco2max = self.sedmax(self.pco2)  

        self.ch4min = self.watmin(self.ch4)
        self.ch4max = self.watmax(self.ch4)
        self.sed_ch4min = self.sedmin(self.ch4)
        self.sed_ch4max = self.sedmax(self.ch4)    
        
        self.om_armin = self.watmin(self.om_ar)
        self.om_armax = self.watmax(self.om_ar)
        self.sed_om_armin = self.sedmin(self.om_ar)
        self.sed_om_armax = self.sedmax(self.om_ar)         
        
    def read_fielddata(self):
        values_summer=[]   # create empty matrix for storing data
#        f = None
        try:
            f_summer = open('summer.txt', 'rb')   # Read file with summer water column data 
            while True: 
#                for i in range(0,85):        
                line1 = f_summer.readline()
                if len(line1) == 0:
                    break                
                values_summer.append(line1.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_summer:
                f_summer.close()
            print("(Cleaning up: Read and closed the file Summer)")
        
        data_summer = zip(*values_summer)
        self.depth_summer = data_summer[0][1:]
        self.pH_summer = data_summer[1][1:]
        self.sal_summer = data_summer[2][1:]
        self.na_summer = data_summer[3][1:]
        
        self.so4_summer = data_summer[8][1:]
        self.no3_summer = data_summer[9][1:]
        self.no2_summer = data_summer[10][1:]
        self.nh4_summer = data_summer[11][1:]
        self.si_summer = data_summer[12][1:]
        
        self.po4_summer = data_summer[14][1:]
        
        self.mn_summer = data_summer[15][1:]
        self.fe_summer = data_summer[16][1:]
        self.date_summer = data_summer[17][1:]
        self.sed_depth_summer = data_summer[18][1:]
        self.h2s_summer = data_summer[19][1:]
#        self.si_summer = data_summer[20][1:]        
        
        values_winter=[]   # create empty matrix for storing data
        f_winter = None
        try:
            f_winter = open('winter.txt', 'rb')   
            while True:
#            for i in range(0,61):        
                line_winter = f_winter.readline()
                if len(line_winter) == 0:
                    break
                values_winter.append(line_winter.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_winter:
                f_winter.close()
            print("(Cleaning up: Read and closed the file Winter)")
        
        data_winter = zip(*values_winter)
        
        
        #print values_winter
        self.depth_winter = data_winter[0][1:]
        self.pH_winter = data_winter[1][1:]
        self.sal_winter = data_winter[2][1:]
        self.na_winter = data_winter[3][1:]
        self.so4_winter = data_winter[8][1:]
        self.no3_winter = data_winter[9][1:]
        self.no2_winter = data_winter[10][1:]
        self.nh4_winter = data_winter[11][1:]
        self.si_winter = data_winter[12][1:]
        self.po4_winter = data_winter[14][1:] 
        self.mn_winter = data_winter[15][1:]
        self.fe_winter = data_winter[16][1:]
        self.date_winter = data_winter[17][1:]
        self.sed_depth_winter = data_winter[18][1:]
        self.h2s_winter = data_winter[19][1:]
        


        values_winter_average=[]   # create empty matrix for storing data
        f_winter_average = None
        try:
            f_winter_average = open('winter-average.txt', 'rb')   
            while True:
#            for i in range(0,61):        
                line_winter_average = f_winter_average.readline()
                if len(line_winter_average) == 0:
                    break
                values_winter_average.append(line_winter_average.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_winter_average:
                f_winter_average.close()
            print("(Cleaning up: Read and closed the file winter_average)")
        
        data_winter_average = zip(*values_winter_average)
        
        
        #print values_winter_average
        self.depth_winter_average = data_winter_average[2][1:]
        self.pH_winter_average = data_winter_average[4][1:]
        self.sal_winter_average = data_winter_average[5][1:]
        self.na_winter_average = data_winter_average[6][1:]
        self.so4_winter_average = data_winter_average[11][1:]
        self.h2s_winter_average = data_winter_average[12][1:]        
        self.no3_winter_average = data_winter_average[13][1:]
        self.no2_winter_average = data_winter_average[14][1:]
        self.nh4_winter_average = data_winter_average[15][1:]
        self.si_winter_average = data_winter_average[16][1:]
        self.po4_winter_average = data_winter_average[18][1:] 
        self.mn_winter_average = data_winter_average[19][1:]
        self.fe_winter_average = data_winter_average[20][1:]
#        self.date_winter_average = data_winter_average[17][1:]
        self.sed_depth_winter_average = data_winter_average[3][1:]





















        values_mai=[]   # create empty matrix for storing data
        f_mai = None
        try:
            f_mai = open('mai.txt', 'rb')   
            while True:
#            for i in range(0,61):        
                line_mai = f_mai.readline()
                if len(line_mai) == 0:
                    break
                values_mai.append(line_mai.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_mai:
                f_mai.close()
            print("(Cleaning up: Read and closed the file mai)")
        
        data_mai = zip(*values_mai)
        
        
        #print values_mai
   
        self.depth_mai = data_mai[0][1:]
        self.pH_mai = data_mai[1][1:]
        self.sal_mai = data_mai[2][1:]
        self.na_mai = data_mai[3][1:]
        self.so4_mai = data_mai[8][1:]
        self.no3_mai = data_mai[9][1:]
        self.no2_mai = data_mai[10][1:]
        self.nh4_mai = data_mai[11][1:]
        self.si_mai = data_mai[12][1:]
        self.po4_mai = data_mai[14][1:] 
        self.mn_mai = data_mai[15][1:]
        self.fe_mai = data_mai[16][1:]
        self.co2_mai = data_mai[17][1:]
        self.sed_depth_mai = data_mai[18][1:]     
        self.h2s_mai = data_mai[19][1:]


          
                
        values_o2=[]   # create empty matrix for storing data
#        fo2 = None
        try:
            f_o2 = open('o2.txt', 'rb')   
            while True:
                line_o2 = f_o2.readline()
                if len(line_o2) == 0:
                    break
                values_o2.append(line_o2.split())        
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_o2:
                f_o2.close()
            print("(Cleaning up: Read and closed the file O2)")
        data_o2 = zip(*values_o2)
        self.depth_o2 = data_o2[0][1:]
        self.sed_depth_o2 = data_o2[1][1:]
        self.o2_o2 = data_o2[2][1:]
        

        values_o2_winter=[]   # create empty matrix for storing data
#        fo2_winter = None
        try:
            f_o2_winter = open('o2_winter.txt', 'rb')   
            while True:
                line_o2_winter = f_o2_winter.readline()
                if len(line_o2_winter) == 0:
                    break
                values_o2_winter.append(line_o2_winter.split())        
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_o2_winter:
                f_o2_winter.close()
            print("(Cleaning up: Read and closed the file o2_winter)")
        data_o2_winter = zip(*values_o2_winter)
        self.depth_o2_winter = data_o2_winter[0][1:]
        self.sed_depth_o2_winter = data_o2_winter[1][1:]
        self.o2_winter = data_o2_winter[2][1:]


        values_o2_mai=[]   # create empty matrix for storing data
#        fo2_mai = None
        try:
            f_o2_mai = open('o2_mai.txt', 'rb')   
            while True:
                line_o2_mai = f_o2_mai.readline()
                if len(line_o2_mai) == 0:
                    break
                values_o2_mai.append(line_o2_mai.split())        
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_o2_mai:
                f_o2_mai.close()
            print("(Cleaning up: Read and closed the file o2_mai)")
        data_o2_mai = zip(*values_o2_mai)
        self.depth_o2_mai = data_o2_mai[0][1:]
        self.sed_depth_o2_mai = data_o2_mai[1][1:]
        self.o2_mai = data_o2_mai[2][1:]
        
        self.depth_o2_mai2 = data_o2_mai[3][1:]
        self.sed_depth_o2_mai2 = data_o2_mai[4][1:]
        self.o2_mai2 = data_o2_mai[5][1:]        
        
        
        self.depth_o2_mai3 = data_o2_mai[6][1:]
        self.sed_depth_o2_mai3 = data_o2_mai[7][1:]
        self.o2_mai3 = data_o2_mai[8][1:]         
        
        
        
        values_pH=[]   # create empty matrix for storing data
        #fpH = None
        try:
            f_pH = open('pH.txt', 'rb')   
            while True:
                line_pH = f_pH.readline()
                if len(line_pH) == 0:
                    break
                values_pH.append(line_pH.split())        
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_pH:
                f_pH.close()
            print("(Cleaning up: Read and closed the file pH)")
        data_pH = zip(*values_pH)
        self.depth_pH = data_pH[0][1:]
        self.sed_depth_pH = data_pH[1][1:]
        self.pH_pH = data_pH[2][1:]
        
        
        values_pH_winter=[]   # create empty matrix for storing data
        #fpH = None
        try:
            f_pH_winter = open('pH_winter.txt', 'rb')   
            while True:
                line_pH_winter = f_pH_winter.readline()
                if len(line_pH_winter) == 0:
                    break
                values_pH_winter.append(line_pH_winter.split())        
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_pH_winter:
                f_pH_winter.close()
            print("(Cleaning up: Read and closed the file pH_winter)")
            
        data_pH_winter = zip(*values_pH_winter)
        self.depth_pH_winter = data_pH_winter[0][1:]
        self.sed_depth_pH_winter = data_pH_winter[1][1:]
        self.pH_pH_winter = data_pH_winter[2][1:]





#        values_mnfe=[]   # create empty matrix for storing data
#        f_mnfe = None
#       try:
#            f_mnfe = open('mnfe_summer.txt', 'rb')   
#            while True:
#            for i in range(0,61):        
#                line_mnfe = f_mnfe.readline()
#                if len(line_mnfe) == 0:
#                    break
#                values_mnfe.append(line_mnfe.split())
#          
#        except  IOError:
#            print("Could not find a file.")
#        except  KeyboardInterrupt:
#            print("!! You cancelled the reading from the file.")
#        finally:
#            if  f_mnfe:
#                f_mnfe.close()
#            print("(Cleaning up: Read and closed the file mnfe)")
        
#        data_mnfe_summer = zip(*values_mnfe)
        
        
        #print values_mnfe
   
#        self.depth_mnfe_summer = data_mnfe_summer[0][1:]
#        self.mn_mnfe_summer = data_mnfe_summer[1][1:]
#        self.fe_mnfe_summer = data_mnfe_summer[2][1:]
#        self.sed_depth_mnfe_summer = data_mnfe_summer[3][1:]#

#        self.depth_mnfe_summer = data_mnfe_summer[4][1:]
#        self.mn_mnfe_summer = data_mnfe_summer[5][1:]
#        self.fe_mnfe_summer = data_mnfe_summer[6][1:]
#        self.sed_depth_mnfe_summer = data_mnfe_summer[7][1:]
        
#        self.depth_mnfe_summer = data_mnfe_summer[8][1:]
#        self.mn_mnfe_summer = data_mnfe_summer[9][1:]
#        self.fe_mnfe_summer = data_mnfe_summer[10][1:]
#        self.sed_depth_mnfe_summer = data_mnfe_summer[11][1:]        
#        
#        self.depth_mnfe_summer = data_mnfe_summer[12][1:]
#        self.mn_mnfe_summer = data_mnfe_summer[13][1:]
#        self.fe_mnfe_summer = data_mnfe_summer[14][1:]
#        self.sed_depth_mnfe_summer = data_mnfe_summer[15][1:]     






        
        #############
        values_mnfe_summer=[]   # create empty matrix for storing data
        #f1 = None
        try:
            f_mnfe_summer = open('mnfe_summer.txt', 'rb')   # Read file with summer water column data 
            for i in range(0,17):        
                line1 = f_mnfe_summer.readline()
                values_mnfe_summer.append(line1.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_mnfe_summer:
                f_mnfe_summer.close()
            print("(Cleaning up: Read and closed the file Summer)")
        
        data_mnfe_summer = zip(*values_mnfe_summer)
        
        self.depth_mnfe_summer = data_mnfe_summer[0][1:]
        self.mn_mnfe_summer = data_mnfe_summer[1][1:]
        self.fe_mnfe_summer = data_mnfe_summer[2][1:]
        self.sed_depth_mnfe_summer = data_mnfe_summer[3][1:]

        self.depth1_mnfe_summer = data_mnfe_summer[4][1:]
        self.mn1_mnfe_summer = data_mnfe_summer[5][1:]
        self.fe1_mnfe_summer = data_mnfe_summer[6][1:]
        self.sed_depth1_mnfe_summer = data_mnfe_summer[7][1:]
        
        self.depth2_mnfe_summer = data_mnfe_summer[8][1:]
        self.mn2_mnfe_summer = data_mnfe_summer[9][1:]
        self.fe2_mnfe_summer = data_mnfe_summer[10][1:]
        self.sed_depth2_mnfe_summer = data_mnfe_summer[11][1:]        
        
        self.depth3_mnfe_summer = data_mnfe_summer[12][1:]
        self.mn3_mnfe_summer = data_mnfe_summer[13][1:]
        self.fe3_mnfe_summer = data_mnfe_summer[14][1:]
        self.sed_depth3_mnfe_summer = data_mnfe_summer[15][1:] 
        
        self.depth4_mnfe_summer = data_mnfe_summer[16][1:]
        self.mn4_mnfe_summer = data_mnfe_summer[17][1:]
        self.fe4_mnfe_summer = data_mnfe_summer[18][1:]
        self.sed_depth4_mnfe_summer = data_mnfe_summer[19][1:]         
        values_mnfe_winter=[]   # create empty matrix for storing data
        #f1 = None
        try:
            f_mnfe_winter = open('mnfe_winter.txt', 'rb')   # Read file with summer water column data 
            for i in range(0,13):        
                line1 = f_mnfe_winter.readline()
                values_mnfe_winter.append(line1.split())
          
        except  IOError:
            print("Could not find a file.")
        except  KeyboardInterrupt:
            print("!! You cancelled the reading from the file.")
        finally:
            if  f_mnfe_winter:
                f_mnfe_winter.close()
            print("(Cleaning up: Read and closed the file mnfe winter)")
        
        data_mnfe_winter = zip(*values_mnfe_winter)
        
        self.mn1_mnfe_winter = data_mnfe_winter[0][1:]
        self.fe1_mnfe_winter = data_mnfe_winter[1][1:]
        self.sed_depth1_mnfe_winter = data_mnfe_winter[2][1:]
        self.mn2_mnfe_winter = data_mnfe_winter[3][1:]
        self.fe2_mnfe_winter = data_mnfe_winter[4][1:]
        self.sed_depth2_mnfe_winter = data_mnfe_winter[5][1:]
        self.mn3_mnfe_winter = data_mnfe_winter[6][1:]
        self.fe3_mnfe_winter = data_mnfe_winter[7][1:]
        self.sed_depth3_mnfe_winter = data_mnfe_winter[8][1:]
        self.mn4_mnfe_winter = data_mnfe_winter[9][1:]
        self.fe4_mnfe_winter = data_mnfe_winter[10][1:]
        self.sed_depth4_mnfe_winter = data_mnfe_winter[11][1:]
        self.mn5_mnfe_winter = data_mnfe_winter[12][1:]
        self.fe5_mnfe_winter = data_mnfe_winter[13][1:]
        self.sed_depth5_mnfe_winter = data_mnfe_winter[14][1:]
        self.mn6_mnfe_winter = data_mnfe_winter[15][1:]
        self.fe6_mnfe_winter = data_mnfe_winter[16][1:]
        self.sed_depth6_mnfe_winter = data_mnfe_winter[17][1:] 
        
        
                                                                                             
    def plot1(self): #function to define 1 figure PO4,SO4,o2
        plt.clf() #clear figure before updating 
        gs = gridspec.GridSpec(3, 3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)   
        self.figure.patch.set_facecolor(self.background)  #Set the background color

        
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water         
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        
        self.ax01 = self.figure.add_subplot(gs[3])        
        self.ax11 = self.figure.add_subplot(gs[4])
        self.ax21 = self.figure.add_subplot(gs[5])  
             
        self.ax02 = self.figure.add_subplot(gs[6]) #sediment
        self.ax12 = self.figure.add_subplot(gs[7])
        self.ax22 = self.figure.add_subplot(gs[8])
        
#        self.ax00.plot(self.po4[50],self.depth,'b',linewidth=0.7)#self.winter,   
#        self.ax01.plot(self.po4[50],self.depth,linewidth=0.7)  
#        self.ax02.plot(self.po4[50],self.depth_sed,linewidth=0.7) 
       
#        for axis in (self.ax00, self.ax01):   
#            axis.set_xlim([0,self.po4max])#self.po4min
#            axis.set_xticks(np.arange(np.round(po4min),np.ceil(po4max)),((np.ceil(po4max)-np.round(po4min))/2))
#        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22): 
#            axis.xaxis.set_label_position('top')
#            axis.xaxis.tick_top()            

#        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22): 
#            axis.xaxis.set_label_position('top')
#            axis.xaxis.tick_top()
#            ax20.set_xticks(np.arange(0,2*kzmax),kzmax)     
             
        for axis in (self.ax00, self.ax01): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()                           
            axis.set_xlim([self.po4min,self.po4max])
#            axis.set_xticks(np.arange(np.round(self.po4min),np.ceil(self.po4max)),
#                            ((np.ceil(self.po4max)-np.round(self.po4min))/2))
            self.ax02.xaxis.tick_top() 
            self.ax02.set_xlim([self.sed_po4min,self.sed_po4max])    
            
        for axis in (self.ax10, self.ax11):

 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()                        
#            watmin = min(15000,so4min)#so4_lastmin
            axis.set_xlim([self.so4min,self.so4max])
            axis.set_xticks(np.arange(self.so4min,self.so4max+((self.so4max-self.so4min)/2.),((self.so4max-self.so4min)/2.)))             
            self.ax12.xaxis.tick_top() 
            self.ax12.set_xlim([self.sed_so4min,self.sed_so4max])    
            self.ax12.set_xticks(np.arange(self.sed_so4min,self.sed_so4max+((self.sed_so4max-self.sed_so4min)/2.),
                                      ((self.sed_so4max-self.sed_so4min)/2.)))              
        for axis in (self.ax20, self.ax21):              
                      
            axis.xaxis.set_label_position('top')  
            axis.xaxis.tick_top()                      
            axis.set_xlim([self.o2min,self.o2max])
            self.ax22.xaxis.tick_top()             
            self.ax22.set_xlim([self.sed_o2min,self.sed_o2max]) 
#            axis.set_xticks(np.arange(o2min,0.75,0.25)) 
           
        for n in range(0,365):  
            if n >= 0 and n<=21:#n <= 18:      #Winter                                 
                self.ax00.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.po4[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.so4[n],self.depth_sed,self.winter,linewidth=0.7) 
                self.ax20.plot(self.o2[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.o2[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.o2[n],self.depth_sed,self.winter,linewidth=0.7)                

                
            elif n >= 22 and n <= 60:      #Winter                                 
                self.ax00.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.po4[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.so4[n],self.depth_sed,self.winter,linewidth=0.7) 
              
                self.ax20.plot(self.o2[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.o2[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.o2[n],self.depth_sed,self.winter,linewidth=0.7) 
                                
#            elif n>=19 and n<=21: #winter to compare with field data
#                ax00.plot(po4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)             
#                ax01.plot(po4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)  
#                ax02.plot(po4[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=8)                 
#                ax10.plot(so4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax11.plot(so4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax12.plot(so4[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
#                ax20.plot(o2[n],depth,self.winter,linewidth=0.7) 
#                ax21.plot(o2[n],depth,self.winter,linewidth=0.7)  #
#                ax22.plot(o2[n],depth_sed,self.winter,linewidth=0.7)                   
                
            elif n >= 335 and n <365: #
                self.ax00.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.po4[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.po4[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.so4[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.so4[n],self.depth_sed,self.winter,linewidth=0.7) 
               
                self.ax20.plot(self.o2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax21.plot(self.o2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                self.ax22.plot(self.o2[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                             
            elif n >= 150 and n < 240:#n < 236: #self.summer                 
                self.ax00.plot(self.po4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                self.ax01.plot(self.po4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                self.ax02.plot(self.po4[n],self.depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                self.ax10.plot(self.so4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax11.plot(self.so4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax12.plot(self.so4[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
###O2  
                self.ax20.plot(self.o2[n],self.depth,self.summer,linewidth=self.linewidth)   
                self.ax21.plot(self.o2[n],self.depth,self.summer,linewidth=self.linewidth)   #marker='o',
                self.ax22.plot(self.o2[n],self.depth_sed,self.summer,linewidth=self.linewidth) #marker='o',           
                
#            elif n >= 236 and n < 240: #from 25 to 30 august               
#                ax00.plot(po4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
#                ax01.plot(po4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
#                ax02.plot(po4[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(so4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(so4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(so4[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
#                ax20.plot(o2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax21.plot(o2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax22.plot(o2[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
             
            else:   #Spring and autumn

                self.ax00.plot(self.po4[n],self.depth,self.spring_autumn, linewidth=0.7, alpha = 0.5)             
                self.ax01.plot(self.po4[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)  
                self.ax02.plot(self.po4[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)                 
                self.ax10.plot(self.so4[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                self.ax11.plot(self.so4[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                self.ax12.plot(self.so4[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)   

                self.ax20.plot(self.o2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 
                self.ax21.plot(self.o2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  #
                self.ax22.plot(self.o2[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)         
             
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22):            
            self.y_lim(axis) 
            
                  
        #self.y_lim(self.ax00)
 
#        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Sediment 
#        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
#        transform=ax22.transAxes)

        #plt.text(1.1, 0.4,'(Test{0})'.format(self.depth2))
        
                
        
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=self.ax20.transAxes) 
        
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=self.ax21.transAxes)
        
        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to BBL
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=self.ax21.transAxes)
                                 
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to BBL
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=self.ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Sediment 
        bbox={'facecolor': self.sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=self.ax22.transAxes) 
        
        self.ax00.set_xlabel(r'$\rm PO _4 $',fontsize=14, fontweight='bold') 
        self.ax10.set_xlabel(r'$\rm SO _4 $',fontsize=14)   
        self.ax20.set_xlabel(r'$\rm O _2 $',fontsize=14)                                                                                                           
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)        
        
         
         
        self.canvas.draw()


                         
    def plot1_field(self): # function to plot PO4,SO4,O2 field data




        self.ax00.plot(self.po4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax01.plot(self.po4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax02.plot(self.po4_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)  
        self.ax10.plot(self.so4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax11.plot(self.so4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax12.plot(self.so4_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)               
#        self.read_fielddata()
        
        self.ax00.scatter(self.po4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax10.scatter(self.so4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 

        self.ax01.scatter(self.po4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax11.scatter(self.so4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
                
        self.ax02.scatter(self.po4_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        self.ax12.scatter(self.so4_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)    
       
        self.ax00.scatter(self.po4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax10.scatter(self.so4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
                    
        self.ax01.scatter(self.po4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        self.ax11.scatter(self.so4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         

        self.ax02.scatter(self.po4_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        self.ax12.scatter(self.so4_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)    
             
#        self.ax00.scatter(self.po4_winter_average,self.depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax01.scatter(self.po4_winter_average,self.depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax02.scatter(self.po4_winter_average,self.sed_depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)     
#        self.ax10.scatter(self.so4_winter_average,self.depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax11.scatter(self.so4_winter_average,self.depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax12.scatter(self.so4_winter_average,self.sed_depth_winter_average,color='b' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)  
#        self.ax20.scatter(self.o2_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax21.scatter(self.o2_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax22.scatter(self.o2_winter_average,self.sed_depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)          

       
        self.ax00.scatter(self.po4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax10.scatter(self.so4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
                    
        self.ax01.scatter(self.po4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        self.ax11.scatter(self.so4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         

        self.ax02.scatter(self.po4_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        self.ax12.scatter(self.so4_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  


         
        self.ax20.scatter(self.o2_o2,self.depth_o2,color='r' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax21.scatter(self.o2_o2,self.depth_o2,color='r' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax22.scatter(self.o2_o2,self.sed_depth_o2,color='r' ,alpha=1,edgecolor='#262626',
                     s = 5 ,linewidth=0.1,zorder=10)         

        self.ax20.scatter(self.o2_winter,self.depth_o2_winter,color='b' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax21.scatter(self.o2_winter,self.depth_o2_winter,color='b' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax22.scatter(self.o2_winter,self.sed_depth_o2_winter,color='b' ,alpha=0.5,edgecolor='#262626',
                     s = 5 ,linewidth=0.1,zorder=10)         

        self.ax20.scatter(self.o2_mai,self.depth_o2_mai,color='g' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax21.scatter(self.o2_mai,self.depth_o2_mai,color='g' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax22.scatter(self.o2_mai,self.sed_depth_o2_mai,color='g' ,alpha=0.5,edgecolor='#262626',
                     s = 5 ,linewidth=0.1,zorder=10) 

        self.ax20.scatter(self.o2_mai2,self.depth_o2_mai2,color='g' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax21.scatter(self.o2_mai2,self.depth_o2_mai2,color='g' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        self.ax22.scatter(self.o2_mai2,self.sed_depth_o2_mai2,color='g' ,alpha=0.5,edgecolor='#262626',
                     s = 5 ,linewidth=0.1,zorder=10) 

#        self.ax20.scatter(self.o2_mai3,self.depth_o2_mai3,color='g' , alpha=0.5,edgecolor='#262626',
#                     s = 5,linewidth=0.1,zorder=10) 
#        self.ax21.scatter(self.o2_mai3,self.depth_o2_mai3,color='g' , alpha=0.5,edgecolor='#262626',
#                     s = 5,linewidth=0.1,zorder=10) 
#        self.ax22.scatter(self.o2_mai3,self.sed_depth_o2_mai3,color='g' ,alpha=0.5,edgecolor='#262626',
#                     s = 5 ,linewidth=0.1,zorder=10) 



                                  
        self.canvas.draw()
        
           
    def plot2(self): # function to define 2 figure T,S,Kz  
        plt.clf() #clear figure before updating         
        gs = gridspec.GridSpec(3, 3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        
        self.ax01 = self.figure.add_subplot(gs[3])        
        self.ax11 = self.figure.add_subplot(gs[4])
        self.ax21 = self.figure.add_subplot(gs[5])  
             
        self.ax02 = self.figure.add_subplot(gs[6]) #sediment
        self.ax12 = self.figure.add_subplot(gs[7])
        self.ax22 = self.figure.add_subplot(gs[8])
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)   
                    
               

        self.ax00.set_xlabel('Temperature',fontsize=14) 
        self.ax10.set_xlabel('Salinity',fontsize=14)   
        self.ax20.set_xlabel('Kz',fontsize=14)                                                                                                           
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                
                                                             
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (self.ax00, self.ax01, self.ax02):              
            axis.set_xlim([self.tempmin,self.tempmax])
#            axis.set_xticks(np.arange(np.round(self.tempmin),np.ceil(self.tempmax)),((np.ceil(self.tempmax)-np.round(self.tempmin))/2))

        for axis in (self.ax10, self.ax11, self.ax12):              
            axis.set_xlim([self.salmin,self.salmax]) 
                       
        for axis in (self.ax20, self.ax21, self.ax22):             
            axis.set_xlim([self.kzmin,self.kzmax])
            axis.set_xticks(np.arange(0,(round(self.kzmax+(self.kzmax/2.),5)),self.kzmax/2.))   
#            axis.set_xticks(np.arange(kzmin,0.75,0.25))          
              
                             
        for n in range(0,365):  
            if n >= 0 and n <= 21: #18:      #Winter                                 
                self.ax00.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.temp[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.sal[n],self.depth_sed,self.winter,linewidth=0.7)     
                self.ax20.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7) 
                self.ax21.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.kz[n],self.depth_sed2,self.winter,linewidth=0.7)
            elif n >= 22 and n <= 60:      #Winter                                 
                self.ax00.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.temp[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.sal[n],self.depth_sed,self.winter,linewidth=0.7)     
                self.ax20.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7) 
                self.ax21.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.kz[n],self.depth_sed2,self.winter,linewidth=0.7)                
                
#            elif n>=19 and n<=21: #winter to compare with field data
#                ax00.plot(temp[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)             
#                ax01.plot(temp[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)  
#                ax02.plot(temp[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=8)                 
#                ax10.plot(sal[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax11.plot(sal[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax12.plot(sal[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
#                ax20.plot(kz[n],depth2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax21.plot(kz[n],depth2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   #marker='o',
#                ax22.plot(kz[n],depth_sed2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8) #marker='o',                   
                
                
            elif n >= 335 and n <365: #
                self.ax00.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.temp[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.temp[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.sal[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.sal[n],self.depth_sed,self.winter,linewidth=0.7) 
                
                self.ax20.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7) 
                self.ax21.plot(self.kz[n],self.depth2,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.kz[n],self.depth_sed2,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 249: #236: #self.summer                 
                self.ax00.plot(self.temp[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                self.ax01.plot(self.temp[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                self.ax02.plot(self.temp[n],self.depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                self.ax10.plot(self.sal[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax11.plot(self.sal[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax12.plot(self.sal[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax20.plot(self.kz[n],self.depth2,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax21.plot(self.kz[n],self.depth2,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                self.ax22.plot(self.kz[n],self.depth_sed2,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
#            elif n >= 236 and n < 240: #from 25 to 30 august ( to compare with field data)                
#                ax00.plot(temp[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--', zorder=9) #marker='o',     
#                ax01.plot(temp[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  #marker='o',
#                ax02.plot(temp[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(sal[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(sal[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(sal[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
#                ax20.plot(kz[n],depth2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax21.plot(kz[n],depth2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax22.plot(kz[n],depth_sed2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9) 
               
            else:   #Spring and autumn
                self.ax00.plot(self.temp[n],self.depth,self.spring_autumn, linewidth=0.7, alpha = self.alpha_autumn)             
                self.ax01.plot(self.temp[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  
                self.ax02.plot(self.temp[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)                 
                self.ax10.plot(self.sal[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   
                self.ax11.plot(self.sal[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   
                self.ax12.plot(self.sal[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   
                self.ax20.plot(self.kz[n],self.depth2,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 
                self.ax21.plot(self.kz[n],self.depth2,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  #
                self.ax22.plot(self.kz[n],self.depth_sed2,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 
                
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22):            
            self.y_lim(axis) 
                                
        self.canvas.draw()
   
    def plot2_field(self):
        
#        self.read_fielddata()  
              
        self.ax10.scatter(self.sal_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        self.ax10.scatter(self.sal_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        self.ax11.scatter(self.sal_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax11.scatter(self.sal_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        self.ax12.scatter(self.sal_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        self.ax12.scatter(self.sal_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        
        self.canvas.draw()
        
    def plot3(self): #function to define 1 figure NO2,NO3,NH4
        plt.clf() #clear figure before updating 
        gs = gridspec.GridSpec(3, 3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        
        self.ax01 = self.figure.add_subplot(gs[3])        
        self.ax11 = self.figure.add_subplot(gs[4])
        self.ax21 = self.figure.add_subplot(gs[5])  
             
        self.ax02 = self.figure.add_subplot(gs[6]) #sediment
        self.ax12 = self.figure.add_subplot(gs[7])
        self.ax22 = self.figure.add_subplot(gs[8])

             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)        
                            
              

        self.ax00.set_xlabel(r'$\rm NO _2 $',fontsize=14, fontweight='bold') 
        self.ax10.set_xlabel(r'$\rm NO _3 $',fontsize=14)   
        self.ax20.set_xlabel(r'$\rm NH _4 $',fontsize=14)                                                                                                           
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                
                                     

                        
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (self.ax00, self.ax01):

            axis.set_xlim([self.no2min,self.no2max])
            axis.set_xticks(np.arange(np.round(self.no2min),np.ceil(self.no2max)),
                            ((np.ceil(self.no2max)-np.round(self.no2min))/2))
        self.ax02.set_xlim([self.sed_no2min,self.sed_no2max])    
        for axis in (self.ax10, self.ax11):           

            axis.set_xlim([self.no3min,self.no3max])
        self.ax12.set_xlim([self.sed_no3min,self.sed_no3max])    
            
        for axis in (self.ax20, self.ax21):               
            axis.set_xlim([self.nh4min,self.nh4max])
        self.ax22.set_xlim([self.sed_nh4min,self.sed_nh4max]) 
#            axis.set_xticks(np.arange(nh4min,0.75,0.25))          
    

                        
        for n in range(0,365):  
            if n >= 0 and n <= 21: #18:      #Winter                                 
                self.ax00.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.no2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.no3[n],self.depth_sed,self.winter,linewidth=0.7)         
                self.ax20.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.nh4[n],self.depth_sed,self.winter,linewidth=0.7)
                
            elif n >= 22 and n <= 60:      #Winter                                 
                self.ax00.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.no2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.no3[n],self.depth_sed,self.winter,linewidth=0.7)         
                self.ax20.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.nh4[n],self.depth_sed,self.winter,linewidth=0.7)                
                
                
#            elif n>=19 and n<=21: #winter to compare with field data
#                ax00.plot(no2[n],depth,'#4e9dda',linewidth=3,alpha = 0.5,linestyle= '--',zorder=5)             
#                ax01.plot(no2[n],depth,'#4e9dda',linewidth=3,alpha = 0.5,linestyle= '--',zorder=5)  
#                ax02.plot(no2[n],depth_sed,'#4e9dda',linewidth=3, alpha = 0.5,linestyle= '--',zorder=5)                 
#                ax10.plot(no3[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax11.plot(no3[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax12.plot(no3[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
#                ax20.plot(nh4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
#                ax21.plot(nh4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   #marker='o',
#                ax22.plot(nh4[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8) #marker='o',                   
                
                
     
            elif n >= 335 and n <365: #
                self.ax00.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.no2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.no2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.no3[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.no3[n],self.depth_sed,self.winter,linewidth=0.7) 
                
                self.ax20.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.nh4[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.nh4[n],self.depth_sed,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 240: #236: #self.summer                 
                self.ax00.plot(self.no2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                self.ax01.plot(self.no2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                self.ax02.plot(self.no2[n],self.depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                self.ax10.plot(self.no3[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax11.plot(self.no3[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax12.plot(self.no3[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax20.plot(self.nh4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax21.plot(self.nh4[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                self.ax22.plot(self.nh4[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
#            elif n >= 236 and n < 240: #from 25 to 30 august               
#                ax00.plot(no2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
#                ax01.plot(no2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
#                ax02.plot(no2[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(no3[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(no3[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(no3[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
#                ax20.plot(nh4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax21.plot(nh4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax22.plot(nh4[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                                  
                         
            else:   #Spring and autumn

                self.ax00.plot(self.no2[n],self.depth,self.spring_autumn, linewidth=0.7, alpha = self.alpha_autumn)             
                self.ax01.plot(self.no2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  
                self.ax02.plot(self.no2[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)                 
                self.ax10.plot(self.no3[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  
                 
                self.ax11.plot(self.no3[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   
                self.ax12.plot(self.no3[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   

                self.ax20.plot(self.nh4[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 
                self.ax21.plot(self.nh4[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  #
                self.ax22.plot(self.nh4[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 

        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22):            
            self.y_lim(axis) 
                                                    
        self.canvas.draw()   
    def plot3_field(self): #NO2,NO3,NH4  

        self.ax00.plot(self.no2_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax01.plot(self.no2_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax02.plot(self.no2_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)  
        self.ax10.plot(self.no3_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax11.plot(self.no3_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax12.plot(self.no3_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5) 
        self.ax20.plot(self.nh4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax21.plot(self.nh4_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax22.plot(self.nh4_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5) 
        
        self.ax00.scatter(self.no2_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax00.scatter(self.no2_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        self.ax00.scatter(self.no2_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
                     
        self.ax01.scatter(self.no2_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax01.scatter(self.no2_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax01.scatter(self.no2_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
                                                    
        self.ax02.scatter(self.no2_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)     
        self.ax02.scatter(self.no2_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax02.scatter(self.no2_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        
                           
        self.ax10.scatter(self.no3_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax10.scatter(self.no3_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        self.ax10.scatter(self.no3_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)            
        
        self.ax11.scatter(self.no3_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax11.scatter(self.no3_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax11.scatter(self.no3_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
                          
        self.ax12.scatter(self.no3_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)      
        self.ax12.scatter(self.no3_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax12.scatter(self.no3_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        
                                         
        self.ax20.scatter(self.nh4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax20.scatter(self.nh4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax20.scatter(self.nh4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                
        self.ax21.scatter(self.nh4_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax21.scatter(self.nh4_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax21.scatter(self.nh4_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)          
               
        self.ax22.scatter(self.nh4_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax22.scatter(self.nh4_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)     
        self.ax22.scatter(self.nh4_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)           
        
        self.canvas.draw()    
    def plot4(self): #function to define 1 figure Si,pH
        plt.clf() #clear figure before updating 

#        alpha_autumn = 0.5
        gs = gridspec.GridSpec(3, 2) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
#        ax20 = self.figure.add_subplot(gs[2])
        
        self.ax01 = self.figure.add_subplot(gs[2])        
        self.ax11 = self.figure.add_subplot(gs[3])
#        ax21 = self.figure.add_subplot(gs[5])  
             
        self.ax02 = self.figure.add_subplot(gs[4]) #sediment
        self.ax12 = self.figure.add_subplot(gs[5])
#        ax22 = self.figure.add_subplot(gs[8])
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax10.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax11.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax11.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax12.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax12.transAxes)  
                             
        self.ax00.set_xlabel(r'$\rm Si $',fontsize=14, fontweight='bold') 
        self.ax10.set_xlabel(r'$\rm pH $',fontsize=14)   
#        ax20.set_xlabel(r'$\rm NH _4 $',fontsize=14)                                                                                                           
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                
            
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (self.ax00, self.ax01): 
            axis.set_xlim([self.simin,self.simax])
        self.ax02.set_xlim([self.sed_simin,self.sed_simax])  
          
        for axis in (self.ax10, self.ax11):
            axis.set_xlim([self.phmin,self.phmax])        
        self.ax12.set_xlim([self.sed_phmin,self.sed_phmax])    
                   

# Plot Field data        

                    
        for n in range(0,365):  
            if n >= 0 and n <= 21: #18:      #Winter                                 
                self.ax00.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)             
                self.ax01.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)  
                self.ax02.plot(self.si[n],self.depth_sed,self.winter,linewidth=self.linewidth)                 
                self.ax10.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax11.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax12.plot(self.ph[n],self.depth_sed,self.winter,linewidth=self.linewidth) 
                
            if n >= 22 and n <= 60:      #Winter                                 
                self.ax00.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)             
                self.ax01.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)  
                self.ax02.plot(self.si[n],self.depth_sed,self.winter,linewidth=self.linewidth)                 
                self.ax10.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax11.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax12.plot(self.ph[n],self.depth_sed,self.winter,linewidth=self.linewidth) 

#            elif n>=19 and n<=21: #winter to compare with field data
#                ax00.plot(si[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
#                ax01.plot(si[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
#                ax02.plot(si[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(ph[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(ph[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(ph[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)       

                
            elif n >= 335 and n <365: ##Winter 
                self.ax00.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)             
                self.ax01.plot(self.si[n],self.depth,self.winter,linewidth=self.linewidth)  
                self.ax02.plot(self.si[n],self.depth_sed,self.winter,linewidth=self.linewidth)                 
                self.ax10.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax11.plot(self.ph[n],self.depth,self.winter,linewidth=self.linewidth)   
                self.ax12.plot(self.ph[n],self.depth_sed,self.winter,linewidth=self.linewidth) 
                
                             
            elif n >= 150 and n < 240:#236: #self.summer                 
                self.ax00.plot(self.si[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                self.ax01.plot(self.si[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                self.ax02.plot(self.si[n],self.depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                self.ax10.plot(self.ph[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax11.plot(self.ph[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax12.plot(self.ph[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                
#            elif n >= 236 and n < 240: #from 25 to 30 august               
#                ax00.plot(si[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
#                ax01.plot(si[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
#                ax02.plot(si[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(ph[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(ph[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(ph[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                              

            else:   #Spring and autumn

                self.ax00.plot(self.si[n],self.depth,self.spring_autumn, linewidth=self.linewidth, alpha = self.alpha_autumn)             
                self.ax01.plot(self.si[n],self.depth,self.spring_autumn,linewidth=self.linewidth, alpha = self.alpha_autumn)  
                self.ax02.plot(self.si[n],self.depth_sed,self.spring_autumn,linewidth=self.linewidth, alpha = self.alpha_autumn)                 
                self.ax10.plot(self.ph[n],self.depth,self.spring_autumn,linewidth=self.linewidth, alpha = self.alpha_autumn)   
                self.ax11.plot(self.ph[n],self.depth,self.spring_autumn,linewidth=self.linewidth, alpha = self.alpha_autumn)   
                self.ax12.plot(self.ph[n],self.depth_sed,self.spring_autumn,linewidth=self.linewidth, alpha = self.alpha_autumn)
      
                          
        for axis in  (self.ax00,self.ax10):   #water          
            axis.set_ylim([self.y2min, 0])
#            axis.fill_between(self.xticks, self.y1max, self.y1min, facecolor= self.wat_color, alpha=self.alpha_wat)
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')   
        for axis in (self.ax01,self.ax11):  #BBL
            axis.set_ylim([self.y2max, self.y2min])
#            axis.fill_between(self.xticks, self.y2max_fill_water, self.y2min, facecolor= self.wat_color, alpha=self.alpha_wat) 
            axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl, facecolor= self.bbl_color, alpha=self.alpha_bbl)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')   
            axis.xaxis.grid(True,'major')    
            plt.setp(axis.get_xticklabels(), visible=False)                                           
        for axis in (self.ax02,self.ax12): #sediment 
            axis.set_ylim([self.ysedmax, self.ysedmin])   #[y3max, y3min]   
            axis.fill_between(self.xticks, self.ysedmax_fill_bbl, self.ysedmin, facecolor= self.bbl_color, alpha=self.alpha_bbl)  
            axis.fill_between(self.xticks, self.ysedmax, self.ysedmin_fill_sed, facecolor= self.sed_color, alpha=self.alpha_sed)    
            axis.yaxis.set_major_locator(majorLocator)   #define yticks
            axis.yaxis.set_major_formatter(majorFormatter)
            axis.yaxis.set_minor_locator(minorLocator)
            axis.yaxis.grid(True,'minor')
            axis.yaxis.grid(True,'major')
            axis.xaxis.grid(True,'major')
                       
                      
        self.canvas.draw()
    def plot4_field(self):   # Si,pH
        

        self.ax00.plot(self.si_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax01.plot(self.si_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax02.plot(self.si_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)  
        self.ax10.plot(self.pH_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax11.plot(self.pH_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax12.plot(self.pH_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5) 


        
        self.ax00.scatter(self.si_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        self.ax01.scatter(self.si_summer,self.depth_summer,color='r' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax02.scatter(self.si_summer,self.sed_depth_summer,color='r' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)     

        self.ax00.scatter(self.si_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        self.ax01.scatter(self.si_mai,self.depth_mai,color='g' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax02.scatter(self.si_mai,self.sed_depth_mai,color='g' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        
        self.ax00.scatter(self.si_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        self.ax01.scatter(self.si_winter,self.depth_winter,color='b' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)          
        self.ax02.scatter(self.si_winter,self.sed_depth_winter,color='b' , alpha=0.5,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)          
        
           
        self.ax10.scatter(self.pH_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)
        self.ax11.scatter(self.pH_summer,self.depth_summer,color='r' , alpha=0.5,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)            
        self.ax12.scatter(self.pH_summer,self.sed_depth_summer,color='r' , alpha = 0.5,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        
        self.ax10.scatter(self.pH_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)
        self.ax11.scatter(self.pH_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)            
        self.ax12.scatter(self.pH_mai,self.sed_depth_mai,color='g' , alpha = 1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)                 
        
        self.ax10.scatter(self.pH_pH,self.depth_pH,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)   
        self.ax11.scatter(self.pH_pH,self.depth_pH,color='r' , alpha=0.5,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        self.ax12.scatter(self.pH_pH,self.sed_depth_pH,color='r' , alpha = 1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        
                        
        self.ax10.scatter(self.pH_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)                    
        self.ax11.scatter(self.pH_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)            
        self.ax12.scatter(self.pH_winter,self.sed_depth_winter,color='b' , alpha = 0.5,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)         

        self.ax10.scatter(self.pH_pH_winter,self.depth_pH_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10)  
        self.ax11.scatter(self.pH_pH_winter,self.depth_pH_winter,color='b' , alpha=0.5,edgecolor='#262626',
                     s = 5,linewidth=0.05,zorder=10)    
        self.ax12.scatter(self.pH_pH_winter,self.sed_depth_pH_winter,color='b' , alpha = 0.5,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        
        self.canvas.draw()    
    def plot5(self): #function to define Mn,fe,h2s

        plt.clf() #clear figure before updating 
        gs = gridspec.GridSpec(3, 3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        
        self.ax01 = self.figure.add_subplot(gs[3])        
        self.ax11 = self.figure.add_subplot(gs[4])
        self.ax21 = self.figure.add_subplot(gs[5])  
             
        self.ax02 = self.figure.add_subplot(gs[6]) #sediment
        self.ax12 = self.figure.add_subplot(gs[7])
        self.ax22 = self.figure.add_subplot(gs[8])
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax22.transAxes)   
                                    

        self.ax00.set_xlabel(r'$\rm Mn $',fontsize=14, fontweight='bold') 
        self.ax10.set_xlabel(r'$\rm Fe $',fontsize=14)   
        self.ax20.set_xlabel(r'$\rm H _2 S $',fontsize=14)                                                                                                           
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                
            

                        
        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (self.ax00, self.ax01): 

            axis.set_xlim([self.mn2min,self.mn2max])
            axis.set_xticks(np.arange(np.round(self.mn2min),np.ceil(self.mn2max)),
                            ((np.ceil(self.mn2max)-np.round(self.mn2min))/2))
            self.ax02.set_xlim([self.sed_mn2min,self.sed_mn2max])    
        for axis in (self.ax10, self.ax11):
         
#            watmin = min(self.fe_min,self.fe2min)
            axis.set_xlim([self.fe2min,self.fe2max])#fe2max
            self.ax12.set_xlim([self.sed_fe2min,self.sed_fe2max])    
            
        for axis in (self.ax20, self.ax21): 
               
            axis.set_xlim([self.h2smin,self.h2smax])
            self.ax22.set_xlim([self.sed_h2smin,self.sed_h2smax]) 
#            axis.set_xticks(np.arange(h2smin,0.75,0.25))          

# Plot Field data        

                        
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                self.ax00.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.mn2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.fe2[n],self.depth_sed,self.winter,linewidth=0.7) 
                
                self.ax20.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.h2s[n],self.depth_sed,self.winter,linewidth=0.7)
                
            elif n>=19 and n <= 60: #n >= 22 and n <= 90:      #Winter                                 
                self.ax00.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.mn2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.fe2[n],self.depth_sed,self.winter,linewidth=0.7) 
                
                self.ax20.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.h2s[n],self.depth_sed,self.winter,linewidth=0.7)      
                          
#            elif n>=19 and n<=21: #winter to compare with field data
#                ax00.plot(mn2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
#                ax01.plot(mn2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
#                ax02.plot(mn2[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
#                ax10.plot(fe2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(fe2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(fe2[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
#                ax20.plot(h2s[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax21.plot(h2s[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   #marker='o',
#                ax22.plot(h2s[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9) #marker='o',                     
                
            elif n >= 335 and n <365: #
                self.ax00.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)             
                self.ax01.plot(self.mn2[n],self.depth,self.winter,linewidth=0.7)  
                self.ax02.plot(self.mn2[n],self.depth_sed,self.winter,linewidth=0.7)                 
                self.ax10.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax11.plot(self.fe2[n],self.depth,self.winter,linewidth=0.7)   
                self.ax12.plot(self.fe2[n],self.depth_sed,self.winter,linewidth=0.7) 
                
                self.ax20.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7) 
                self.ax21.plot(self.h2s[n],self.depth,self.winter,linewidth=0.7)  #
                self.ax22.plot(self.h2s[n],self.depth_sed,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 240: #n >= 150 and n < 236: #self.summer                 
                self.ax00.plot(self.mn2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                self.ax01.plot(self.mn2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                self.ax02.plot(self.mn2[n],self.depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                self.ax10.plot(self.fe2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax11.plot(self.fe2[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                self.ax12.plot(self.fe2[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax20.plot(self.h2s[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                self.ax21.plot(self.h2s[n],self.depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                self.ax22.plot(self.h2s[n],self.depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
#            elif n >= 236 and n < 240: #from 25 to 30 august               
#                ax00.plot(mn2[n],depth,self.summer,linewidth=self.linewidth,zorder=9)             
#                ax01.plot(mn2[n],depth,self.summer,linewidth=self.linewidth)  
#                ax02.plot(mn2[n],depth_sed,self.summer,linewidth= self.linewidth)                 
#                ax10.plot(fe2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax11.plot(fe2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
#                ax12.plot(fe2[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
#                ax20.plot(h2s[n],depth,self.summer,linewidth=self.linewidth)   
#                ax21.plot(h2s[n],depth,self.summer,linewidth=self.linewidth)   #marker='o',
#                ax22.plot(h2s[n],depth_sed,self.summer,linewidth=self.linewidth) #marker='o',                                  
                         
            else:   #Spring and autumn

                self.ax00.plot(self.mn2[n],self.depth,self.spring_autumn, linewidth=0.7, alpha = self.alpha_autumn)             
                self.ax01.plot(self.mn2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  
                self.ax02.plot(self.mn2[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)                 
                self.ax10.plot(self.fe2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  
                 
                self.ax11.plot(self.fe2[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   
                self.ax12.plot(self.fe2[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)   

                self.ax20.plot(self.h2s[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 
                self.ax21.plot(self.h2s[n],self.depth,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn)  #
                self.ax22.plot(self.h2s[n],self.depth_sed,self.spring_autumn,linewidth=0.7, alpha = self.alpha_autumn) 

        for axis in (self.ax00,self.ax01,self.ax02,self.ax10,self.ax11,self.ax12,self.ax20,self.ax21,self.ax22):            
            self.y_lim(axis) 
            
        self.canvas.draw() 
    def plot5_field(self): #Mn,fe,h2s  
      
#        self.ax00.scatter(self.mn_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax01.scatter(self.mn_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax02.scatter(self.mn_winter_average,self.sed_depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10) 
#        self.ax10.scatter(self.fe_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax11.scatter(self.fe_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax12.scatter(self.fe_winter_average,self.sed_depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)         
#        self.ax20.scatter(self.h2s_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60 ,linewidth=0.5,zorder=10)#self.markersize
#        self.ax21.scatter(self.h2s_winter_average,self.depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)                               
#        self.ax22.scatter(self.h2s_winter_average,self.sed_depth_winter_average,color='g' , alpha=1,edgecolor='#262626',
#                     s = 60,linewidth=0.5,zorder=10)         
        self.ax00.plot(self.mn_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax01.plot(self.mn_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax02.plot(self.mn_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)  
        self.ax10.plot(self.fe_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax11.plot(self.fe_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax12.plot(self.fe_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)         
        self.ax20.plot(self.h2s_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax21.plot(self.h2s_winter_average,self.depth_winter_average,'bo--',linewidth=0.5)
        self.ax22.plot(self.h2s_winter_average,self.sed_depth_winter_average,'bo--',linewidth=0.5)   
                      
        self.ax00.scatter(self.mn_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax01.scatter(self.mn_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                               
        self.ax02.scatter(self.mn_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   

        self.ax00.plot(self.mn_mnfe_summer,self.depth_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax01.plot(self.mn_mnfe_summer,self.depth_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax02.plot(self.mn_mnfe_summer,self.sed_depth_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',  
        self.ax00.plot(self.mn1_mnfe_summer,self.depth1_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax01.plot(self.mn1_mnfe_summer,self.depth1_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax02.plot(self.mn1_mnfe_summer,self.sed_depth1_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',  
        self.ax00.plot(self.mn2_mnfe_summer,self.depth2_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax01.plot(self.mn2_mnfe_summer,self.depth2_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax02.plot(self.mn2_mnfe_summer,self.sed_depth2_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o', 
        self.ax00.plot(self.mn3_mnfe_summer,self.depth3_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax01.plot(self.mn3_mnfe_summer,self.depth3_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax02.plot(self.mn3_mnfe_summer,self.sed_depth3_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o', 
        self.ax00.plot(self.mn4_mnfe_summer,self.depth4_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax01.plot(self.mn4_mnfe_summer,self.depth4_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax02.plot(self.mn4_mnfe_summer,self.sed_depth4_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o', 
        
        self.ax00.scatter(self.mn_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax01.scatter(self.mn_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                               
        self.ax02.scatter(self.mn_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)           
         
#        self.ax00.scatter(self.mn_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
#                     s = self.markersize,linewidth=0.5,zorder=10)
#        self.ax01.scatter(self.mn_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
#                     s = self.markersize,linewidth=0.5,zorder=10)                               
#        self.ax02.scatter(self.mn_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
#                     s = self.markersize,linewidth=0.5,zorder=10)         



                      
        self.ax10.scatter(self.fe_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                
        self.ax11.scatter(self.fe_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax12.scatter(self.fe_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 

 
        self.ax10.plot(self.fe1_mnfe_summer,self.depth1_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax11.plot(self.fe1_mnfe_summer,self.depth1_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax12.plot(self.fe1_mnfe_summer,self.sed_depth1_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',
        self.ax10.plot(self.fe2_mnfe_summer,self.depth2_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax11.plot(self.fe2_mnfe_summer,self.depth2_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax12.plot(self.fe2_mnfe_summer,self.sed_depth2_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',        
        self.ax10.plot(self.fe3_mnfe_summer,self.depth3_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax11.plot(self.fe3_mnfe_summer,self.depth3_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax12.plot(self.fe3_mnfe_summer,self.sed_depth3_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',        
        self.ax10.plot(self.fe4_mnfe_summer,self.depth4_mnfe_summer,color='r',linewidth=self.linewidth)   
        self.ax11.plot(self.fe4_mnfe_summer,self.depth4_mnfe_summer,color='r',linewidth=self.linewidth)   #marker='o',
        self.ax12.plot(self.fe4_mnfe_summer,self.sed_depth_mnfe_summer,color='r',linewidth=self.linewidth) #marker='o',        
        

#        self.ax02.plot(self.mn1_mnfe_winter,self.sed_depth1_mnfe_winter,color='b',marker='o',linewidth=self.linewidth) #marker='o',
#        self.ax02.plot(self.mn2_mnfe_winter,self.sed_depth2_mnfe_winter,color='b',marker='o',linewidth=self.linewidth) #marker='o',        
#        self.ax02.plot(self.mn3_mnfe_winter,self.sed_depth3_mnfe_winter,color='b',marker='o',linewidth=self.linewidth) #marker='o',        
#        self.ax02.plot(self.mn4_mnfe_winter,self.sed_depth4_mnfe_winter,color='b',marker='o',linewidth=self.linewidth) #marker='o', 
#        self.ax02.plot(self.mn5_mnfe_winter,self.sed_depth5_mnfe_winter,color='b',marker='o',linewidth=self.linewidth) #marker='o', 
                
#        self.ax12.plot(self.fe1_mnfe_winter,self.sed_depth1_mnfe_winter,color='b',linewidth=self.linewidth) #marker='o',
#        self.ax12.plot(self.fe2_mnfe_winter,self.sed_depth2_mnfe_winter,color='b',linewidth=self.linewidth) #marker='o',        
#        self.ax12.plot(self.fe3_mnfe_winter,self.sed_depth3_mnfe_winter,color='b',linewidth=self.linewidth) #marker='o',        
#        self.ax12.plot(self.fe4_mnfe_winter,self.sed_depth4_mnfe_winter,color='b',linewidth=self.linewidth) #marker='o', 
#        self.ax12.plot(self.fe5_mnfe_winter,self.sed_depth5_mnfe_winter,color='b',linewidth=self.linewidth) #marker='o',  
#                       
        self.ax10.scatter(self.fe_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                
        self.ax11.scatter(self.fe_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax12.scatter(self.fe_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        
        self.ax10.scatter(self.fe_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        self.ax11.scatter(self.fe_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        self.ax12.scatter(self.fe_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   


       
           
        self.ax20.scatter(self.h2s_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                                     
        self.ax21.scatter(self.h2s_summer,self.depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        self.ax22.scatter(self.h2s_summer,self.sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        
        self.ax20.scatter(self.h2s_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                                     
        self.ax21.scatter(self.h2s_mai,self.depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        self.ax22.scatter(self.h2s_mai,self.sed_depth_mai,color='g' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)          
        
        
        self.ax20.scatter(self.h2s_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)           
        self.ax21.scatter(self.h2s_winter,self.depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        self.ax22.scatter(self.h2s_winter,self.sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        
          
        
        
        self.canvas.draw()    
    def plot6(self): # function to define 1 figure
        plt.clf() #clear figure before updating 
        self.numday = self.numdaySpinBox.value() #take the input value of numday spinbox
        style.use('ggplot')                 #use predefined style   
        self.figure.patch.set_facecolor('white')  #Set the background     
        wspace=0.40                         #define values for grid 
        hspace = 0.05                       #define values for grid
        gs = gridspec.GridSpec(2, 6) 
        gs.update(left=0.06, right=0.93,top = 0.84,bottom = 0.4, wspace=wspace,hspace=hspace)
        gs1 = gridspec.GridSpec(1, 6)
        gs1.update(left=0.06, right=0.93, top = 0.26, bottom = 0.02, wspace=wspace,hspace=hspace)     
           
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        self.ax30 = self.figure.add_subplot(gs[3])        
        self.ax40 = self.figure.add_subplot(gs[4])
        self.ax50 = self.figure.add_subplot(gs[5]) 
        
        self.ax01 = self.figure.add_subplot(gs[6]) #BBL
        self.ax11 = self.figure.add_subplot(gs[7])
        self.ax21 = self.figure.add_subplot(gs[8])
        self.ax31 = self.figure.add_subplot(gs[9])        
        self.ax41 = self.figure.add_subplot(gs[10])
        self.ax51 = self.figure.add_subplot(gs[11])  

        self.ax02 = self.figure.add_subplot(gs1[0]) #sediment
        self.ax12 = self.figure.add_subplot(gs1[1])
        self.ax22 = self.figure.add_subplot(gs1[2])
        self.ax32 = self.figure.add_subplot(gs1[3])        
        self.ax42 = self.figure.add_subplot(gs1[4])
        self.ax52 = self.figure.add_subplot(gs1[5])
        
        #Create axes sharing y              
        self.ax00_1 = self.ax00.twiny()  #water
        self.ax00_2 = self.ax00.twiny()  
        self.ax00_3 = self.ax00.twiny()
        
        self.ax01_1 = self.ax01.twiny() #bbl
        self.ax01_2 = self.ax01.twiny()
        self.ax01_3 = self.ax01.twiny()

        self.ax02_1 = self.ax02.twiny() #sediment
        self.ax02_2 = self.ax02.twiny()
        self.ax02_3 = self.ax02.twiny()
#        ax02_4 = ax02.twiny()
                 
        self.ax10_1 = self.ax10.twiny() #water
        self.ax10_2 = self.ax10.twiny() 
        self.ax10_3 = self.ax10.twiny()        
        self.ax10_4 = self.ax10.twiny()
#        ax10_5 = ax10.twiny()
        
        self.ax11_1 = self.ax11.twiny() #bbl
        self.ax11_2 = self.ax11.twiny()
        self.ax11_3 = self.ax11.twiny()
        self.ax11_4 = self.ax11.twiny()  

        self.ax12_1 = self.ax12.twiny() #sediment
        self.ax12_2 = self.ax12.twiny()
        self.ax12_3 = self.ax12.twiny()
        self.ax12_4 = self.ax12.twiny() 
                 
        self.ax20_1 = self.ax20.twiny() 
        self.ax20_2 = self.ax20.twiny() 
        self.ax20_3 = self.ax20.twiny()        
#        ax20_4 = ax20.twiny() 
        
        self.ax21_1 = self.ax21.twiny() 
        self.ax21_2 = self.ax21.twiny() 
        self.ax21_3 = self.ax21.twiny()        
#        ax21_4 = ax21.twiny() 

        self.ax22_1 = self.ax22.twiny() 
        self.ax22_2 = self.ax22.twiny() 
        self.ax22_3 = self.ax22.twiny() 
                       
        self.ax30_1 = self.ax30.twiny() 
        self.ax30_2 = self.ax30.twiny() 
        self.ax30_3 = self.ax30.twiny()        
        self.ax30_4 = self.ax30.twiny()            
        self.ax30_5 = self.ax30.twiny()
        
        self.ax31_1 = self.ax31.twiny() 
        self.ax31_2 = self.ax31.twiny() 
        self.ax31_3 = self.ax31.twiny()        
        self.ax31_4 = self.ax31.twiny()            
        self.ax31_5 = self.ax31.twiny()        
 
        self.ax32_1 = self.ax32.twiny() 
        self.ax32_2 = self.ax32.twiny() 
        self.ax32_3 = self.ax32.twiny()        
        self.ax32_4 = self.ax32.twiny()            
        self.ax32_5 = self.ax32.twiny()  
       
        self.ax40_1 = self.ax40.twiny() 
        self.ax40_2 = self.ax40.twiny() 
        self.ax40_3 = self.ax40.twiny()        
        self.ax40_4 = self.ax40.twiny()            
 
        self.ax41_1 = self.ax41.twiny() 
        self.ax41_2 = self.ax41.twiny() 
        self.ax41_3 = self.ax41.twiny()        
        self.ax41_4 = self.ax41.twiny() 

        self.ax42_1 = self.ax42.twiny() 
        self.ax42_2 = self.ax42.twiny() 
        self.ax42_3 = self.ax42.twiny()        
        self.ax42_4 = self.ax42.twiny() 
       
        self.ax50_1 = self.ax50.twiny() #water
        self.ax50_2 = self.ax50.twiny() 
        self.ax50_3 = self.ax50.twiny()        
        self.ax50_4 = self.ax50.twiny() 
               
        self.ax51_1 = self.ax51.twiny() #bbl
        self.ax51_2 = self.ax51.twiny() 
        self.ax51_3 = self.ax51.twiny()        
        self.ax51_4 = self.ax51.twiny()       

        self.ax52_1 = self.ax52.twiny() #sediment
        self.ax52_2 = self.ax52.twiny() 
        self.ax52_3 = self.ax52.twiny()        
        self.ax52_4 = self.ax52.twiny()        
        
        
        plt.text(1.1, 0.5,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax50.transAxes) 
        
        plt.text(1.1, 0.8,'Water ', fontweight='bold', # draw legend to BBL
        bbox={'facecolor': self.wat_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax51.transAxes)
        plt.text(1.1, 0.4,'BBL ', fontweight='bold',  #draw legend to Sediment
        bbox={'facecolor': self.bbl_color1 , 'alpha':0.6, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax51.transAxes) 
       
        plt.text(1.1, 0.7,'BBL ', fontweight='bold',  # draw legend to BBL
        bbox={'facecolor': self.bbl_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax52.transAxes)
        plt.text(1.1, 0.4,'Sediment ', fontweight='bold', #draw legend to Sediment
        bbox={'facecolor': self.sed_color1 , 'alpha':0.6, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax52.transAxes)  
       
        for axis in (self.ax00,self.ax10,self.ax20,self.ax30,self.ax40,self.ax50,
                    self.ax01,self.ax11,self.ax21,self.ax31,self.ax41,self.ax51,
                    self.ax02,self.ax12,self.ax22,self.ax32,self.ax42,self.ax52):
            self.y_lim1(axis)     
                                                                                     
        self.ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                

        plt.text(0, 1.61,'{}{}'.format('day', self.numday) , fontweight='bold', # Write number of day to Figure
        bbox={'facecolor': self.wat_color1, 'alpha':0.5, 'pad':10}, fontsize=14,
        transform= self.ax00.transAxes)
         

#        for axis in (self.ax00_1,self.ax20_1,self.ax30_1):
#            axis.spines['top'].set_position(('outward', self.axis1))
#            axis.spines['top'].set_color1('g')  
                
        #call function to place spines  
        for axis in (self.ax00,self.ax00_1,self.ax00_2,self.ax00_3,self.ax01,self.ax01_1,self.ax01_2,
                     self.ax01_3,self.ax02,self.ax02_1,self.ax02_2,self.ax02_3,self.ax10,self.ax10_1,
                     self.ax10_2,self.ax10_3,self.ax10_4,self.ax11,self.ax11_1,self.ax11_2,
                     self.ax11_3,self.ax11_4,self.ax12,self.ax12_1,self.ax12_2,self.ax12_3,
                     self.ax12_4,self.ax20,self.ax20_1,self.ax20_2,self.ax20_3,self.ax21,
                     self.ax21_1,self.ax21_2,self.ax21_3,self.ax22,self.ax22_1,self.ax22_2,self.ax22_3,
                     self.ax30,self.ax30_1,self.ax30_2,self.ax30_3,self.ax30_4,self.ax30_5,self.ax31,self.ax31_1,
                     self.ax31_2,self.ax31_3,self.ax31_4,self.ax31_5,self.ax32,self.ax32_1,self.ax32_2,self.ax32_3,
                     self.ax32_4,self.ax32_5,self.ax40,self.ax40_1,self.ax40_2,self.ax40_3,self.ax40_4,
                     self.ax41,self.ax41_1,self.ax41_2,self.ax41_3,self.ax41_4,self.ax42,self.ax42_1,self.ax42_2,
                     self.ax42_3,self.ax42_4,self.ax50,self.ax50_1,self.ax50_2,self.ax50_3,self.ax50_4,self.ax51,
                     self.ax51_1,self.ax51_2,self.ax51_3,self.ax51_4,
                     self.ax52,self.ax52_1,self.ax52_2,self.ax52_3,self.ax52_4):
            self.spines(axis)                       

        for axis in (self.ax00_1,self.ax01_1):        
            axis.set_xlim([self.kzmin,self.kzmax])
            axis.set_xticks(np.arange(self.kzmin,self.kzmax+((self.kzmax -self.kzmin)/2.),((self.kzmax - self.kzmin)/2.))) 
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                           
        self.ax00_1.annotate(r'$\rm Kz $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
 
            
        self.ax02_1.set_xlim([self.sed_kzmin,self.sed_kzmax])
        self.ax02_1.set_xticks(np.arange(self.sed_kzmin,self.sed_kzmax+
                        ((self.sed_kzmax - self.sed_kzmin)/2.),((self.sed_kzmax - self.sed_kzmin)/2.)))            
        self.ax02_1.annotate(r'$\rm Kz $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
        self.ax02_1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e')) 
                        
        for axis in (self.ax00, self.ax00_2, self.ax01_2,self.ax02_2):  
            axis.set_xlim([self.salmin,self.salmax])
            axis.set_xticks(np.arange(self.salmin,self.salmax+((self.salmax - self.salmin)/2.),((self.salmax - self.salmin)/2.))) 
        self.ax02_2.annotate(r'$\rm S $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')
        self.ax00_2.annotate(r'$\rm S $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r') 
                             
        for axis in ( self.ax00_3,  self.ax01_3,self.ax02_3):   
            axis.set_xlim([self.tempmin,self.tempmax])
            axis.set_xticks(np.arange(self.tempmin,self.tempmax+((self.tempmax - self.tempmin)/2.),
                            ((self.tempmax - self.tempmin)/2.))) 
        self.ax02_3.annotate(r'$\rm T $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')
        self.ax00_3.annotate(r'$\rm T $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')                                        
        for axis in (self.ax10, self.ax10_1,self.ax11_1, self.ax11):  
            axis.set_xlim([self.o2min,self.o2max])
            axis.set_xticks(np.arange(self.o2min,self.o2max+((self.o2max - self.o2min)/2.),((self.o2max - self.o2min)/2.)))   
        for axis in (self.ax12,self.ax12_1):  
            axis.set_xlim([self.sed_o2min,self.sed_o2max])
            axis.set_xticks(np.arange(self.sed_o2min,self.sed_o2max+
                            ((self.sed_o2max - self.sed_o2min)/2.),((self.sed_o2max - self.sed_o2min)/2.)))  
        self.ax12_1.annotate(r'$\rm O _2 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')   
        self.ax10_1.annotate(r'$\rm O _2 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                              
        for axis in ( self.ax10_2,  self.ax11_2):  
            axis.set_xlim([self.nh4min,self.nh4max])
            axis.set_xticks(np.arange(self.nh4min,self.nh4max+(self.nh4max /2.),(self.nh4max/2.)))    
            self.ax12_2.set_xlim([0,self.sed_nh4max])
            self.ax12_2.set_xticks(np.arange(0,self.sed_nh4max+(self.sed_nh4max /2.),(self.sed_nh4max/2.)))   
            self.ax12_2.annotate(r'$\rm NH _4 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r') 
            self.ax10_2.annotate(r'$\rm NH _4 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')                                          
        for axis in ( self.ax10_3,  self.ax11_3):  
            axis.set_xlim([0,self.no2max])
            axis.set_xticks(np.arange(0,self.no2max+(self.no2max /2.),(self.no2max/2.))) 
            self.ax12_3.set_xlim([0,self.sed_no2max])
            self.ax12_3.set_xticks(np.arange(0,self.sed_no2max+(self.sed_no2max /2.),(self.sed_no2max/2.))) 
            self.ax10_3.annotate(r'$\rm NO _2 $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')   
            self.ax12_3.annotate(r'$\rm NO _2 $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')                                                
        for axis in ( self.ax10_4,  self.ax11_4):  
            axis.set_xlim([0,self.no3max])
            axis.set_xticks(np.arange(0,self.no3max+(self.no3max /2.),(self.no3max/2.)))                   
        self.ax10_4.annotate(r'$\rm NO _3 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')                              
        self.ax12_4.set_xlim([0,self.sed_no3max])
        self.ax12_4.set_xticks(np.arange(0,self.sed_no3max+(self.sed_no3max /2.),(self.sed_no3max/2.)))         
        self.ax12_4.annotate(r'$\rm NO _3 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')     
              
        for axis in ( self.ax20, self.ax20_1,  self.ax21_1, self.ax21):  
            axis.set_xlim([0,self.po4max])
            axis.set_xticks(np.arange(0,self.po4max+(self.po4max /2.),(self.po4max /2.)))   
        for axis in ( self.ax22,  self.ax22_1):
            axis.set_xlim([0,self.sed_po4max])
            axis.set_xticks(np.arange(0,self.sed_po4max+(self.sed_po4max /2.),(self.sed_po4max /2.)))  
            axis.annotate(r'$\rm PO _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')    
        self.ax20_1.annotate(r'$\rm PO _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                              
        for axis in ( self.ax20_2,  self.ax21_2):  
            axis.set_xlim([0,self.ponmax])
            axis.set_xticks(np.arange(0,self.ponmax+(self.ponmax /2.),(self.ponmax/2.))) 
        self.ax22_2.set_xlim([0,self.sed_ponmax])
        self.ax22_2.set_xticks(np.arange(0,self.sed_ponmax+(self.sed_ponmax /2.),(self.sed_ponmax/2.))) 
        self.ax22_2.annotate(r'$\rm PON $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')    
        self.ax20_2.annotate(r'$\rm PON $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r') 
                                      
        for axis in ( self.ax20_3,  self.ax21_3):  
            axis.set_xlim([0,self.donmax])
            axis.set_xticks(np.arange(0,self.donmax+(self.donmax /2.),(self.donmax/2.)))                
        self.ax22_3.set_xlim([0,self.sed_donmax])
        self.ax22_3.set_xticks(np.arange(0,self.sed_donmax+(self.sed_donmax /2.),(self.sed_donmax/2.)))    
        self.ax20_3.annotate(r'$\rm DON $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b') 
        self.ax22_3.annotate(r'$\rm DON $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b') 
                                                                                                                                                                        
        for axis in ( self.ax30, self.ax30_1,  self.ax31_1, self.ax31):  
            axis.set_xlim([0,self.mn2max])
            axis.set_xticks(np.arange(0,(round(self.mn2max+(self.mn2max /2.),5)),self.mn2max/2.))                     
        for axis in ( self.ax32,  self.ax32_1):  
            axis.set_xlim([0,self.sed_mn2max])
            axis.set_xticks(np.arange(0,(round(self.sed_mn2max+(self.sed_mn2max /2.),5)),self.sed_mn2max/2.))                     
            axis.annotate(r'$\rm MnII $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')    
            self.ax30_1.annotate(r'$\rm MnII $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                                        
        for axis in ( self.ax30_2,  self.ax31_2):  
            axis.set_xlim([0,self.mn3max])
            axis.set_xticks(np.arange(0,(round(self.mn3max+(self.mn3max /2.),5)),self.mn3max/2.))                  
        self.ax32_2.set_xlim([0,self.sed_mn3max])
        self.ax32_2.set_xticks(np.arange(0,(round(self.sed_mn3max+(self.sed_mn3max /2.),5)),self.sed_mn3max/2.))                     
        self.ax32_2.annotate(r'$\rm MnIII $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')        
        self.ax30_2.annotate(r'$\rm MnIII $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')                           
        for axis in ( self.ax30_3,  self.ax31_3):  
            axis.set_xlim([0,self.mn4max])
            axis.set_xticks(np.arange(0,(round(self.mn4max+(self.mn4max /2.),5)),self.mn4max/2.))                      
        self.ax32_3.set_xlim([0,self.sed_mn4max])
        self.ax32_3.set_xticks(np.arange(0,self.sed_mn4max+(self.sed_mn4max /2.),(self.sed_mn4max/2.)))      
        self.ax32_3.annotate(r'$\rm MnIV $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')   
        self.ax30_3.annotate(r'$\rm MnIV $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')                                          
        for axis in ( self.ax30_4,  self.ax31_4):  
            axis.set_xlim([0,self.mnsmax])
            axis.set_xticks(np.arange(0,(round(self.mnsmax+(self.mnsmax /2.),5)),self.mnsmax/2.))    
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                
        self.ax32_4.set_xlim([0,self.sed_mnsmax])
        self.ax32_4.set_xticks(np.arange(0,(round(self.sed_mnsmax+(self.sed_mnsmax /2.),5)),self.sed_mnsmax/2.))                      
        self.ax32_4.annotate(r'$\rm MnS $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')     
        self.ax30_4.annotate(r'$\rm MnS $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')                                                          
        for axis in ( self.ax30_5, self.ax31_5):  
            axis.set_xlim([0,self.mnco3max])
            axis.set_xticks(np.arange(0,self.mnco3max+(self.mnco3max /2.),(self.mnco3max/2.))) 
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))     
        self.ax32_5.set_xlim([0,self.sed_mnco3max])
        self.ax32_5.set_xticks(np.arange(0,self.sed_mnco3max+(self.sed_mnco3max /2.),(self.sed_mnco3max/2.)))  
        self.ax32_5.annotate(r'$\rm MnCO _3 $', xy=(self.labelaxis_x,self.labelaxis5_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='c') 
        self.ax30_5.annotate(r'$\rm MnCO _3 $', xy=(self.labelaxis_x,self.labelaxis5_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='c')                                               
        for axis in (self.ax40,self.ax40_1, self.ax41_1,self.ax41):  
            axis.set_xlim([0,self.fe2max])
            axis.set_xticks(np.arange(0,(round(self.fe2max+(self.fe2max /2.),5)),self.fe2max/2.))                   
        for axis in (self.ax42, self.ax42_1):     
            axis.set_xlim([0,self.sed_fe2max])        
            axis.set_xticks(np.arange(0,self.sed_fe2max+(self.sed_fe2max/2.),(self.sed_fe2max/2.)))       
            axis.annotate(r'$\rm FeII $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
        self.ax40_1.annotate(r'$\rm FeII $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                                                        
        for axis in (self.ax40_2, self.ax41_2):  
            axis.set_xlim([0,self.fe3max])
            axis.set_xticks(np.arange(0,(round(self.fe3max+(self.fe3max /2.),5)),self.fe3max/2.))                   
        self.ax42_2.set_xlim([0,self.sed_fe3max])
        self.ax42_2.set_xticks(np.arange(0,self.sed_fe3max+(self.sed_fe3max /2.),(self.sed_fe3max/2.)))    
        self.ax42_2.annotate(r'$\rm FeIII $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')  
        self.ax40_2.annotate(r'$\rm FeIII $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')                                                             
        for axis in (self.ax40_3, self.ax41_3):  
            axis.set_xlim([0,self.fesmax])
            axis.set_xticks(np.arange(0,self.fesmax+(self.fesmax),(self.fesmax))) 
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                  
        self.ax42_3.set_xlim([0,self.sed_fesmax])
        self.ax42_3.set_xticks(np.arange(0,self.sed_fesmax+(self.sed_fesmax /2.),(self.sed_fesmax/2.)))   
        self.ax42_3.annotate(r'$\rm FeS $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='b')  
        self.ax40_3.annotate(r'$\rm FeS $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='b')                                                                  
        for axis in (self.ax40_4, self.ax41_4):  
            axis.set_xlim([0,self.fes2max])
            axis.set_xticks(np.arange(0,self.fes2max+(self.fes2max /2.),(self.fes2max/2.)))  
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                 
        self.ax42_4.set_xlim([0,self.sed_fes2max])
        self.ax42_4.set_xticks(np.arange(0,self.sed_fes2max+(self.sed_fes2max /2.),(self.sed_fes2max/2.)))  
        self.ax42_4.annotate(r'$\rm FeS _2 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='m')
        self.ax40_4.annotate(r'$\rm FeS _2 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='m')     
                                  
        for axis in (self.ax50,self.ax50_1, self.ax51_1,self.ax51):  
            axis.set_xlim([self.so4min,self.so4max])
            axis.set_xticks(np.arange(self.so4min,self.so4max+((self.so4max-self.so4min)/2.),((self.so4max-self.so4min)/2.)))              
#            axis.set_xticks(np.arange(0,self.so4max+(self.so4max/2.),(self.so4max/2.)))  
        for axis in (self.ax52, self.ax52_1):
            axis.set_xlim([self.sed_so4min,self.sed_so4max])
            axis.set_xticks(np.arange(self.sed_so4min,self.sed_so4max+((self.sed_so4max-self.sed_so4min)/2.),
                                      ((self.sed_so4max-self.sed_so4min)/2.)))  
            axis.annotate(r'$\rm SO _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='g')   
            self.ax50_1.annotate(r'$\rm SO _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='g')                                                 
        for axis in (self.ax50_2, self.ax51_2):  
            axis.set_xlim([0,self.s0max])
            axis.set_xticks(np.arange(0,self.s0max+(self.s0max /2.),(self.s0max/2.)))
        self.ax52_2.set_xlim([0,self.sed_s0max])
        self.ax52_2.set_xticks(np.arange(0,self.sed_s0max+(self.sed_s0max /2.),(self.sed_s0max/2.)))  
        self.ax52_2.annotate(r'$\rm S ^0 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
        xycoords='axes fraction', fontsize = self.xlabel_fontsize,color='r')      
        self.ax50_1.annotate(r'$\rm S ^0 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
        xycoords='axes fraction', fontsize = self.xlabel_fontsize,color='r')                                   
        for axis in (self.ax50_3, self.ax51_3):  
            axis.set_xlim([0,self.h2smax])
            axis.set_xticks(np.arange(0,self.h2smax+(self.h2smax /2.),(self.h2smax/2.)))  
        self.ax52_3.set_xlim([0,self.sed_h2smax])
        self.ax52_3.set_xticks(np.arange(0,self.sed_h2smax+(self.sed_h2smax /2.),(self.sed_h2smax/2.)))
        self.ax52_3.annotate(r'$\rm H _2 S $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='b') 
        self.ax50_3.annotate(r'$\rm H _2 S $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='b')                                                     
        for axis in (self.ax50_4, self.ax51_4):
            axis.set_xlim([0,self.s2o3max])
            axis.set_xticks(np.arange(0,(round(self.s2o3max+(self.s2o3max /2.),5)),self.s2o3max/2.))                            
        self.ax52_4.set_xlim([0,self.sed_s2o3max])
        self.ax52_4.set_xticks(np.arange(0,(round(self.sed_s2o3max+(self.sed_s2o3max /2.),5)),self.sed_s2o3max/2.))                
        self.ax52_4.annotate(r'$\rm S _2 O _3 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='center',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')
        self.ax50_4.annotate(r'$\rm S _2 O _3 $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')

                    
        # plot data
        self.ax00_1.plot(self.kz[self.numday],self.depth2,'g-')  
        self.ax01_1.plot(self.kz[self.numday],self.depth2,'go-')  #
        self.ax00_1.annotate(r'$\rm Kz $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
        self.ax00_1.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))  
                
        self.ax02_1.plot(self.kz[self.numday],self.depth_sed2,'go-')                          
        self.ax00_2.plot(self.sal[self.numday],self.depth,'r-')   
        self.ax01_2.plot(self.sal[self.numday],self.depth,'ro-')   
        self.ax02_2.plot(self.sal[self.numday],self.depth_sed,'ro-') 
        self.ax00_3.plot(self.temp[self.numday],self.depth,'b-') 
        self.ax01_3.plot(self.temp[self.numday],self.depth,'bo-')  
        self.ax02_3.plot(self.temp[self.numday],self.depth_sed,'bo-')                 
                            
        self.ax10_1.plot(self.o2[self.numday], self.depth, 'g-')
        self.ax11_1.plot(self.o2[self.numday], self.depth, 'go-')
        self.ax12_1.plot(self.o2[self.numday], self.depth_sed, 'go-')                 
        self.ax10_2.plot(self.nh4[self.numday], self.depth, 'r-')
        self.ax11_2.plot(self.nh4[self.numday], self.depth, 'ro-') 
        self.ax12_2.plot(self.nh4[self.numday], self.depth_sed, 'ro-')                
        self.ax10_3.plot(self.no2[self.numday], self.depth, 'b-')
        self.ax11_3.plot(self.no2[self.numday], self.depth, 'bo-') 
        self.ax12_3.plot(self.no2[self.numday], self.depth_sed, 'bo-')                 
        self.ax10_4.plot(self.no3[self.numday], self.depth, 'm-')        
        self.ax11_4.plot(self.no3[self.numday], self.depth, 'mo-')  
        self.ax12_4.plot(self.no3[self.numday], self.depth_sed, 'mo-') 
                       
        self.ax20_1.plot(self.po4[self.numday], self.depth, 'g-') 
        self.ax21_1.plot(self.po4[self.numday], self.depth, 'go-') 
        self.ax22_1.plot(self.po4[self.numday], self.depth_sed, 'go-')  
                      
        self.ax20_2.plot(self.pon[self.numday], self.depth, 'r-')
        self.ax21_2.plot(self.pon[self.numday], self.depth, 'ro-')
        self.ax22_2.plot(self.pon[self.numday], self.depth_sed, 'ro-')   
                     
        self.ax20_3.plot(self.don[self.numday], self.depth, 'b-') 
        self.ax21_3.plot(self.don[self.numday], self.depth, 'bo-')  
        self.ax22_3.plot(self.don[self.numday], self.depth_sed, 'bo-')                
               
        self.ax30_1.plot(self.mn2[self.numday], self.depth, 'g-') 
        self.ax31_1.plot(self.mn2[self.numday], self.depth, 'go-') 
        self.ax32_1.plot(self.mn2[self.numday], self.depth_sed, 'go-')               
        self.ax30_2.plot(self.mn3[self.numday], self.depth, 'r-')
        self.ax31_2.plot(self.mn3[self.numday], self.depth, 'ro-') 
        self.ax32_2.plot(self.mn3[self.numday], self.depth_sed, 'ro-')                
        self.ax30_3.plot(self.mn4[self.numday], self.depth, 'b-') 
        self.ax31_3.plot(self.mn4[self.numday], self.depth, 'bo-') 
        self.ax32_3.plot(self.mn4[self.numday], self.depth_sed, 'bo-')                
        self.ax30_4.plot(self.mns[self.numday], self.depth, 'm-')  
        self.ax31_4.plot(self.mns[self.numday], self.depth, 'mo-') 
        self.ax32_4.plot(self.mns[self.numday], self.depth_sed, 'mo-')                     
        self.ax30_5.plot(self.mnco3[self.numday], self.depth, 'c-')   
        self.ax31_5.plot(self.mnco3[self.numday], self.depth, 'co-')  
        self.ax32_5.plot(self.mnco3[self.numday], self.depth_sed, 'co-')                       

        self.ax40_1.plot(self.fe2[self.numday], self.depth, 'g-') 
        self.ax41_1.plot(self.fe2[self.numday], self.depth, 'g-')  
        self.ax42_1.plot(self.fe2[self.numday], self.depth_sed, 'go-')               
        self.ax40_2.plot(self.fe3[self.numday], self.depth, 'r-')
        self.ax41_2.plot(self.fe3[self.numday], self.depth, 'ro-') 
        self.ax42_2.plot(self.fe3[self.numday], self.depth_sed, 'ro-')                
        self.ax40_3.plot(self.fes[self.numday], self.depth, 'b-') 
        self.ax41_3.plot(self.fes[self.numday], self.depth, 'bo-')  
        self.ax42_3.plot(self.fes[self.numday], self.depth_sed, 'bo-')              
        self.ax40_4.plot(self.fes2[self.numday], self.depth, 'm-')  
        self.ax41_4.plot(self.fes2[self.numday], self.depth, 'mo-')
        self.ax42_4.plot(self.fes2[self.numday], self.depth_sed, 'mo-')
        self.ax50_1.plot(self.so4[self.numday], self.depth, 'g-') 
        self.ax51_1.plot(self.so4[self.numday], self.depth, 'go-') 
        self.ax52_1.plot(self.so4[self.numday], self.depth_sed, 'go-')                
        self.ax50_2.plot(self.s0[self.numday], self.depth, 'r-')
        self.ax51_2.plot(self.s0[self.numday], self.depth, 'ro-') 
        self.ax52_2.plot(self.s0[self.numday], self.depth_sed, 'ro-')                
        self.ax50_3.plot(self.h2s[self.numday], self.depth, 'b-') 
        self.ax51_3.plot(self.h2s[self.numday], self.depth, 'bo-')  
        self.ax52_3.plot(self.h2s[self.numday], self.depth_sed, 'bo-')              
        self.ax50_4.plot(self.s2o3[self.numday], self.depth, 'm-')  
        self.ax51_4.plot(self.s2o3[self.numday], self.depth, 'mo-')
        self.ax52_4.plot(self.s2o3[self.numday], self.depth_sed, 'mo-')


        self.canvas.draw()

    def plot6_1(self):
        plt.clf() #clear figure before updating 
        self.numday = self.numdaySpinBox.value() #take the input value of numday spinbox
        style.use('ggplot')                 #use predefined style   
        self.figure.patch.set_facecolor('white')  #Set the background     
        wspace=0.40                         #define values for grid 
        hspace = 0.05                       #define values for grid
        gs = gridspec.GridSpec(2, 6) 
        gs.update(left=0.06, right=0.93,top = 0.84,bottom = 0.4, wspace=wspace,hspace=hspace)
        gs1 = gridspec.GridSpec(1, 6)
        gs1.update(left=0.06, right=0.93, top = 0.26, bottom = 0.02, wspace=wspace,hspace=hspace)     
           
        #create subplots
        self.ax00 = self.figure.add_subplot(gs[0]) # water
        self.ax10 = self.figure.add_subplot(gs[1])
        self.ax20 = self.figure.add_subplot(gs[2])
        self.ax30 = self.figure.add_subplot(gs[3])        
        self.ax40 = self.figure.add_subplot(gs[4])
        self.ax50 = self.figure.add_subplot(gs[5]) 
        
        self.ax01 = self.figure.add_subplot(gs[6]) #BBL
        self.ax11 = self.figure.add_subplot(gs[7])
        self.ax21 = self.figure.add_subplot(gs[8])
        self.ax31 = self.figure.add_subplot(gs[9])        
        self.ax41 = self.figure.add_subplot(gs[10])
        self.ax51 = self.figure.add_subplot(gs[11])  

        self.ax02 = self.figure.add_subplot(gs1[0]) #sediment
        self.ax12 = self.figure.add_subplot(gs1[1])
        self.ax22 = self.figure.add_subplot(gs1[2])
        self.ax32 = self.figure.add_subplot(gs1[3])        
        self.ax42 = self.figure.add_subplot(gs1[4])
        self.ax52 = self.figure.add_subplot(gs1[5])
        
        plt.text(1.1, 0.5,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': self.wat_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform= self.ax50.transAxes) 
        
        plt.text(1.1, 0.8,'Water ', fontweight='bold', # draw legend to BBL
        bbox={'facecolor': self.wat_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax51.transAxes)
        plt.text(1.1, 0.4,'BBL ', fontweight='bold',  #draw legend to Sediment
        bbox={'facecolor': self.bbl_color1 , 'alpha':0.6, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax51.transAxes) 
       
        plt.text(1.1, 0.7,'BBL ', fontweight='bold',  # draw legend to BBL
        bbox={'facecolor': self.bbl_color1, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax52.transAxes)
        plt.text(1.1, 0.4,'Sediment ', fontweight='bold', #draw legend to Sediment
        bbox={'facecolor': self.sed_color1 , 'alpha':0.6, 'pad':10}, fontsize=14, rotation=90,
        transform= self.ax52.transAxes)  

        self.ax00.set_ylabel('Depth (m)',fontsize=14)
        self.ax01.set_ylabel('Depth (m)',fontsize=14)   
        self.ax02.set_ylabel('Depth (cm)',fontsize=14)                

        plt.text(0, 1.61,'{}{}'.format('day', self.numday) , fontweight='bold', #Write number of day to Figure
        bbox={'facecolor': self.wat_color, 'alpha':0.5, 'pad':10}, fontsize=14,
        transform=self.ax00.transAxes)
        
        self.ax00_1 = self.ax00.twiny()  #water
        self.ax00_2 = self.ax00.twiny()       
        self.ax01_1 = self.ax01.twiny() #bbl
        self.ax01_2 = self.ax01.twiny()
        self.ax02_1 = self.ax02.twiny() #sediment
        self.ax02_2 = self.ax02.twiny()
                 
        self.ax10_1 = self.ax10.twiny() #water
        self.ax10_2 = self.ax10.twiny() 
        self.ax10_3 = self.ax10.twiny()        
        self.ax10_4 = self.ax10.twiny()     
        self.ax11_1 = self.ax11.twiny() #bbl
        self.ax11_2 = self.ax11.twiny()
        self.ax11_3 = self.ax11.twiny()
        self.ax11_4 = self.ax11.twiny()  
        self.ax12_1 = self.ax12.twiny() #sediment
        self.ax12_2 = self.ax12.twiny()
        self.ax12_3 = self.ax12.twiny()
        self.ax12_4 = self.ax12.twiny() 
                 
        self.ax20_1 = self.ax20.twiny() 
        self.ax20_2 = self.ax20.twiny()         
        self.ax21_1 = self.ax21.twiny() 
        self.ax21_2 = self.ax21.twiny() 
        self.ax22_1 = self.ax22.twiny() 
        self.ax22_2 = self.ax22.twiny() 
                       
        self.ax30_1 = self.ax30.twiny() 
        self.ax30_2 = self.ax30.twiny()         
        self.ax31_1 = self.ax31.twiny()      
        self.ax31_2 = self.ax31.twiny() 
        self.ax32_1 = self.ax32.twiny() 
        self.ax32_2 = self.ax32.twiny()  
       
        self.ax40_1 = self.ax40.twiny() 
        self.ax40_2 = self.ax40.twiny()           
        self.ax41_1 = self.ax41.twiny() 
        self.ax41_2 = self.ax41.twiny() 
        self.ax42_1 = self.ax42.twiny() 
        self.ax42_2 = self.ax42.twiny()  
       
        self.ax50_1 = self.ax50.twiny() #water
        self.ax50_2 = self.ax50.twiny()                
        self.ax51_1 = self.ax51.twiny() #bbl
        self.ax51_2 = self.ax51.twiny()      
        self.ax52_1 = self.ax52.twiny() #sediment
        self.ax52_2 = self.ax52.twiny() 
        
        for axis in (self.ax00_1,self.ax02_1,self.ax10_1,self.ax12_1,
            self.ax20_1,self.ax22_1,self.ax30_1,self.ax32_1,self.ax40_1,self.ax42_1,self.ax50_1,self.ax52_1,
            self.ax00_2,self.ax02_2,self.ax10_2,self.ax12_2,self.ax20_2,self.ax22_2,self.ax30_2,self.ax32_2,
            self.ax40_2,self.ax42_2,self.ax50_2,self.ax52_2,self.ax10_3,self.ax12_3,self.ax10_4,self.ax12_4,
            self.ax00,self.ax01,self.ax02,self.ax01_1,self.ax01_2,self.ax10,#ax01_4,ax01_3
            self.ax11,self.ax11_1,self.ax11_2,self.ax11_3,self.ax11_4,self.ax12,self.ax20,
            self.ax21,self.ax21_1,self.ax21_2,self.ax22,self.ax30,#self.ax21_4,self.ax21_3,
            self.ax31,self.ax31_1,self.ax31_2,self.ax32,self.ax40,#self.ax31_3,self.ax31_4,self.ax31_5,
            self.ax41,self.ax41_1,self.ax41_2,self.ax42,self.ax50,self.ax51,#self.ax41_3,self.ax41_4,
            self.ax51_1,self.ax51_2,self.ax52):             
            for spinename, spine in axis.spines.iteritems():
                if spinename != 'top':
                    spine.set_visible(False)                
        for axis in (self.ax00_1,self.ax02_1,self.ax10_1,self.ax12_1,self.ax20_1,self.ax22_1,self.ax30_1,self.ax32_1,
                     self.ax40_1,self.ax42_1,self.ax50_1,self.ax52_1):
            axis.spines['top'].set_position(('outward', self.axis1))
            axis.spines['top'].set_color('g')                   
        for axis in (self.ax00_2,self.ax02_2,self.ax10_2,self.ax12_2,self.ax20_2,self.ax22_2,self.ax30_2,self.ax32_2,
                      self.ax40_2,self.ax42_2,self.ax50_2,self.ax52_2):    
            axis.spines['top'].set_position(('outward', self.axis2))
            axis.spines['top'].set_color('r')   
        for axis in (self.ax10_3,self.ax12_3):#,ax30_3,ax32_3,ax40_3,ax42_3,ax50_3,ax52_3,ax00_3,ax02_3,ax20_3,ax22_3):    
            axis.spines['top'].set_position(('outward', self.axis3))
            axis.spines['top'].set_color('b') 
        for axis in (self.ax10_4,self.ax12_4): #,ax20_4,ax30_4,ax32_4,ax40_4,ax42_4,ax50_4,ax52_4):
            axis.spines['top'].set_position(('outward', self.axis4))
            axis.spines['top'].set_color('m')     
#       elif axis in (ax30_5, ax32_5) :    
#           axis.spines['top'].set_position(('outward', axis5))
#           axis.spines['top'].set_color('c')    
        for axis in (self.ax00,self.ax01,self.ax02,self.ax01_1,self.ax01_2,self.ax10,#ax01_4,ax01_3
                        self.ax11,self.ax11_1,self.ax11_2,self.ax11_3,self.ax11_4,self.ax12,self.ax20,
                        self.ax21,self.ax21_1,self.ax21_2,self.ax22,self.ax30,#self.ax21_4,self.ax21_3,
                        self.ax31,self.ax31_1,self.ax31_2,self.ax32,self.ax40,#self.ax31_3,self.ax31_4,self.ax31_5,
                        self.ax41,self.ax41_1,self.ax41_2,self.ax42,self.ax50,self.ax51,#self.ax41_3,self.ax41_4,
                        self.ax51_1,self.ax51_2,self.ax52): #self.ax51_3,self.ax51_4, 
            plt.setp(axis.get_xticklabels(), visible=False)   

        #call function to define limits for all axis                                                  
        for axis in (self.ax00,self.ax10,self.ax20,self.ax30,self.ax40,self.ax50,
                    self.ax01,self.ax11,self.ax21,self.ax31,self.ax41,self.ax51,
                    self.ax02,self.ax12,self.ax22,self.ax32,self.ax42,self.ax52):
            self.y_lim1(axis)     
                       
              
                             

        for axis in ( self.ax00, self.ax00_1,  self.ax01_1):   
            axis.set_xlim([self.phymin,self.phymax])
            axis.set_xticks(np.arange(0,(round(self.phymax+(self.phymax/2.),5)),self.phymax/2.))                   
        self.ax02_1.set_xlim([self.sed_phymin,self.sed_phymax])
        self.ax02_1.set_xticks(np.arange(self.sed_phymin,self.sed_phymax+
            ((self.sed_phymax - self.sed_phymin)/2.),((self.sed_phymax - self.sed_phymin)/2.)))            
        self.ax02_1.annotate(r'$\rm Phy $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
        self.ax00_1.annotate(r'$\rm Phy $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
        for axis in (self.ax00, self.ax00_2, self.ax01_2):  
            axis.set_xlim([self.hetmin,self.hetmax])
            axis.set_xticks(np.arange(self.hetmin,self.hetmax+((self.hetmax - self.hetmin)/2.),((self.hetmax -self.hetmin)/2.))) 
        for axis in ( self.ax02, self.ax02_2):  
            axis.set_xlim([self.sed_hetmin,self.sed_hetmax])
            axis.set_xticks(np.arange(self.sed_hetmin,self.sed_hetmax+((self.sed_hetmax -self.sed_hetmin)/2.),((self.sed_hetmax -self.sed_hetmin)/2.)))  
            axis.annotate(r'$\rm Het $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')  
        self.ax00_2.annotate(r'$\rm Het $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')                               
        for axis in (self.ax10, self.ax10_1,  self.ax11_1, self.ax11):  
            axis.set_xlim([self.baanmin,self.baanmax])
            axis.set_xticks(np.arange(self.baanmin,self.baanmax+((self.baanmax - self.baanmin)/2.),((self.baanmax - self.baanmin)/2.)))   
        for axis in ( self.ax12, self.ax12_1):  
            axis.set_xlim([self.sed_baanmin,self.sed_baanmax])
            axis.set_xticks(np.arange(self.sed_baanmin,self.sed_baanmax+
                            ((self.sed_baanmax - self.sed_baanmin)/2.),((self.sed_baanmax - self.sed_baanmin)/2.)))  
            axis.annotate(r'$\rm Baan $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')   
        self.ax10_1.annotate(r'$\rm Baan $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
        xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                              
        for axis in ( self.ax10_2,  self.ax11_2):  
            axis.set_xlim([0,self.bhanmax])
            axis.set_xticks(np.arange(0,self.bhanmax+(self.bhanmax /2.),(self.bhanmax/2.)))    
        self.ax12_2.set_xlim([0,self.sed_bhanmax])
        self.ax12_2.set_xticks(np.arange(0,self.sed_bhanmax+(self.sed_bhanmax /2.),(self.sed_bhanmax/2.)))   
        self.ax12_2.annotate(r'$\rm Bhan $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r') 
        self.ax10_2.annotate(r'$\rm Bhan $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')                                          
        for axis in ( self.ax10_3,  self.ax11_3):  
            axis.set_xlim([0,self.bhaemax])
            axis.set_xticks(np.arange(0,self.bhaemax+(self.bhaemax/2.),(self.bhaemax/2.))) 
        self.ax12_3.set_xlim([0,self.sed_bhaemax])
        self.ax12_3.set_xticks(np.arange(0,self.sed_bhaemax+(self.sed_bhaemax /2.),(self.sed_bhaemax/2.))) 
        self.ax12_3.annotate(r'$\rm Bhae $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')   
        self.ax10_3.annotate(r'$\rm Bhae $', xy=(self.labelaxis_x,self.labelaxis3_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='b')                                                
        for axis in ( self.ax10_4,  self.ax11_4):  
            axis.set_xlim([0,self.baaemax])
            axis.set_xticks(np.arange(0,self.baaemax+(self.baaemax /2.),(self.baaemax/2.)))  
        self.ax12_4.set_xlim([0,self.sed_baaemax])
        self.ax12_4.set_xticks(np.arange(0,self.sed_baaemax+(self.sed_baaemax /2.),(self.sed_baaemax/2.)))         
        self.ax12_4.annotate(r'$\rm Baae $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')      
        self.ax10_4.annotate(r'$\rm Baae $', xy=(self.labelaxis_x,self.labelaxis4_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='m')               
        for axis in ( self.ax20, self.ax20_1,  self.ax21_1, self.ax21):  
            axis.set_xlim([self.phmin,self.phmax])
            axis.set_xticks(np.arange(self.phmin,(round(self.phmax+((self.phmax - self.phmin)/2.),5)),
                                      ((self.phmax - self.phmin)/2.)))  
        for axis in ( self.ax22,  self.ax22_1):
            axis.set_xlim([self.sed_phmin,self.sed_phmax])
            axis.set_xticks(np.arange(self.sed_phmin,(round(self.sed_phmax+(
                            (self.sed_phmax - self.sed_phmin)/2.),5)),((self.sed_phmax - self.sed_phmin)/2.))) 
            axis.annotate(r'$\rm pH $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')    
            self.ax20_1.annotate(r'$\rm pH $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                              
        for axis in ( self.ax20_2,  self.ax21_2):  
            axis.set_xlim([0,self.pco2max])
            axis.set_xticks(np.arange(0,self.pco2max+(self.pco2max /2.),(self.pco2max/2.))) 
        self.ax22_2.set_xlim([0,self.sed_pco2max])
        self.ax22_2.set_xticks(np.arange(0,self.sed_pco2max+(self.sed_pco2max /2.),(self.sed_pco2max/2.))) 
        self.ax22_2.annotate(r'$\rm pCO _2 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')    
        self.ax20_2.annotate(r'$\rm pCO _2 $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')                                                                                                                                                                                            
        for axis in (self.ax30, self.ax30_1,  self.ax31_1, self.ax31):  
            axis.set_xlim([self.alkmin,self.alkmax])
            axis.set_xticks(np.arange(self.alkmin,(self.alkmax+(self.alkmax - self.alkmin)/2.),((self.alkmax - self.alkmin)/2.)))                                  
        for axis in ( self.ax32,  self.ax32_1):  
            axis.set_xlim([self.sed_alkmin,self.sed_alkmax])
            axis.set_xticks(np.arange(self.sed_alkmin,(self.sed_alkmax+(self.sed_alkmax - self.sed_alkmin)/2.),
                                      ((self.sed_alkmax - self.sed_alkmin)/2.)))            
#            axis.set_xticks(np.arange(self.sed_alkmin,(round(self.sed_alkmax+(
#                            (self.sed_alkmax - self.sed_alkmin)/2.),5)),((self.sed_alkmax - self.sed_alkmin)/2.)))                                      
            axis.annotate(r'$\rm Alk $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')    
            self.ax30_1.annotate(r'$\rm Alk $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')                                        
        for axis in ( self.ax30_2,  self.ax31_2):  
            axis.set_xlim([0,self.dicmax])
            axis.set_xticks(np.arange(0,(round(self.dicmax+(self.dicmax /2.),5)),self.dicmax/2.))                  
        self.ax32_2.set_xlim([0,self.sed_dicmax])
        self.ax32_2.set_xticks(np.arange(0,(round(self.sed_dicmax+(self.sed_dicmax /2.),5)),self.sed_dicmax/2.))                     
        self.ax32_2.annotate(r'$\rm DIC $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')        
        self.ax30_2.annotate(r'$\rm DIC $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='r')                           

                     
        for axis in (self.ax40,self.ax40_1, self.ax41_1,self.ax41):  
            axis.set_xlim([0,self.ch4max])
            axis.ticklabel_format(style='sci', axis='x', scilimits=(-4,4),labelOnlyBase=False)
#                axis.set_xticks(np.arange(0,(round(self.ch4max+(self.ch4max /2.),4)),self.ch4max/2.))   
            axis.set_xticks(np.arange(0,self.ch4max+(self.ch4max/2.),(self.ch4max/2.)))    
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                                 
        for axis in (self.ax42, self.ax42_1):   
            axis.set_xlim([0,self.sed_ch4max])        
            axis.set_xticks(np.arange(0,self.sed_ch4max+(self.sed_ch4max/2.),(self.sed_ch4max/2.)))       
            axis.annotate(r'$\rm CH _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')
            self.ax40_1.annotate(r'$\rm CH _4 $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='g')      
            axis.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))                                       
        for axis in (self.ax40_2, self.ax41_2):  
            axis.set_xlim([0,self.om_armax])
            axis.set_xticks(np.arange(0,(round(self.om_armax+(self.om_armax /2.),5)),self.om_armax/2.))                     
        self.ax42_2.set_xlim([0,self.sed_om_armax])
        self.ax42_2.set_xticks(np.arange(0,self.sed_om_armax+(self.sed_om_armax /2.),(self.sed_om_armax/2.)))            
        self.ax42_2.annotate(r'$\rm \Omega Ar $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')  
        self.ax40_2.annotate(r'$\rm \Omega Ar $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize,color='r')                                                             
                  
        for axis in (self.ax50,self.ax50_1, self.ax51_1,self.ax51):  
            axis.set_xlim([0,self.simax])
            axis.set_xticks(np.arange(0,self.simax+(self.simax/2.),(self.simax/2.)))  
        for axis in (self.ax52, self.ax52_1):
            axis.set_xlim([0,self.sed_simax])
            axis.set_xticks(np.arange(0,self.sed_simax+(self.sed_simax/2.),(self.sed_simax/2.)))  
            axis.annotate(r'$\rm Si $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='center',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='g')   
            self.ax50_1.annotate(r'$\rm Si $', xy=(self.labelaxis_x,self.labelaxis1_y), ha='left', va='bottom',
            xycoords='axes fraction',  fontsize = self.xlabel_fontsize, color='g')                                                 
        for axis in (self.ax50_2, self.ax51_2):  
            axis.set_xlim([0,self.si_partmax])
            axis.set_xticks(np.arange(0,self.si_partmax+(self.si_partmax /2.),(self.si_partmax/2.)))
        self.ax52_2.set_xlim([0,self.sed_si_partmax])
        self.ax52_2.set_xticks(np.arange(0,self.sed_si_partmax+(self.sed_si_partmax /2.),(self.sed_si_partmax/2.)))  
        self.ax52_2.annotate(r'$\rm Si part $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='center',
            xycoords='axes fraction', fontsize = self.xlabel_fontsize,color='r')      
        self.ax50_1.annotate(r'$\rm Si part $', xy=(self.labelaxis_x,self.labelaxis2_y), ha='left', va='bottom',
            xycoords='axes fraction', fontsize = self.xlabel_fontsize,color='r')                                   

                 
        # plot data
        self.ax00_1.plot(self.phy[self.numday],self.depth,'g-') 
        self.ax01_1.plot(self.phy[self.numday],self.depth,'go-')  
        self.ax02_1.plot(self.phy[self.numday],self.depth_sed,'go-')                          
        self.ax00_2.plot(self.het[self.numday],self.depth,'r-')   
        self.ax01_2.plot(self.het[self.numday],self.depth,'ro-')   
        self.ax02_2.plot(self.het[self.numday],self.depth_sed,'ro-') 
#        self.ax00_3.plot(temp[self.numday],self.depth,'b-') 
#        self.ax01_3.plot(temp[self.numday],self.depth,'bo-')  
#        self.ax02_3.plot(temp[self.numday],self.depth_sed,'bo-')                 
                            
        self.ax10_1.plot(self.baan[self.numday], self.depth, 'g-')
        self.ax11_1.plot(self.baan[self.numday], self.depth, 'go-')
        self.ax12_1.plot(self.baan[self.numday], self.depth_sed, 'go-')                 
        self.ax10_2.plot(self.bhan[self.numday], self.depth, 'r-')
        self.ax11_2.plot(self.bhan[self.numday], self.depth, 'ro-') 
        self.ax12_2.plot(self.bhan[self.numday], self.depth_sed, 'ro-')                
        self.ax10_3.plot(self.bhae[self.numday], self.depth, 'b-')
        self.ax11_3.plot(self.bhae[self.numday], self.depth, 'bo-') 
        self.ax12_3.plot(self.bhae[self.numday], self.depth_sed, 'bo-')                 
        self.ax10_4.plot(self.baae[self.numday], self.depth, 'm-')        
        self.ax11_4.plot(self.baae[self.numday], self.depth, 'mo-')  
        self.ax12_4.plot(self.baae[self.numday], self.depth_sed, 'mo-') 
                       
        self.ax20_1.plot(self.ph[self.numday], self.depth, 'g-') 
        self.ax21_1.plot(self.ph[self.numday], self.depth, 'go-') 
        self.ax22_1.plot(self.ph[self.numday], self.depth_sed, 'go-')                
        self.ax20_2.plot(self.pco2[self.numday], self.depth, 'r-')
        self.ax21_2.plot(self.pco2[self.numday], self.depth, 'ro-')
        self.ax22_2.plot(self.pco2[self.numday], self.depth_sed, 'ro-')                
#        self.ax20_3.plot(don[self.numday], self.depth, 'b-') 
#        self.ax21_3.plot(don[self.numday], self.depth, 'bo-')  
#        self.ax22_3.plot(don[self.numday], self.depth_sed, 'bo-')                
               
        self.ax30_1.plot(self.alk[self.numday], self.depth, 'g-') 
        self.ax31_1.plot(self.alk[self.numday], self.depth, 'go-') 
        self.ax32_1.plot(self.alk[self.numday], self.depth_sed, 'go-')               
        self.ax30_2.plot(self.dic[self.numday], self.depth, 'r-')
        self.ax31_2.plot(self.dic[self.numday], self.depth, 'ro-') 
        self.ax32_2.plot(self.dic[self.numday], self.depth_sed, 'ro-')                
#        self.ax30_3.plot(mn4[self.numday], self.depth, 'b-') 
#        self.ax31_3.plot(mn4[self.numday], self.depth, 'bo-') 
#        self.ax32_3.plot(mn4[self.numday], self.depth_sed, 'bo-')                
#        self.ax30_4.plot(mns[self.numday], self.depth, 'm-')  
#        self.ax31_4.plot(mns[self.numday], self.depth, 'mo-') 
#        self.ax32_4.plot(mns[self.numday], self.depth_sed, 'mo-')                     
#        self.ax30_5.plot(mnco3[self.numday], self.depth, 'c-')   
#        self.ax31_5.plot(mnco3[self.numday], self.depth, 'co-')  
#        self.ax32_5.plot(mnco3[self.numday], self.depth_sed, 'co-')                       

        self.ax40_1.plot(self.ch4[self.numday], self.depth, 'g-') 
        self.ax41_1.plot(self.ch4[self.numday], self.depth, 'g-')  
        self.ax42_1.plot(self.ch4[self.numday], self.depth_sed, 'go-')               
        self.ax40_2.plot(self.om_ar[self.numday], self.depth, 'r-')
        self.ax41_2.plot(self.om_ar[self.numday], self.depth, 'ro-') 
        self.ax42_2.plot(self.om_ar[self.numday], self.depth_sed, 'ro-')                
#        self.ax40_3.plot(fes[self.numday], self.depth, 'b-') 
#        self.ax41_3.plot(fes[self.numday], self.depth, 'bo-')  
#        self.ax42_3.plot(fes[self.numday], self.depth_sed, 'bo-')              
#        self.ax40_4.plot(fes2[self.numday], self.depth, 'm-')  
#        self.ax41_4.plot(fes2[self.numday], self.depth, 'mo-')
#        self.ax42_4.plot(fes2[self.numday], self.depth_sed, 'mo-')
        self.ax50_1.plot(self.si[self.numday], self.depth, 'g-') 
        self.ax51_1.plot(self.si[self.numday], self.depth, 'go-') 
        self.ax52_1.plot(self.si[self.numday], self.depth_sed, 'go-')                
        self.ax50_2.plot(self.si_part[self.numday], self.depth, 'r-')
        self.ax51_2.plot(self.si_part[self.numday], self.depth, 'ro-') 
        self.ax52_2.plot(self.si_part[self.numday], self.depth_sed, 'ro-')                
#        self.ax50_3.plot(h2s[self.numday], self.depth, 'b-') 
#        self.ax51_3.plot(h2s[self.numday], self.depth, 'bo-')  
#        self.ax52_3.plot(h2s[self.numday], self.depth_sed, 'bo-')              
#        self.ax50_4.plot(s2o3[self.numday], self.depth, 'm-')  
#        self.ax51_4.plot(s2o3[self.numday], self.depth, 'mo-')
#        self.ax52_4.plot(s2o3[self.numday], self.depth_sed, 'mo-')


        self.canvas.draw()


             
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.showDialog()
#    main2 = Window2()    
#    main.show()
    main.show()
    
    sys.exit(app.exec_()) 
