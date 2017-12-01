#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 14. des. 2016

@author: E.Protsenko
'''


import os,sys
import numpy as np
from netCDF4 import Dataset 
#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets,QtGui, QtCore

from matplotlib import rc
#from matplotlib.backends.backend_qt4agg import (
#    FigureCanvasQTAgg as FigureCanvas)
#from matplotlib.backends.backend_qt4agg import (
#    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)

from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.pyplot as plt


import readdata
import time_plot 
import dist_plot
import fluxes_plot
import all_year_1d
import help_dialog


class Window(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # function to display the names of the window flags        
        # Qt.Window Indicates that the widget is a window, 
        # usually with a window system frame and a title bar
        # ! it is not possible to unset this flag if the widget 
        # does not have a parent.
        
        self.setWindowFlags(QtCore.Qt.Window)   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo2.png'))       
        self.figure = plt.figure(figsize=(6.69 , 5.27), dpi=100,
                                  facecolor='white') 
                
        # open file system to choose needed nc file 
        
        #self.fname = str(QtWidgets.QFileDialog.getOpenFileName(self,
        #'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)")) 
        
        self.fname ,_  = (QtWidgets.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))  #str


          
        totitle = os.path.split(self.fname)[1]
        #self.totitle = totitle[16:-3]
        self.setWindowTitle("BROM Pictures ("+str(totitle)+')')     
        readdata.readdata_brom(self,self.fname)    
         
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self) 
                
        # Create widgets
        self.label_choose_var = QtWidgets.QLabel('Choose variable:')                   

        self.qlistwidget = QtWidgets.QListWidget()      
        self.qlistwidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.all_year_box = QtWidgets.QComboBox()                                      
        self.dist_prof_button = QtWidgets.QPushButton()           
        #self.injlines_checkbox = QtWidgets.QCheckBox(
        #    'Draw inject lines')                     
        self.time_prof_last_year =  QtWidgets.QPushButton()    
        self.time_prof_all =  QtWidgets.QPushButton()  
        
        #self.time_prof_box = QtWidgets.QComboBox()  
                                 
        self.all_year_button =  QtWidgets.QPushButton()                                  
        self.fick_box = QtWidgets.QPushButton() 
        self.help_button = QtWidgets.QPushButton(' ')
        

        
        ## add only 2d arrays to variables list       
        ## We skip z and time since they are 1d array, 
        ## we need to know the shape of other arrays
        ## If the file includes other 1d var, it 
        ## could raise an err, such var should be skipped also
        
        self.fh =  Dataset(self.fname)
        
        #def testvar(self):                    
        readdata.read_num_col(self,self.fname)
            #max_num_col = self.testvar.shape[0]
            #return (self.testvar)
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self)        
                
        if 'i' in self.names_vars: 
            self.dist = np.array(self.fh.variables['i'])  
                    
        # sort variables alphabetically non-case sensitive        
        self.sorted_names =  sorted(self.names_vars, key=lambda s: s.lower())  
        self.qlistwidget.addItems(self.sorted_names)
        
        self.fh.close()
        
       #print (max_num_col)        
               
        if 'i' in self.names_vars:                        
            self.numcol_2d.setRange(0, int(self.testvar.shape[0]-1))               
            self.numday_box.setRange(0, self.lentime-1)              
            self.numday_stop_box.setRange(0, self.lentime-1)             
            self.numday_stop_box.setValue(self.lentime-1)

        self.time_prof_all.setText('Time: all year')
        self.fick_box.setText('Fluxes SWI')
        self.all_year_button.setText('1D plot')
        self.time_prof_last_year.setText('Time: last year')               
        self.dist_prof_button.setText('Show Dist Profile')  
           
        ### Define connection between clicking the button and 
        ### calling the function to plot figures         
                                 
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.all_year_button.released.connect(self.call_all_year)
        self.time_prof_all.released.connect(self.call_print_allyr)        
        self.fick_box.released.connect(self.call_fluxes)        
        self.dist_prof_button.released.connect(self.call_print_dist)                             
        self.help_button.released.connect(self.call_help)
                  
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
        self.canvas.setMinimumSize(self.canvas.size())
        
        ## The QGridLayout class lays out widgets in a grid          
        self.grid = QtWidgets.QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self,self.fname)   
                 
        if 'Kz'  in self.names_vars :
            readdata.calculate_ywat(self)
            readdata.calculate_ybbl(self)   
            readdata.y2max_fill_water(self)
            readdata.depth_sed(self)
            readdata.calculate_ysed(self)
            readdata.calculate_ysed(self)
            readdata.calc_nysedmin(self)  
            readdata.y_coords(self)        
        else: 
            self.sediment = False
           
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
        self.num = 50. 
        
    def call_all_year(self):    
        all_year_1d.plot(self)
        
    def call_fluxes(self):    
        fluxes_plot.fluxes(self)
        
    def call_print_dist(self): 
        dist_plot.dist_profile(self)
            
    def call_print_lyr(self): 
        stop = len(self.time)
        start = stop - 365
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop) 
            
    def call_print_allyr(self):  
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value()  
        #stop = len(self.time)
        #start = 0
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop)   
                       

   
   
    def call_help(self):
        help_dialog.show(self) 

        
def createDistGroup(self):  
        
    self.dist_groupBox = QtWidgets.QGroupBox("Distance axis")  
         
    self.dist_grid = QtWidgets.QGridLayout(self.dist_groupBox)
    
    self.col_label = QtWidgets.QLabel('Column: ')
    self.numcol_2d = QtWidgets.QSpinBox() 
    readdata.read_num_col(self,self.fname)
    self.label_maxcol = QtWidgets.QLabel('max\ncolumn: '+ str(self.testvar.shape[0]-1)) 

    #max_col = readdata.read_num_col(self,self.fname)
    #self.label_maxcol_n = QtWidgets.QLabel('max\ncolumn: ') #+ str(testvar.shape[0]-1))      
    
    self.dist_grid.addWidget(self.col_label,0,0,1,1) 
    self.dist_grid.addWidget(self.numcol_2d,1,0,1,1) 
    self.dist_grid.addWidget(self.label_maxcol,1,1,1,1) 
    
       
def createTimeGroup(self):  
     
    self.last_year_button = QtWidgets.QPushButton('last year')    
    self.time_groupBox = QtWidgets.QGroupBox(" Time axis")        
    self.label_maxday_label = QtWidgets.QLabel('max day: ')
    self.label_maxday = QtWidgets.QLabel(str(self.lentime-1))    
    self.numday_start_label = QtWidgets.QLabel('start: ') 
    self.numday_box = QtWidgets.QSpinBox()     
    self.numday_stop_label = QtWidgets.QLabel('stop: ') 
    self.numday_stop_box = QtWidgets.QSpinBox()    

    self.time_grid = QtWidgets.QGridLayout(self.time_groupBox)   

    #self.time_grid.addWidget(self.last_year_button,0,0,1,1)
      
    self.time_grid.addWidget(self.numday_start_label,1,0,1,1)
    self.time_grid.addWidget(self.numday_stop_label,1,1,1,1)
    self.time_grid.addWidget(self.label_maxday_label,1,2,1,1) 
    
    
    self.time_grid.addWidget(self.label_maxday,2,2,1,1)                    
    self.time_grid.addWidget(self.numday_box,2,0,1,1) 
    self.time_grid.addWidget(self.numday_stop_box,2,1,1,1)      

   
def createOptionsGroup(self):
        self.groupBox = QtWidgets.QGroupBox(" Properties ")  
        
        self.scale_all_axes = QtWidgets.QCheckBox(
            "Scale:all columns, all time")                 
        self.yearlines_checkbox = QtWidgets.QCheckBox(
            'Draw year lines')           
        self.datescale_checkbox = QtWidgets.QCheckBox(
            'Format time axis')         
        self.fielddata_checkbox = QtWidgets.QCheckBox(
            'Add field data') 
                 
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.scale_all_axes)
        vbox.addWidget(self.yearlines_checkbox)
        vbox.addWidget(self.datescale_checkbox)
        vbox.addWidget(self.fielddata_checkbox)        
        vbox.addStretch(1)
        self.groupBox.setLayout(vbox)     
               
class PropertiesDlg(QtWidgets.QDialog): 
    def __init__(self, parent=None):
        super(PropertiesDlg, self).__init__(parent)    
        #window = Window(self)
        #print (self.Window.value)
        #self.okButton = QtWidgets.QPushButton("&OK")
        #self.cancelButton = QtWidgets.QPushButton("Cancel")
        #self.button = QtWidgets.QCheckBox('test') 
        #if self.value == True or None:
        #    self.dialog.button.setChecked()
        #layout = QtWidgets.QGridLayout()
        #layout.addWidget(self.button, 0, 0, 1, 1) 
        #layout.addWidget(self.okButton, 1, 0, 1, 1) 
        
        #layout.addWidget(self.cancelButton, 1, 1, 1, 1)         
        #layout.addWidget(self.buttonBox, 3, 0, 1, 3)
        #self.setLayout(layout) 
        #self.okButton.released.connect(self.accept)
        #self.cancelButton.released.connect(self.reject)
        
        #if self.button.isChecked():
        #    #self.button_event()
        #    print('is checked')
            
        #def button_event(self):
        #    print ('button event')
        #    self.value1 = True 
        #    return self.value1                
        
                       
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    sys.exit(app.exec_()) 
