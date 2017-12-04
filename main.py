#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 14. des. 2016

@author: E.Protsenko
'''

import os, sys
import numpy as np
from netCDF4 import Dataset 
from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib import rc
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.pyplot as plt


import readdata
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
        self.fname , _ = (QtWidgets.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))
          
        self.totitle = os.path.split(self.fname)[1]
        self.setWindowTitle("BROM Pictures (" + str(self.totitle) + ')')     
        readdata.readdata_brom(self, self.fname)    
         
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self) 
        createCmapLimitsGroup(self)
                
        # Create widgets
        self.label_choose_var = QtWidgets.QLabel('Choose variable:')                   

        self.qlistwidget = QtWidgets.QListWidget()      
        self.qlistwidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.all_year_box = QtWidgets.QComboBox()                                                                       
        self.all_year_button = QtWidgets.QPushButton()                                  
        self.fick_box = QtWidgets.QPushButton() 
        self.help_button = QtWidgets.QPushButton('Help')
                
        self.fh = Dataset(self.fname)                    
        readdata.read_num_col(self, self.fname)
        self.qlistwidget.addItems(self.sorted_names)
        
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self)        
                
        if 'i' in self.names_vars: 
            self.dist = np.array(self.fh.variables['i'])  
                    
        self.fh.close()

        if 'i' in self.names_vars:                        
            self.numcol_2d.setRange(0, int(self.testvar.shape[0] - 1))               
            self.numday_box.setRange(0, self.lentime)              
            self.numday_stop_box.setRange(0, self.lentime)             
            self.numday_stop_box.setValue(self.lentime)

        self.fick_box.setText('Fluxes SWI')
        self.all_year_button.setText('1D plot')
           
        # ## Define connection between clicking the button and 
        # ## calling the function to plot figures         
                                 
        self.all_year_button.released.connect(self.call_all_year)      
        self.fick_box.released.connect(self.call_fluxes)                                   
        self.help_button.released.connect(self.call_help)
   
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.setMinimumSize(self.canvas.size())
        
        # # The QGridLayout class lays out widgets in a grid          
        self.grid = QtWidgets.QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self, self.fname)   
                 
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
                                     
    def call_help(self):
        help_dialog.show(self) 
        
def createDistGroup(self):  
        
    self.dist_groupBox = QtWidgets.QGroupBox("Distance axis")           
    self.dist_grid = QtWidgets.QGridLayout(self.dist_groupBox)    
    self.col_label = QtWidgets.QLabel('Column: ')
    self.numcol_2d = QtWidgets.QSpinBox() 
    readdata.read_num_col(self, self.fname)
    self.label_maxcol = QtWidgets.QLabel(
        'max\ncolumn: ' + str(self.testvar.shape[0] - 1))         
    self.dist_grid.addWidget(self.col_label, 0, 0, 1, 1) 
    self.dist_grid.addWidget(self.numcol_2d, 1, 0, 1, 1) 
    self.dist_grid.addWidget(self.label_maxcol, 1, 1, 1, 1) 
    
       
def createTimeGroup(self):  
     
    self.last_year_button = QtWidgets.QPushButton('last year')    
    self.time_groupBox = QtWidgets.QGroupBox(" Time axis")        
    self.label_maxday_label = QtWidgets.QLabel('max day: ')
    self.label_maxday = QtWidgets.QLabel(str(self.lentime - 1))    
    self.numday_start_label = QtWidgets.QLabel('start: ') 
    self.numday_box = QtWidgets.QSpinBox()     
    self.numday_stop_label = QtWidgets.QLabel('stop: ') 
    self.numday_stop_box = QtWidgets.QSpinBox()    

    self.time_grid = QtWidgets.QGridLayout(self.time_groupBox)   

    # self.time_grid.addWidget(self.last_year_button,0,0,1,1)      
    self.time_grid.addWidget(self.numday_start_label, 1, 0, 1, 1)
    self.time_grid.addWidget(self.numday_stop_label, 1, 1, 1, 1)
    self.time_grid.addWidget(self.label_maxday_label, 1, 2, 1, 1) 
    
    self.time_grid.addWidget(self.label_maxday, 2, 2, 1, 1)                    
    self.time_grid.addWidget(self.numday_box, 2, 0, 1, 1) 
    self.time_grid.addWidget(self.numday_stop_box, 2, 1, 1, 1)      
  
def createOptionsGroup(self):
        self.OptionsgroupBox = QtWidgets.QGroupBox(" Properties ")  
        self.change_limits_checkbox = QtWidgets.QCheckBox('Change limits')        
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
        vbox.addWidget(self.change_limits_checkbox)        
        vbox.addWidget(self.datescale_checkbox)
        vbox.addWidget(self.fielddata_checkbox)        
        vbox.addStretch(1)
        self.OptionsgroupBox.setLayout(vbox)     

def createCmapLimitsGroup(self):
        
        self.cmap_groupBox = QtWidgets.QGroupBox("colour map limits ")  

        self.label_maxwater = QtWidgets.QLabel('cmap max water: ')       
        self.label_minwater = QtWidgets.QLabel('min water: ')         
        self.label_maxbbl = QtWidgets.QLabel('cmap max bbl: ')       
        self.label_minbbl = QtWidgets.QLabel('min bbl: ')                   
        self.label_maxsed = QtWidgets.QLabel('cmap max sediment: ')
        self.label_minsed = QtWidgets.QLabel('min sediment: ')  
        
        self.box_minwater = QtWidgets.QDoubleSpinBox()
        self.box_maxwater = QtWidgets.QDoubleSpinBox()
        self.box_minbbl = QtWidgets.QDoubleSpinBox()
        self.box_maxbbl = QtWidgets.QDoubleSpinBox()        
        self.box_minsed = QtWidgets.QDoubleSpinBox()
        self.box_maxsed = QtWidgets.QDoubleSpinBox()    
                
        self.box_minwater.setMaximum(1000000000)   
        self.box_minbbl.setMaximum(1000000000)       
        self.box_minsed.setMaximum(1000000000)      
                      
        self.box_maxwater.setMaximum(1000000000)   
        self.box_maxbbl.setMaximum(1000000000)           
        self.box_maxsed.setMaximum(1000000000)  
        
        cmap_grid = QtWidgets.QGridLayout(self.cmap_groupBox) 
        
        # cmap_grid.addWidget(self.change_limits_checkbox,0,0,1,1) 
        
        cmap_grid.addWidget(self.label_minwater, 1, 0, 1, 1)
        cmap_grid.addWidget(self.label_maxwater, 1, 1, 1, 1)
        cmap_grid.addWidget(self.box_minwater, 2, 0, 1, 1)
        cmap_grid.addWidget(self.box_maxwater, 2, 1, 1, 1)  
                 
        cmap_grid.addWidget(self.label_minbbl, 3, 0, 1, 1)        
        cmap_grid.addWidget(self.label_maxbbl, 3, 1, 1, 1)
        cmap_grid.addWidget(self.box_minbbl, 4, 0, 1, 1)
        cmap_grid.addWidget(self.box_maxbbl, 4, 1, 1, 1)     
         
        cmap_grid.addWidget(self.label_minsed, 5, 0, 1, 1)        
        cmap_grid.addWidget(self.label_maxsed, 5, 1, 1, 1)
        cmap_grid.addWidget(self.box_minsed, 6, 0, 1, 1)
        cmap_grid.addWidget(self.box_maxsed, 6, 1, 1, 1)  
                      
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    sys.exit(app.exec_()) 
