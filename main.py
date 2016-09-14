import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QSpinBox,QLabel
#from numpy import nan
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


values_summer=[]   # create empty matrix for storing data
f1 = None
try:
    f_summer = open('summer.txt', 'rb')   # Read file with summer water column data 
    for i in range(0,85):        
        line1 = f_summer.readline()
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
depth_summer = data_summer[0][1:]
pH_summer = data_summer[1][1:]
sal_summer = data_summer[2][1:]
na_summer = data_summer[3][1:]

so4_summer = data_summer[8][1:]
no3_summer = data_summer[9][1:]
no2_summer = data_summer[10][1:]
nh4_summer = data_summer[11][1:]
si_summer = data_summer[12][1:]

po4_summer = data_summer[14][1:]

mn_summer = data_summer[15][1:]
fe_summer = data_summer[16][1:]
date_summer = data_summer[17][1:]
sed_depth_summer = data_summer[18][1:]
h2s_summer = data_summer[19][1:]


values_winter=[]   # create empty matrix for storing data
f_winter = None
try:
    f_winter = open('winter.txt', 'rb')   
    for i in range(0,61):        
        line_winter = f_winter.readline()
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
depth_winter = data_winter[0][1:]
pH_winter = data_winter[1][1:]
sal_winter = data_winter[2][1:]
na_winter = data_winter[3][1:]
so4_winter = data_winter[8][1:]
no3_winter = data_winter[9][1:]
no2_winter = data_winter[10][1:]
nh4_winter = data_winter[11][1:]
si_winter = data_winter[12][1:]
po4_winter = data_winter[14][1:] 
mn_winter = data_winter[15][1:]
fe_winter = data_winter[16][1:]
date_winter = data_winter[17][1:]
sed_depth_winter = data_winter[18][1:]
h2s_winter = data_winter[19][1:]



so4_summermin = np.ceil(float(min(so4_summer)))
so4_wintermin = np.ceil(float(min(so4_winter)))
so4_lastmin = min(so4_summermin,so4_wintermin)
so4_summermax = np.ceil(float(max(so4_summer)))
po4_summermin = np.ceil(float(min(po4_summer)))
po4_summermax = np.ceil(float(max(po4_summer)))
pH_summermin = np.ceil(float(min(pH_summer)))
pH_summermax = np.ceil(float(max(pH_summer)))

#h2s_summermin = np.ceil(float(min(h2s_summer)))
#h2s_summermax = np.ceil(float(max(h2s_summer)))
no2_summermin = np.ceil(float(min(no2_summer)))
no2_summermax = np.ceil(float(max(no2_summer)))
no3_summermin = np.ceil(float(min(no3_summer)))
no3_summermax = np.ceil(float(max(no3_summer)))
nh4_summermin = np.ceil(float(min(nh4_summer)))
nh4_summermax = np.ceil(float(max(nh4_summer)))
si_summermin = np.ceil(float(min(si_summer)))
si_summermax = np.ceil(float(max(si_summer)))
mn_summermin = np.ceil(float(min(mn_summer)))
mn_summermax = np.ceil(float(max(mn_summer)))
fe_summermin = np.ceil(float(min(fe_summer)))
fe_summermax = np.ceil(float(max(fe_summer)))
#my_example_nc_file = 'BROM_out.nc'

values_o2=[]   # create empty matrix for storing data
fo2 = None
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
depth_o2 = data_o2[0][1:]
sed_depth_o2 = data_o2[1][1:]
o2_o2 = data_o2[2][1:]


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
depth_pH = data_pH[0][1:]
sed_depth_pH = data_pH[1][1:]
pH_pH = data_pH[2][1:]


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
depth_pH_winter = data_pH_winter[0][1:]
sed_depth_pH_winter = data_pH_winter[1][1:]
pH_pH_winter = data_pH_winter[2][1:]





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
no2 = fh.variables['NO2'][:,:,0]
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
        if depth2[n+1] - depth2[n] >= 0.5:
            pass
        elif depth2[n+1] - depth2[n] < 0.50:    
            y1max = (depth2[n])                               
            return y1max
            break
        
def calculate_nwatmax():
    for n in range(0,(len(depth2)-1)):
        if depth2[n+1] - depth2[n] >= 0.5:
            pass
        elif depth2[n+1] - depth2[n] < 0.50:    
            ny1max = n                               
            return ny1max
            break
      
def calculate_bblmax():
    for n in range(0,(len(depth2)-1)):
        if kz[1,n] == 0:
            y2max =depth2[n]         
            return y2max
            break        
def calculate_nbblmax():
    for n in range(0,(len(depth2)-1)):
        if kz[1,n] == 0:
#            y2max =depth2[n]         
            return n
            break  
         
def y2max_fill_water():
    for n in range(0,(len(depth2)-1)):
#        if depth[_]-depth[_?]
        if depth2[n+1] - depth2[n] >= 0.5:
            pass
        elif depth2[n+1] - depth2[n] < 0.50:
#            watmax =  depth[n],depth[n]-depth[n+1],n
            y2max_fill_water = depth2[n]            
            return y2max_fill_water
            break 
   
y1min = 0
y1max = calculate_watmax()
ny1max = calculate_nwatmax()
#y2min = y1max #109 #depth[len(depth[:])-19]#108.5
y2max = calculate_bblmax() #110.0 #(sed_wat interface)#depth[len(depth[:])-13]#
ny2max = calculate_nbblmax()
y2min = y2max - 2*(y2max - y1max)   #calculate the position of y2min, for catching part of BBL 
ny2min = ny2max - 2*(ny2max - ny1max) 

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
            return ysedmin
            break   
        
def calculate_sedmax():
    for n in range(0,(len(depth_sed)-1)):
        if kz[1,n] == 0:
            ysed = depth_sed[n]    
            ysedmax =  ysed + 10                
            return ysedmax
            break          

ysedmin = calculate_sedmin()
ysedmax = calculate_sedmax()    #10#depth[len(depth[:])-1]#110.1

xticks =(np.arange(0,100000))

wat_color = '#ffffff' #'#f9fafb'#'#c9ecfd' #colors for filling water,bbl and sedimnet 
bbl_color = '#ccd6de'#'#2873b8' 
sed_color = '#a3abb1' #'#7a8085' #666b6f '#'#916012'
alpha_wat = 0.3 # saturation of color (from 0 to 1) 
alpha_bbl = 0.3
alpha_sed = 0.5
alpha_autumn = 0.5

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


#numday = fh.variables['time'][:] 
def watmax(variable):
    n = variable[:,:ny2max].max()#+ ((variable[:,y1min:y2max].max())/10))                
    return n 

def watmin(variable):
    n = np.round(variable[:,0:ny2max].min())
    return n

#so4_summermin = np.ceil(float(min(so4_summer)))


def sedmax(variable):
    n = np.ceil(variable[:,ny2min:].max())# + ((variable[:,ysedmin:ysedmax].max()))) #np.ceil

    return n 

def sedmin(variable):
    n = variable[:,ny2min:].min()
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
no3min =  watmin(no3)
sed_no3max =  sedmax(no3)
sed_no3min =  sedmin(no3)

po4min =  watmin(po4)
po4max =  watmax(po4)
sed_po4max =  sedmax(po4)
sed_po4min =  sedmin(po4)

nh4max =  watmax(nh4)
nh4min =  watmin(nh4)
sed_nh4max =  sedmax(nh4)
sed_nh4min  =  sedmin(nh4)
ponmax = watmax(pon)
sed_ponmax = sedmax(pon)

donmax = watmax(don)
sed_donmax = sedmax(don)

o2max = watmax(o2)
o2min = 0#watmin(o2)
sed_o2max = sedmax(o2)
sed_o2min = 0#sedmin(o2)

mn2max = watmax(mn2)
mn2min = watmin(mn2)
sed_mn2max = sedmax(mn2)
sed_mn2min = sedmin(mn2)
mn3max = watmax(mn3)

sed_mn3max = sedmax(mn3)

mn4max = watmax(mn4)
sed_mn4max = sedmax(mn4)

h2smax = watmax(h2s)
h2smin= watmin(h2s)
sed_h2smax = sedmax(h2s)
sed_h2smin = sedmin(h2s)

mnsmax = watmax(mns)
sed_mnsmax = sedmax(mns)

mnco3max = watmax(mnco3)
sed_mnco3max = sedmax(mnco3)

fe2max = watmax(fe2)
fe2min = watmin(fe2)
sed_fe2max = sedmax(fe2)
sed_fe2min = sedmin(fe2)

fe3max = watmax(fe3)
sed_fe3max = sedmax(fe3)

fesmax = watmax(fes)
sed_fesmax = sedmax(fes)

feco3max = watmax(feco3)
sed_feco3max = sedmax(feco3)

no2max = watmax(no2)
no2min = watmin(no2)
sed_no2max = sedmax(no2)
sed_no2min = sedmin(no2)

s0max = watmax(s0)
sed_s0max = sedmax(s0)

s2o3max = watmax(s2o3)
sed_s2o3max = sedmax(s2o3)

so4max = watmax(so4)
sed_so4max = sedmax(so4)

so4min = watmin(so4)
sed_so4min = sedmin(so4)

simax = watmax(si)
simin = watmin(si)
sed_simax = sedmax(si)
sed_simin = sedmin(si)

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

phmax = round((ph[:,:ny2min].max()),1)#watmax(ph)
print phmax
phmin = watmin(ph)
sed_phmax = round((ph[:,ny2min:].max()),1)

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


fh.close() #Close the nc file

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
        self.button1 = QtGui.QPushButton('Plot PO4,SO4,H2S')         
        self.button2 = QtGui.QPushButton('Plot T,S,Kz')         
        self.button3 = QtGui.QPushButton('Plot NO2,NO3,NH4')   
        self.button4 = QtGui.QPushButton('Plot Si,pH')         
        self.button5 = QtGui.QPushButton('Plot Mn,Fe;O2')            
#        self.button6 = QtGui.QPushButton('Plot Figure 6')               
                            

        self.button1.clicked.connect(self.plot1) #Plot PO4,SO4,H2S 
        self.button2.clicked.connect(self.plot2) #Plot T,S,Kz
        self.button3.clicked.connect(self.plot3) #Plot NO2,NO3,NH4   
        self.button4.clicked.connect(self.plot4) #Plot Si,pH 
        self.button5.clicked.connect(self.plot5) #Plot Mn,Fe,O2   
                                        
        self.numdaySpinBox = QSpinBox()
        self.Daylabel = QLabel('Choose day to plot:')
        self.numdaySpinBox.setRange(1, 366)
        self.numdaySpinBox.setValue(100)      

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,2,1,2)       
        layout.addWidget(self.canvas,1,2,1,2)       
        layout.addWidget(self.button1,3,2,1,1)        
        layout.addWidget(self.button2,3,3,1,1)
        layout.addWidget(self.button3,3,4,1,1)            
        layout.addWidget(self.button4,4,2,1,1)         
        layout.addWidget(self.button5,4,3,1,1)  
#        layout.addWidget(self.button6,4,4,1,1)   
                     
 
        self.setLayout(layout)
        

    spring_autumn ='#998970'#'#cecebd'#'#ffffd1'#'#e5e5d2'  
    winter = '#8dc0e7' 
    summer = '#d0576f' 
    markersize=25
    linewidth = 0.5
    alpha = 0.5 
    def plot1(self): #function to define 1 figure PO4,SO4,H2S
        plt.clf() #clear figure before updating 
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
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)   
                    
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

        ax00.set_xlabel(r'$\rm PO _4 $',fontsize=14, fontweight='bold') 
        ax10.set_xlabel(r'$\rm SO _4 $',fontsize=14)   
        ax20.set_xlabel(r'$\rm H _2 S $',fontsize=14)                                                                                                           
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
            ax20.set_xticks(np.arange(0,2*kzmax),kzmax)      
        for axis in (ax00, ax01):   
            axis.set_xlim([po4min,po4max])
            axis.set_xticks(np.arange(np.round(po4min),np.ceil(po4max)),((np.ceil(po4max)-np.round(po4min))/2))
        ax02.set_xlim([sed_po4min,sed_po4max])    
        for axis in (ax10, ax11):
            watmin = min(so4_lastmin,so4min)
            axis.set_xlim([watmin,so4max])
        ax12.set_xlim([sed_so4min,sed_so4max])    
            
        for axis in (ax20, ax21):   
            axis.set_xlim([h2smin,h2smax])
        ax22.set_xlim([sed_h2smin,sed_h2smax]) 
#            axis.set_xticks(np.arange(h2smin,0.75,0.25))          

# Plot Field data        

                        
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                ax00.plot(po4[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(po4[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(po4[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(so4[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(h2s[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(h2s[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(h2s[n],depth_sed,self.winter,linewidth=0.7)
                
            elif n >= 22 and n <= 90:      #Winter                                 
                ax00.plot(po4[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(po4[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(po4[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(so4[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(h2s[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(h2s[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(h2s[n],depth_sed,self.winter,linewidth=0.7)
                                
            elif n>=19 and n<=21: #winter to compare with field data
                ax00.plot(po4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)             
                ax01.plot(po4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)  
                ax02.plot(po4[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=8)                 
                ax10.plot(so4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax11.plot(so4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax12.plot(so4[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
                ax20.plot(h2s[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax21.plot(h2s[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   #marker='o',
                ax22.plot(h2s[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8) #marker='o',                 
                
            elif n >= 335 and n <365: #
                ax00.plot(po4[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(po4[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(po4[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(so4[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(so4[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(h2s[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(h2s[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(h2s[n],depth_sed,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 236: #self.summer                 
                ax00.plot(po4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                ax01.plot(po4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                ax02.plot(po4[n],depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                ax10.plot(so4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax11.plot(so4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax12.plot(so4[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax20.plot(h2s[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax21.plot(h2s[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                ax22.plot(h2s[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
            elif n >= 236 and n < 240: #from 25 to 30 august               
                ax00.plot(po4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
                ax01.plot(po4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
                ax02.plot(po4[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(so4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(so4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(so4[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
                ax20.plot(h2s[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax21.plot(h2s[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax22.plot(h2s[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                
            else:   #Spring and autumn

                ax00.plot(po4[n],depth,self.spring_autumn, linewidth=0.7, alpha = 0.5)             
                ax01.plot(po4[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)  
                ax02.plot(po4[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)                 
                ax10.plot(so4[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax11.plot(so4[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax12.plot(so4[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax20.plot(h2s[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                ax21.plot(h2s[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  #
                ax22.plot(h2s[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                    
        ax00.scatter(po4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax10.scatter(so4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax20.scatter(h2s_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                                     
        ax01.scatter(po4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax11.scatter(so4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax21.scatter(h2s_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                   
        ax02.scatter(po4_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        ax12.scatter(so4_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)    
        ax22.scatter(h2s_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        
        ax00.scatter(po4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax10.scatter(so4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax20.scatter(h2s_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                       
        ax01.scatter(po4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        ax11.scatter(so4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        ax21.scatter(h2s_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax02.scatter(po4_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)       
        ax12.scatter(so4_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        ax22.scatter(h2s_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        
                                                              
        self.canvas.draw()     
        
    def plot2(self): # function to define 2 figure T,S,Kz  
        plt.clf() #clear figure before updating         
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
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)   
                    
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
            axis.set_xticks(np.arange(0,(round(kzmax+(kzmax/2.),5)),kzmax/2.))   
#            axis.set_xticks(np.arange(kzmin,0.75,0.25))          
              
                             
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                ax00.plot(temp[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(temp[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(temp[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(sal[n],depth_sed,self.winter,linewidth=0.7)     
                ax20.plot(kz[n],depth2,self.winter,linewidth=0.7) 
                ax21.plot(kz[n],depth2,self.winter,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,self.winter,linewidth=0.7)
            elif n >= 22 and n <= 90:      #Winter                                 
                ax00.plot(temp[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(temp[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(temp[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(sal[n],depth_sed,self.winter,linewidth=0.7)     
                ax20.plot(kz[n],depth2,self.winter,linewidth=0.7) 
                ax21.plot(kz[n],depth2,self.winter,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,self.winter,linewidth=0.7)                
                
            elif n>=19 and n<=21: #winter to compare with field data
                ax00.plot(temp[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)             
                ax01.plot(temp[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)  
                ax02.plot(temp[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=8)                 
                ax10.plot(sal[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax11.plot(sal[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax12.plot(sal[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
                ax20.plot(kz[n],depth2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax21.plot(kz[n],depth2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   #marker='o',
                ax22.plot(kz[n],depth_sed2,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8) #marker='o',                   
                
                
            elif n >= 335 and n <365: #
                ax00.plot(temp[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(temp[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(temp[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(sal[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(sal[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(kz[n],depth2,self.winter,linewidth=0.7) 
                ax21.plot(kz[n],depth2,self.winter,linewidth=0.7)  #
                ax22.plot(kz[n],depth_sed2,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 236: #self.summer                 
                ax00.plot(temp[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                ax01.plot(temp[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                ax02.plot(temp[n],depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                ax10.plot(sal[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax11.plot(sal[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax12.plot(sal[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax20.plot(kz[n],depth2,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax21.plot(kz[n],depth2,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                ax22.plot(kz[n],depth_sed2,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
            elif n >= 236 and n < 240: #from 25 to 30 august ( to compare with field data)                
                ax00.plot(temp[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--', zorder=9) #marker='o',     
                ax01.plot(temp[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  #marker='o',
                ax02.plot(temp[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(sal[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(sal[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(sal[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
                ax20.plot(kz[n],depth2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax21.plot(kz[n],depth2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax22.plot(kz[n],depth_sed2,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                
            else:   #Spring and autumn
                ax00.plot(temp[n],depth,self.spring_autumn, linewidth=0.7, alpha = alpha_autumn)             
                ax01.plot(temp[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  
                ax02.plot(temp[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)                 
                ax10.plot(sal[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)   
                ax11.plot(sal[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)   
                ax12.plot(sal[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)   
                ax20.plot(kz[n],depth2,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                ax21.plot(kz[n],depth2,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  #
                ax22.plot(kz[n],depth_sed2,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                
        ax10.scatter(sal_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        ax10.scatter(sal_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        ax11.scatter(sal_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax11.scatter(sal_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        ax12.scatter(sal_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)   
        ax12.scatter(sal_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
                              
        self.canvas.draw()
        
    def plot3(self): #function to define 1 figure NO2,NO3,NH4
        plt.clf() #clear figure before updating 
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

             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)        
                            
        def y_lim(axis): #function to define y limits 
            if axis in (ax00,ax10,ax20):   #water
                axis.set_ylim([y2min, 0])
                axis.fill_between(xticks, y1max, y1min, facecolor= wat_color, alpha=alpha_wat)
                axis.yaxis.grid(True,'minor') #add grid to plot 
                axis.xaxis.grid(True,'major') #add grid to plot                
                axis.yaxis.grid(True,'major') #add grid to plot                 
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

        ax00.set_xlabel(r'$\rm NO _2 $',fontsize=14, fontweight='bold') 
        ax10.set_xlabel(r'$\rm NO _3 $',fontsize=14)   
        ax20.set_xlabel(r'$\rm NH _4 $',fontsize=14)                                                                                                           
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
        for axis in (ax00, ax01):   
            axis.set_xlim([no2min,no2max])
            axis.set_xticks(np.arange(np.round(no2min),np.ceil(no2max)),((np.ceil(no2max)-np.round(no2min))/2))
        ax02.set_xlim([sed_no2min,sed_no2max])    
        for axis in (ax10, ax11):
            watmin = min(no3_summermin,no3min)
            axis.set_xlim([watmin,no3max])
        ax12.set_xlim([sed_no3min,sed_no3max])    
            
        for axis in (ax20, ax21):   
            axis.set_xlim([nh4min,nh4max])
        ax22.set_xlim([sed_nh4min,sed_nh4max]) 
#            axis.set_xticks(np.arange(nh4min,0.75,0.25))          
    

                        
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                ax00.plot(no2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(no2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(no2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(no3[n],depth_sed,self.winter,linewidth=0.7)         
                ax20.plot(nh4[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(nh4[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(nh4[n],depth_sed,self.winter,linewidth=0.7)
                
            elif n >= 22 and n <= 90:      #Winter                                 
                ax00.plot(no2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(no2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(no2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(no3[n],depth_sed,self.winter,linewidth=0.7)         
                ax20.plot(nh4[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(nh4[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(nh4[n],depth_sed,self.winter,linewidth=0.7)                
                
                
            elif n>=19 and n<=21: #winter to compare with field data
                ax00.plot(no2[n],depth,'#4e9dda',linewidth=3,alpha = 0.5,linestyle= '--',zorder=5)             
                ax01.plot(no2[n],depth,'#4e9dda',linewidth=3,alpha = 0.5,linestyle= '--',zorder=5)  
                ax02.plot(no2[n],depth_sed,'#4e9dda',linewidth=3, alpha = 0.5,linestyle= '--',zorder=5)                 
                ax10.plot(no3[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax11.plot(no3[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax12.plot(no3[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)       
                ax20.plot(nh4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   
                ax21.plot(nh4[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8)   #marker='o',
                ax22.plot(nh4[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=8) #marker='o',                   
                
                
                
                
                
            elif n >= 335 and n <365: #
                ax00.plot(no2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(no2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(no2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(no3[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(no3[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(nh4[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(nh4[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(nh4[n],depth_sed,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 236: #self.summer                 
                ax00.plot(no2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                ax01.plot(no2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                ax02.plot(no2[n],depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                ax10.plot(no3[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax11.plot(no3[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax12.plot(no3[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax20.plot(nh4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax21.plot(nh4[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                ax22.plot(nh4[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
            elif n >= 236 and n < 240: #from 25 to 30 august               
                ax00.plot(no2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
                ax01.plot(no2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
                ax02.plot(no2[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(no3[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(no3[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(no3[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
                ax20.plot(nh4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax21.plot(nh4[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax22.plot(nh4[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                                  
                         
            else:   #Spring and autumn

                ax00.plot(no2[n],depth,self.spring_autumn, linewidth=0.7, alpha = alpha_autumn)             
                ax01.plot(no2[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  
                ax02.plot(no2[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)                 
                ax10.plot(no3[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  
                 
                ax11.plot(no3[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)   
                ax12.plot(no3[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)   

                ax20.plot(nh4[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                ax21.plot(nh4[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  #
                ax22.plot(nh4[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                
        # Field data        
        ax00.scatter(no2_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax00.scatter(no2_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        ax01.scatter(no2_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax01.scatter(no2_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                                             
        ax02.scatter(no2_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)     
        ax02.scatter(no2_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
                   
        ax10.scatter(no3_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax10.scatter(no3_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        ax11.scatter(no3_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax11.scatter(no3_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
                  
        ax12.scatter(no3_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)      
        ax12.scatter(no3_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
                                 
        ax20.scatter(nh4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax20.scatter(nh4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        ax21.scatter(nh4_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 
        ax21.scatter(nh4_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
               
        ax22.scatter(nh4_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax22.scatter(nh4_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                  
   
                                                
        self.canvas.draw()

    def plot4(self): #function to define 1 figure Si,pH
        plt.clf() #clear figure before updating 

        alpha_autumn = 0.5
        gs = gridspec.GridSpec(3, 2) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04, wspace=0.2,hspace=0.1)
   
        self.figure.patch.set_facecolor('white')  #Set the background
        #create subplots
        ax00 = self.figure.add_subplot(gs[0]) # water
        ax10 = self.figure.add_subplot(gs[1])
#        ax20 = self.figure.add_subplot(gs[2])
        
        ax01 = self.figure.add_subplot(gs[2])        
        ax11 = self.figure.add_subplot(gs[3])
#        ax21 = self.figure.add_subplot(gs[5])  
             
        ax02 = self.figure.add_subplot(gs[4]) #sediment
        ax12 = self.figure.add_subplot(gs[5])
#        ax22 = self.figure.add_subplot(gs[8])
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax10.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax11.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax11.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax12.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax12.transAxes)  
                    
        def y_lim(axis): #function to define y limits 
            if axis in (ax00,ax10):   #water
                axis.set_ylim([y2min, 0])
                axis.fill_between(xticks, y1max, y1min, facecolor= wat_color, alpha=alpha_wat)
                axis.yaxis.grid(True,'minor')
                axis.xaxis.grid(True,'major')                
                axis.yaxis.grid(True,'major')                
            elif axis in (ax01,ax11):  #BBL
                axis.set_ylim([y2max, y2min])
                axis.fill_between(xticks, y2max_fill_water, y2min, facecolor= wat_color, alpha=alpha_wat) 
                axis.fill_between(xticks, y2max, y2min_fill_bbl, facecolor= bbl_color, alpha=alpha_bbl)
                axis.yaxis.grid(True,'minor')
                axis.yaxis.grid(True,'major')   
                axis.xaxis.grid(True,'major')    
                plt.setp(axis.get_xticklabels(), visible=False)                                           
            elif axis in (ax02,ax12): #sediment 
                axis.set_ylim([ysedmax, ysedmin])   #[y3max, y3min]   
                axis.fill_between(xticks, ysedmax_fill_bbl, ysedmin, facecolor= bbl_color, alpha=alpha_bbl)  
                axis.fill_between(xticks, ysedmax, ysedmin_fill_sed, facecolor= sed_color, alpha=alpha_sed)    
                axis.yaxis.set_major_locator(majorLocator)   #define yticks
                axis.yaxis.set_major_formatter(majorFormatter)
                axis.yaxis.set_minor_locator(minorLocator)
                axis.yaxis.grid(True,'minor')
                axis.yaxis.grid(True,'major')
                axis.xaxis.grid(True,'major')                 

        ax00.set_xlabel(r'$\rm Si $',fontsize=14, fontweight='bold') 
        ax10.set_xlabel(r'$\rm pH $',fontsize=14)   
#        ax20.set_xlabel(r'$\rm NH _4 $',fontsize=14)                                                                                                           
        ax00.set_ylabel('Depth (m)',fontsize=14) #Label y axis
        ax01.set_ylabel('Depth (m)',fontsize=14)   
        ax02.set_ylabel('Depth (cm)',fontsize=14)                

         
        #call function to define limits for all axis        
        #water subplots 
        y_lim(ax00) 
        y_lim(ax10) 
#        y_lim(ax20) 
        y_lim(ax01)         
        y_lim(ax11) 
#        y_lim(ax21) 
        #bbl subplots                
     
        #sediment subplots        
        y_lim(ax02) 
        y_lim(ax12)         
#        y_lim(ax22) 
                                     

        for axis in (ax00,ax01,ax02,ax10,ax11,ax12): 
            axis.xaxis.set_label_position('top')
            axis.xaxis.tick_top()
        for axis in (ax00, ax01):   
            axis.set_xlim([simin,simax])
            axis.set_xticks(np.arange(np.round(simin),np.ceil(simax)),((np.ceil(simax)-np.round(simin))/2))
        ax02.set_xlim([sed_simin,sed_simax])    
        for axis in (ax10, ax11):
#            watmin = min(pH_summermin,phmin)
            axis.set_xlim([phmin,phmax+0.1])
#            axis.set_xticks(np.arange(np.round(phmin),np.ceil(simax)),((np.ceil(simax)-np.round(simin))/2))            
        ax12.set_xlim([sed_phmin,sed_phmax+0.3])    
                   

# Plot Field data        

                    
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                ax00.plot(si[n],depth,self.winter,linewidth=self.linewidth)             
                ax01.plot(si[n],depth,self.winter,linewidth=self.linewidth)  
                ax02.plot(si[n],depth_sed,self.winter,linewidth=self.linewidth)                 
                ax10.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax11.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax12.plot(ph[n],depth_sed,self.winter,linewidth=self.linewidth) 
                
            if n >= 22 and n <= 90:      #Winter                                 
                ax00.plot(si[n],depth,self.winter,linewidth=self.linewidth)             
                ax01.plot(si[n],depth,self.winter,linewidth=self.linewidth)  
                ax02.plot(si[n],depth_sed,self.winter,linewidth=self.linewidth)                 
                ax10.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax11.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax12.plot(ph[n],depth_sed,self.winter,linewidth=self.linewidth) 

            elif n>=19 and n<=21: #winter to compare with field data
                ax00.plot(si[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
                ax01.plot(si[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
                ax02.plot(si[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(ph[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(ph[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(ph[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)       

                
            elif n >= 335 and n <365: #
                ax00.plot(si[n],depth,self.winter,linewidth=self.linewidth)             
                ax01.plot(si[n],depth,self.winter,linewidth=self.linewidth)  
                ax02.plot(si[n],depth_sed,self.winter,linewidth=self.linewidth)                 
                ax10.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax11.plot(ph[n],depth,self.winter,linewidth=self.linewidth)   
                ax12.plot(ph[n],depth_sed,self.winter,linewidth=self.linewidth) 
                
                             
            elif n >= 150 and n < 236: #self.summer                 
                ax00.plot(si[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                ax01.plot(si[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                ax02.plot(si[n],depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                ax10.plot(ph[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax11.plot(ph[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax12.plot(ph[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                
            elif n >= 236 and n < 240: #from 25 to 30 august               
                ax00.plot(si[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
                ax01.plot(si[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
                ax02.plot(si[n],depth_sed,self.summer,linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(ph[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(ph[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(ph[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)                              

            else:   #Spring and autumn

                ax00.plot(si[n],depth,self.spring_autumn, linewidth=self.linewidth, alpha = alpha_autumn)             
                ax01.plot(si[n],depth,self.spring_autumn,linewidth=self.linewidth, alpha = alpha_autumn)  
                ax02.plot(si[n],depth_sed,self.spring_autumn,linewidth=self.linewidth, alpha = alpha_autumn)                 
                ax10.plot(ph[n],depth,self.spring_autumn,linewidth=self.linewidth, alpha = alpha_autumn)   
                ax11.plot(ph[n],depth,self.spring_autumn,linewidth=self.linewidth, alpha = alpha_autumn)   
                ax12.plot(ph[n],depth_sed,self.spring_autumn,linewidth=self.linewidth, alpha = alpha_autumn)
      

#        ax00.plot(si_summer,depth_summer,'ro',line_width = 1.5, markersize = self.markersize,linewidth=0.7) 
#       plt.scatter(si_summer,depth_summer, s= 50, c= 'r', alpha=0.5)
        #zorder moves plot to the top layer      
        ax00.scatter(si_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        ax01.scatter(si_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax02.scatter(si_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                
        ax10.scatter(pH_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)
        ax10.scatter(pH_pH,depth_pH,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)   
        ax10.scatter(pH_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.5,zorder=10)            
        ax11.scatter(pH_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)    
        ax11.scatter(pH_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)            
        ax11.scatter(pH_pH,depth_pH,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        ax11.scatter(pH_pH_winter,depth_pH_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10)                          
        ax12.scatter(pH_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        ax12.scatter(pH_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10)           
        ax12.scatter(pH_pH,sed_depth_pH,color='r' , alpha=1,edgecolor='#262626',
                     s = 15,linewidth=0.1,zorder=10) 
        ax12.scatter(pH_pH_winter,sed_depth_pH_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
                        
#        depth_pH = data_pH[0][1:]
#sed_depth_pH = data_pH[1][1:]
#pH_pH = data_pH[2][1:]                          
        self.canvas.draw()

    def plot5(self): #function to define Mn,fe,O2
        plt.clf() #clear figure before updating 
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
      
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax20.transAxes) 

        plt.text(1.1, 0.4,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes)
             
        plt.text(1.1, 0.7,'Water ', fontweight='bold', # draw legend to Water
        bbox={'facecolor': wat_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax21.transAxes) 
                    
        plt.text(1.1, 0.7,'BBL', fontweight='bold', # draw legend to Water
        bbox={'facecolor': bbl_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)

        plt.text(1.1, 0.4,'Sediment', fontweight='bold', # draw legend to Water
        bbox={'facecolor': sed_color, 'alpha':0.5, 'pad':10}, fontsize=14, rotation=90, 
        transform=ax22.transAxes)   
                    
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

        ax00.set_xlabel(r'$\rm Mn $',fontsize=14, fontweight='bold') 
        ax10.set_xlabel(r'$\rm Fe $',fontsize=14)   
        ax20.set_xlabel(r'$\rm O _2 $',fontsize=14)                                                                                                           
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
        for axis in (ax00, ax01):   
            axis.set_xlim([mn2min,5])
            axis.set_xticks(np.arange(np.round(mn2min),np.ceil(mn2max)),((np.ceil(mn2max)-np.round(mn2min))/2))
        ax02.set_xlim([sed_mn2min,31])    
        for axis in (ax10, ax11):
            watmin = min(fe_summermin,fe2min)
            axis.set_xlim([watmin,5])#fe2max
        ax12.set_xlim([sed_fe2min,60])    
            
        for axis in (ax20, ax21):   
            axis.set_xlim([o2min,o2max])
        ax22.set_xlim([sed_o2min,sed_o2max]) 
#            axis.set_xticks(np.arange(o2min,0.75,0.25))          

# Plot Field data        

                        
        for n in range(0,365):  
            if n >= 0 and n <= 18:      #Winter                                 
                ax00.plot(mn2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(mn2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(mn2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(fe2[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(o2[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(o2[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(o2[n],depth_sed,self.winter,linewidth=0.7)
                
            elif n >= 22 and n <= 90:      #Winter                                 
                ax00.plot(mn2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(mn2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(mn2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(fe2[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(o2[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(o2[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(o2[n],depth_sed,self.winter,linewidth=0.7)      
                          
            elif n>=19 and n<=21: #winter to compare with field data
                ax00.plot(mn2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)             
                ax01.plot(mn2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)  
                ax02.plot(mn2[n],depth_sed,'#4e9dda',linewidth=3, alpha = 1,linestyle= '--',zorder=9)                 
                ax10.plot(fe2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(fe2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(fe2[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
                ax20.plot(o2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax21.plot(o2[n],depth,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9)   #marker='o',
                ax22.plot(o2[n],depth_sed,'#4e9dda',linewidth=3,alpha = 1,linestyle= '--',zorder=9) #marker='o',                     
                
            elif n >= 335 and n <365: #
                ax00.plot(mn2[n],depth,self.winter,linewidth=0.7)             
                ax01.plot(mn2[n],depth,self.winter,linewidth=0.7)  
                ax02.plot(mn2[n],depth_sed,self.winter,linewidth=0.7)                 
                ax10.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax11.plot(fe2[n],depth,self.winter,linewidth=0.7)   
                ax12.plot(fe2[n],depth_sed,self.winter,linewidth=0.7) 
                
                ax20.plot(o2[n],depth,self.winter,linewidth=0.7) 
                ax21.plot(o2[n],depth,self.winter,linewidth=0.7)  #
                ax22.plot(o2[n],depth_sed,self.winter,linewidth=0.7)   
                             
            elif n >= 150 and n < 236: #self.summer                 
                ax00.plot(mn2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)             
                ax01.plot(mn2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  
                ax02.plot(mn2[n],depth_sed,self.summer,linewidth=self.linewidth, alpha = self.alpha)                 
                ax10.plot(fe2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax11.plot(fe2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)   
                ax12.plot(fe2[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax20.plot(o2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha) 
                ax21.plot(o2[n],depth,self.summer,linewidth=self.linewidth,alpha = self.alpha)  #
                ax22.plot(o2[n],depth_sed,self.summer,linewidth=self.linewidth,alpha = self.alpha)              
                
            elif n >= 236 and n < 240: #from 25 to 30 august               
                ax00.plot(mn2[n],depth,self.summer,linewidth=self.linewidth,zorder=9)             
                ax01.plot(mn2[n],depth,self.summer,linewidth=self.linewidth)  
                ax02.plot(mn2[n],depth_sed,self.summer,linewidth= self.linewidth)                 
                ax10.plot(fe2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax11.plot(fe2[n],depth,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)   
                ax12.plot(fe2[n],depth_sed,self.summer,linewidth=3,alpha = 1,linestyle= '--',zorder=9)       
                ax20.plot(o2[n],depth,self.summer,linewidth=self.linewidth)   
                ax21.plot(o2[n],depth,self.summer,linewidth=self.linewidth)   #marker='o',
                ax22.plot(o2[n],depth_sed,self.summer,linewidth=self.linewidth) #marker='o',                                  
                         
            else:   #Spring and autumn

                ax00.plot(mn2[n],depth,self.spring_autumn, linewidth=0.7, alpha = 0.5)             
                ax01.plot(mn2[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)  
                ax02.plot(mn2[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)                 
                ax10.plot(fe2[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)  
                 
                ax11.plot(fe2[n],depth,self.spring_autumn,linewidth=0.7, alpha = 0.5)   
                ax12.plot(fe2[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = 0.5)   

                ax20.plot(o2[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                ax21.plot(o2[n],depth,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn)  #
                ax22.plot(o2[n],depth_sed,self.spring_autumn,linewidth=0.7, alpha = alpha_autumn) 
                
                
        ax00.scatter(mn_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax01.scatter(mn_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                               
        ax02.scatter(mn_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)    
        ax00.scatter(mn_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax01.scatter(mn_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)                               
        ax02.scatter(mn_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)         
        
        
              
        ax10.scatter(fe_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)
        ax10.scatter(fe_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)      
          
        ax11.scatter(fe_summer,depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax12.scatter(fe_summer,sed_depth_summer,color='r' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10) 

        ax11.scatter(fe_winter,depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)  
        ax12.scatter(fe_winter,sed_depth_winter,color='b' , alpha=1,edgecolor='#262626',
                     s = self.markersize,linewidth=0.5,zorder=10)        
        
                             
        ax20.scatter(o2_o2,depth_o2,color='r' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        ax21.scatter(o2_o2,depth_o2,color='r' , alpha=1,edgecolor='#262626',
                     s = 5,linewidth=0.1,zorder=10) 
        ax22.scatter(o2_o2,sed_depth_o2,color='r' ,alpha=1,edgecolor='#262626',
                     s = 5 ,linewidth=0.1,zorder=10)  
               
   
                                                
        self.canvas.draw() 
        
        
        
#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111)
#for n in range(0,365):                               
#    ax2.plot(o2[n],depth,color='r', marker = 'o', linewidth=0.1)
#ax2.set_ylim([5.95, 5.88])
#ax2.yaxis.grid(True,'major')
#ax2.yaxis.grid(True,'minor')
#ax2.xaxis.grid(True,'major')
#plt.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    
    main = Window()
    main.show()

    sys.exit(app.exec_())