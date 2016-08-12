import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QSpinBox,QLabel

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#import numpy as np
#from readfile import *

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

'''
Created on 24. jun. 2016

@author: ELP
'''

#!/usr/bin/python
# Filename: readfile.py
# Import standard (i.e., non GOTM-GUI) modules.
import sys,os
from netCDF4 import Dataset
import numpy as np


numday = 100
#my_example_nc_file = 'BROM_out.nc'
my_example_nc_file = 'BROM_Berre_out.nc'
fh = Dataset(my_example_nc_file, mode='r')

depth = fh.variables['z'][:] #middle points
depth2 = fh.variables['z2'][:] #middle points
alk = fh.variables['Alk'][:,:,0]
temp = fh.variables['T'][:,:,0]
sal = fh.variables['S'][:,:,0]
kz = fh.variables['Kz'][:,:,0]
dic = fh.variables['DIC'][:,:,0]
phy = fh.variables['Phy'][:,:,0]
het = fh.variables['Het'][:,:,0]
no3 = fh.variables['NO3'][:,:,0]
po4 = fh.variables['PO4'][:,:,0]
nh4 = fh.variables['NH4'][:,:,0]
pon = fh.variables['PON'][:,:,0]
don = fh.variables['DON'][:,:,0]
o2  = fh.variables['O2'][:,:,0]
mn2 = fh.variables['Mn2'][:,:,0]
mn3 = fh.variables['Mn3'][:,:,0]
mn4 = fh.variables['Mn4'][:,:,0]
h2s = fh.variables['H2S'][:,:,0]
mns = fh.variables['MnS'][:,:,0]
mnco3 = fh.variables['MnCO3'][:,:,0]
fe2 = fh.variables['Fe2'][:,:,0]
fe3 = fh.variables['Fe3'][:,:,0]
fes = fh.variables['FeS'][:,:,0]
feco3 = fh.variables['FeCO3'][:,:,0]
no2 = fh.variables['NO3'][:,:,0]
s0 = fh.variables['S0'][:,:,0]
s2o3 = fh.variables['S2O3'][:,:,0]
so4 = fh.variables['SO4'][:,:,0]
si = fh.variables['Si'][:,:,0]
si_part = fh.variables['Sipart'][:,:,0]
baae = fh.variables['Baae'][:,:,0]
bhae = fh.variables['Bhae'][:,:,0]
baan = fh.variables['Baan'][:,:,0]
bhan = fh.variables['Bhan'][:,:,0]
caco3 = fh.variables['CaCO3'][:,:,0]
fes2 = fh.variables['FeS2'][:,:,0]
ch4 = fh.variables['CH4'][:,:,0]
ph = fh.variables['pH'][:,:,0]
pco2 = fh.variables['pCO2'][:,:,0]
om_ca = fh.variables['Om_Ca'][:,:,0]
om_ar = fh.variables['Om_Ar'][:,:,0]
co3 = fh.variables['CO3'][:,:,0]
ca = fh.variables['Ca'][:,:,0]
time = fh.variables['time'][:]


def calculate_watmax():
    for n in range(0,(len(depth2)-1)):
#        if depth[_]-depth[_?]
        if depth2[n+1] - depth2[n] >= 0.5:
            pass
        elif depth2[n+1] - depth2[n] < 0.50:
#            watmax =  depth[n],depth[n]-depth[n+1],n
#            y1max =np.ceil(depth2[n])    
            y1max = (depth2[n])                     
#            print y1max,depth[n+1],depth[n],depth[n+1]-depth[n]
#            print 'y1max', y1max
#            print 'ynmax', ynmax             
            return y1max
            break

      
#print kz[numday,n]
def calculate_bblmax():
    for n in range(0,(len(depth2)-1)):
        if kz[1,n] == 0:
            y2max =depth2[n]    
#            print 'y2max', y2max       
            return y2max
            break        
 
def y2max_fill_water():
    for n in range(0,(len(depth2)-1)):
#        if depth[_]-depth[_?]
        if depth2[n+1] - depth2[n] >= 0.5:
            pass
        elif depth2[n+1] - depth2[n] < 0.50:
#            watmax =  depth[n],depth[n]-depth[n+1],n
            y2max_fill_water = depth2[n]            
#            print y1max,depth[n+1],depth[n],depth[n+1]-depth[n]
#            print 'y2max_fill_water',y2max_fill_water
            return y2max_fill_water
            break 
   
y1min = 0
y1max = calculate_watmax()

#y2min = y1max #109 #depth[len(depth[:])-19]#108.5
y2max = calculate_bblmax() #110.0 #(sed_wat interface)#depth[len(depth[:])-13]#
y2min = y2max - 2*(y2max - y1max)   #calculate the position of y2min, for catching part of BBL 
#print 'y2min', y2min
y2min_fill_bbl = y2max_fill_water = y1max #y2max_fill_water() #109.5 #BBL-water interface
ysedmax_fill_bbl = ysedmin_fill_sed = 0

#y2max = 110 #(sed_wat interface)
to_float = []
for item in depth:
    to_float.append(float(item)) #make a list of floats from tuple 
depth_sed = [] # list for storing final depth data for sediment 
v=0  
for i in to_float:
    v = (i- y2max)*100  #convert depth from m to cm
    depth_sed.append(v)

to_float2 = []
for item in depth2:
    to_float2.append(float(item)) #make a list of floats from tuple 
depth_sed2 = [] # list for storing final depth data for sediment 
v2=0  
for i in to_float2:
    v2 = (i- y2max)*100  #convert depth from m to cm
    depth_sed2.append(v2) 

def calculate_sedmin():
    for n in range(0,(len(depth_sed)-1)):
        if kz[1,n] == 0:
            ysed = depth_sed[n]  
            ysedmin =  ysed - 10                
#            print ysed    
            return ysedmin
            break   
        
def calculate_sedmax():
    for n in range(0,(len(depth_sed)-1)):
        if kz[1,n] == 0:
            ysed = depth_sed[n]    
            ysedmax =  ysed + 10              
#            print ysed    
            return ysedmax
            break          
#calculate_sedmin()        
        
#y3min = -10 #109.91
#y3max = 10 #110.10
ysedmin = calculate_sedmin()
#print ysedmin #-10#depth[len(depth[:])-15]#109.9 #for depth in m
ysedmax = calculate_sedmax()    #10#depth[len(depth[:])-1]#110.1
#print depth[len(depth[:])-12]
#print depth_sed2#ysedmin


#for filling the font


#ysedmin_fill_bbl = 0
#y3max_fill_bbl = 0
#y3min_fill_sed = 0


xticks =(np.arange(0,100000))

wat_color = '#ffffff' #'#f9fafb'#'#c9ecfd' #colors for filling water,bbl and sedimnet 
bbl_color = '#ccd6de'#'#2873b8' 
sed_color = '#7a8085' #666b6f '#'#916012'
alpha_wat = 0.3 # saturation of color (from 0 to 1) 
alpha_bbl = 0.3
alpha_sed = 0.5


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


#wat_color = '#c9ecfd' #colors for filling water,bbl and sedimnet 
#bbl_color = '#2873b8' 
#sed_color = '#916012'

xlabel_fontsize = 14

#numday = fh.variables['time'][:] 

def watmax(variable):
    n = variable[:,y1min:y2max].max()#+ ((variable[:,y1min:y2max].max())/10))

    if n > 10000:
        n = 30000#np.ceil(n)
    elif n > 5000 and n <= 10000:  
        n = 10000         
    elif n > 1000 and n <= 5000:  
        n = 5000        
    elif n > 500 and n <= 1000:  
        n = 1000 
    elif n > 350 and n <= 500:  
        n = 500                       
    elif n > 200 and n <= 350:  
        n = 350          
    elif n > 100 and n <= 200:  
        n = 200         
    elif n > 10 and n <= 100:
        n = 100     
    elif n > 0.5 and n <= 10:
        n = 10          
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


def watmin(variable):
    n = np.round(variable[:,y1min:y2max].min())
    return n
#print depth [:-12]
def sedmax(variable):
    n = variable[:,-15:].max()# + ((variable[:,ysedmin:ysedmax].max()))) #np.ceil
    if n > 10000:
        n = 30000#np.ceil(n)
    elif n > 5000 and n <= 10000:  
        n = 10000         
    elif n > 1000 and n <= 5000:  
        n = 5000        
    elif n > 500 and n <= 1000:  
        n = 1000 
    elif n > 350 and n <= 500:  
        n = 500                       
    elif n > 200 and n <= 350:  
        n = 350          
    elif n > 100 and n <= 200:  
        n = 200         
    elif n > 10 and n <= 100:
        n = 100     
    elif n > 0.5 and n <= 10:
        n = 10          
    elif n > 0.05 and n <= 0.5:
        n = 0.5           
    elif n > 0.005 and n <= 0.05:
        n = 0.05         
    elif n > 0.0005 and n <= 0.005:
        n = 0.005
    elif n > 0.00005 and  n  <= 0.0005 :
        n = 0.0005   
    elif n <= 5.e-5:#   0.00005  :
        n = 5.e-5#0.00005             
    return n 

def sedmin(variable):
    n = np.ceil(variable[:,-15:].min())
    return n
    



alkmax =  watmax(alk)
sed_alkmax = sedmax(alk)
alkmin =  watmin(alk)
sed_alkmin = sedmin(alk)

tempmax = temp[:,y1min:ysedmax].max()+0.01 #np.ceil(temp[:,:-13].max())  # watmax(temp)
sed_tempmax =  np.ceil(temp[:,-15:].max())#sedmax(temp)
tempmin =  temp[:,y1min:y2max].min()- 0.01 #watmin(temp)
sed_tempmin =  sedmin(temp)

salmax =  sal[:,y1min:ysedmax].max()+0.01   #watmax(sal) #sal[:,:].max()+ 0.1 #np.ceil()#watmax(sal)
sed_salmax = np.ceil(sal[:,-15:].max())   #sedmax(sal)
salmin =  sal[:,y1min:y2max].min()- 0.01  #watmin(sal)#sal[:,:].min()-0.2 #np.round(sal[:,-15:].min())#watmin(sal)
sed_salmin = sal[:,y1min:y2max].min()     #np.round(sal[:,-15:].min())#sedmin(sal)

kzmax =  watmax(kz)
sed_kzmax = sedmax(kz)
kzmin =  0#watmin(kz)
sed_kzmin = 0#sedmin(kz)

dicmax =  watmax(dic)
dicmin =  watmin(dic)
sed_dicmax = sedmax(dic)
sed_dicmin = sedmin(dic)

phymax =  watmax(phy)
phymin =  watmin(phy)
sed_phymin = sedmin(phy)
sed_phymax = sedmax(phy)

hetmax =  watmax(het)
hetmin = watmin(het)
sed_hetmax =  sedmax(het)
sed_hetmin =  sedmin(het)

no3max =  watmax(no3)
sed_no3max =  sedmax(no3)

po4max =  watmax(po4)
sed_po4max =  sedmax(po4)

nh4max =  watmax(nh4)
sed_nh4max =  sedmax(nh4)

ponmax = watmax(pon)
sed_ponmax = sedmax(pon)

donmax = watmax(don)
sed_donmax = sedmax(don)

o2max = watmax(o2)
o2min = 0#watmin(o2)
sed_o2max = sedmax(o2)
sed_o2min = 0#sedmin(o2)

mn2max = watmax(mn2)
sed_mn2max = sedmax(mn2)

mn3max = watmax(mn3)

sed_mn3max = sedmax(mn3)

mn4max = watmax(mn4)
sed_mn4max = sedmax(mn4)

h2smax = watmax(h2s)
sed_h2smax = sedmax(h2s)

mnsmax = watmax(mns)
sed_mnsmax = sedmax(mns)

mnco3max = watmax(mnco3)
sed_mnco3max = sedmax(mnco3)

fe2max = watmax(fe2)
sed_fe2max = sedmax(fe2)

fe3max = watmax(fe3)
sed_fe3max = sedmax(fe3)

fesmax = watmax(fes)
sed_fesmax = sedmax(fes)

feco3max = watmax(feco3)
sed_feco3max = sedmax(feco3)

no2max = watmax(no2)
sed_no2max = sedmax(no2)

s0max = watmax(s0)
sed_s0max = sedmax(s0)

s2o3max = watmax(s2o3)
sed_s2o3max = sedmax(s2o3)

so4max = watmax(so4)
sed_so4max = sedmax(so4)
so4min = watmin(so4)
sed_so4min = sedmin(so4)

simax = watmax(si)
sed_simax = sedmax(si)

si_partmax = watmax(si_part)
sed_si_partmax = sedmax(si_part)

baaemax = watmax(baae)
sed_baaemax = sedmax(baae)

bhaemax = watmax(bhae)
sed_bhaemax = sedmax(bhae)

sed_baanmin = 0#sedmin(baan)
baanmin = 0#watmin(baan)
baanmax = watmax(baan)
sed_baanmax = sedmax(baan)

bhanmax = watmax(bhan)
sed_bhanmax = sedmax(bhan)

caco3smax = watmax(caco3)
sed_caco3smax = sedmax(caco3)

fes2max = watmax(fes2)
sed_fes2max = sedmax(fes2)

ch4max = watmax(ch4)
sed_ch4max = sedmax(ch4)

phmax = watmax(ph)
phmin = watmin(ph)
sed_phmax = sedmax(ph)
sed_phmin = sedmin(ph)

pco2max = watmax(pco2)
sed_pco2max = sedmax(pco2)

om_camax = watmax(om_ca)
sed_om_camax = sedmax(om_ca)

om_armax = watmax(om_ar)
sed_om_armax = sedmax(om_ar)

co3max = watmax(co3)
sed_co3max = sedmax(co3)

camax = watmax(ca)
sed_camax = sedmax(ca)


fh.close()

class Window(QtGui.QDialog):
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
        self.button = QtGui.QPushButton('Plot T,S,Kz')
        self.button2 = QtGui.QPushButton('Plot Figure 2')   
        self.button0 = QtGui.QPushButton('Plot Figure 3')              
        self.button.clicked.connect(self.plot1)
        self.button2.clicked.connect(self.plot2)
        
        self.numdaySpinBox = QSpinBox()
        self.Daylabel = QLabel('Choose day to plot:')
        self.numdaySpinBox.setRange(1, 366)
        self.numdaySpinBox.setValue(100)
        self.button.clicked.connect(self.plot1)       

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,2,1,2)
        layout.addWidget(self.canvas,1,2,1,2)
        layout.addWidget(self.button0,4,2,1,1) 
        layout.addWidget(self.button,3,3,1,2)
        layout.addWidget(self.button2,4,3,1,2)        
#        layout.addWidget(self.Daylabel,1,2,1,2) #does not work well
        self.setLayout(layout)


    def plot1(self): # function to define 1 figure
#        plt.clf() #clear figure before updating 
#        style.use('ggplot')                 #use predefined style        
        gs = gridspec.GridSpec(3, 3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        ax00 = self.figure.add_subplot(gs[0]) # water

        ax10 = self.figure.add_subplot(gs[1])
        ax20 = self.figure.add_subplot(gs[2])
        
        ax01 = self.figure.add_subplot(gs[3])        
        ax11 = self.figure.add_subplot(gs[4])
        ax21 = self.figure.add_subplot(gs[5])  
             
        ax02 = self.figure.add_subplot(gs[6]) #sediment
        ax12 = self.figure.add_subplot(gs[7])
        ax22 = self.figure.add_subplot(gs[8])
      
        plt.text(1.1, 0.5,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes) 
                    
        def y_lim(axis): #function to define y limits 
            if axis in (ax00,ax10,ax20):   #water
                axis.set_ylim([y2min, 0])
                axis.fill_between(xticks, y1max, y1min, facecolor= wat_color, alpha=alpha_wat)
                axis.yaxis.grid(True,'minor')
                axis.xaxis.grid(True,'major')                
                axis.yaxis.grid(True,'major')                
            elif axis in (ax01,ax11,ax21):  #BBL
                axis.set_ylim([y2max, y2min])
                axis.fill_between(xticks, y2max_fill_water, y2min, facecolor= wat_color, alpha=alpha_wat) 
                axis.fill_between(xticks, y2max, y2min_fill_bbl, facecolor= bbl_color, alpha=alpha_bbl)
                axis.yaxis.grid(True,'minor')
                axis.yaxis.grid(True,'major')   
                axis.xaxis.grid(True,'major')    
                plt.setp(axis.get_xticklabels(), visible=False)                                           
            elif axis in (ax02,ax12,ax22): #sediment 
                axis.set_ylim([ysedmax, ysedmin])   #[y3max, y3min]   
                axis.fill_between(xticks, ysedmax_fill_bbl, ysedmin, facecolor= bbl_color, alpha=alpha_bbl)  
                axis.fill_between(xticks, ysedmax, ysedmin_fill_sed, facecolor= sed_color, alpha=alpha_sed)    
                axis.yaxis.set_major_locator(majorLocator)   #define yticks
                axis.yaxis.set_major_formatter(majorFormatter)
                axis.yaxis.set_minor_locator(minorLocator)
                axis.yaxis.grid(True,'minor')
                axis.yaxis.grid(True,'major')
                axis.xaxis.grid(True,'major')                 

        ax00.set_xlabel('Temperature',fontsize=14) 
        ax10.set_xlabel('Salinity',fontsize=14)   
        ax20.set_xlabel('Kz',fontsize=14)                                                                                                           
        ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        ax01.set_ylabel('Depth (m)',fontsize=14)   
        ax02.set_ylabel('Depth (cm)',fontsize=14)                

         
        #call function to define limits for all axis        
        #water subplots 
        y_lim(ax00) 
        y_lim(ax10) 
        y_lim(ax20) 
        y_lim(ax01)         
        y_lim(ax11) 
        y_lim(ax21) 
        #bbl subplots                
     
        #sediment subplots        
        y_lim(ax02) 
        y_lim(ax12)         
        y_lim(ax22) 
                                     

        for axis in (ax00,ax01,ax02,ax10,ax11,ax12,ax20,ax21,ax22): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (ax00, ax01, ax02):   
            axis.set_xlim([tempmin,tempmax])
            axis.set_xticks(np.arange(np.round(tempmin),np.ceil(tempmax)),((np.ceil(tempmax)-np.round(tempmin))/2))
        for axis in (ax10, ax11, ax12):  
            axis.set_xlim([salmin,salmax])
            
        for axis in (ax20, ax21, ax22):   
            axis.set_xlim([kzmin,kzmax])
            print 'kzmax',kzmax
#            axis.set_xticks(np.arange(kzmin,0.75,0.25))          
              
        spring_autumn = '#cecebd'#'#ffffd1'#'#e5e5d2'  
        winter = '#8dc0e7' 
        summer = '#d0576f'                              
        for n in range(0,365):  
            if n >= 0 and n <= 90:      #Winter                                 
                ax00.plot(temp[n],depth,winter,linewidth=0.7)             
                ax01.plot(temp[n],depth,winter,linewidth=0.7)  
                ax02.plot(temp[n],depth_sed,winter,linewidth=0.7)                 
                ax10.plot(sal[n],depth,winter,linewidth=0.7)   
                ax11.plot(sal[n],depth,winter,linewidth=0.7)   
                ax12.plot(sal[n],depth_sed,winter,linewidth=0.7) 
                
                ax20.plot(kz[n],depth2,winter,linewidth=0.7) 
                ax21.plot(kz[n],depth2,winter,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,winter,linewidth=0.7)
            elif n >= 335 and n <365: #
                ax00.plot(temp[n],depth,winter,linewidth=0.7)             
                ax01.plot(temp[n],depth,winter,linewidth=0.7)  
                ax02.plot(temp[n],depth_sed,winter,linewidth=0.7)                 
                ax10.plot(sal[n],depth,winter,linewidth=0.7)   
                ax11.plot(sal[n],depth,winter,linewidth=0.7)   
                ax12.plot(sal[n],depth_sed,winter,linewidth=0.7) 
                
                ax20.plot(kz[n],depth2,winter,linewidth=0.7) 
                ax21.plot(kz[n],depth2,winter,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 240: #summer                 
                ax00.plot(temp[n],depth,summer,linewidth=0.7,alpha = 0.5)             
                ax01.plot(temp[n],depth,summer,linewidth=0.7,alpha = 0.5)  
                ax02.plot(temp[n],depth_sed,summer,linewidth=0.7, alpha = 0.5)                 
                ax10.plot(sal[n],depth,summer,linewidth=0.7,alpha = 0.5)   
                ax11.plot(sal[n],depth,summer,linewidth=0.7,alpha = 0.5)   
                ax12.plot(sal[n],depth_sed,summer,linewidth=0.7,alpha = 0.5)                 
                
                ax20.plot(kz[n],depth2,summer,linewidth=0.7) 
                ax21.plot(kz[n],depth2,summer,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,summer,linewidth=0.7)                
            else:   #Spring and autumn

                ax00.plot(temp[n],depth,spring_autumn, linewidth=0.7, alpha = 0.5)             
                ax01.plot(temp[n],depth,spring_autumn,linewidth=0.7, alpha = 0.5)  
                ax02.plot(temp[n],depth_sed,spring_autumn,linewidth=0.7, alpha = 0.5)                 
                ax10.plot(sal[n],depth,spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax11.plot(sal[n],depth,spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax12.plot(sal[n],depth_sed,spring_autumn,linewidth=0.7, alpha = 0.5)   

                ax20.plot(kz[n],depth2,spring_autumn,linewidth=0.7) 
                ax21.plot(kz[n],depth2,spring_autumn,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,spring_autumn,linewidth=0.7) 
        self.canvas.draw()


    def plot2(self): #main function to define figure

        self.canvas.draw()


 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    
    main = Window()
    main.show()

    sys.exit(app.exec_())