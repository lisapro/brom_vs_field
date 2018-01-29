import csv 
import numpy as np
import pandas as pd
import csv  
 
class field:
    def __init__(self,index,ax00,ax10,ax20):
        self.index = index #str(self.qlistwidget.currentItem().text())  
        self.ax00 = ax00
        self.ax10 = ax10
        self.ax20 = ax20   
        self.mfc ='#b71c1c'  # marker facecolor
        self.mec = '#5b0e0e' # marker edgecolor    
        self.mew = 0.7       # markeredgewidth
           
        self.df_1808 = pd.read_csv('field_data\BBL_18-08-2009.txt',
                sep = '\t',
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','so4','don','nh4','no3','no2','fe','mn','ni',
                'hg_tot','mehg'])           
        self.df_1808.depth = self.df_1808.sed_depth/100 + 9    
    
        self.df_1507 = pd.read_csv('field_data\BBL_15-07-2009.txt',
                sep='\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','so4','don','nh4','no3','no2','fe',
                'mn','ni','hg_tot','mehg' ])
        
        self.df_2009 = pd.read_csv('field_data/bbl_porewater_2009.txt',
                sep = '\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','so4','don','nh4','fe','mn','ni',
                'hg_tot','mehg'])
    
        self.df_2010 = pd.read_csv('field_data/bbl_porewater_2010.txt',
                sep = '\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','don','nh4','no3','so4','fe','mn','ni'])        
        
        
        self.read() 
        
    def read(self):    
           
        #if self.index == 'Alk':
        #    self.call_plot('Alk')
                                 
        if self.index in ('Alk','pH','H2S','PO4'):
            self.call_plot(self.index)
                    
        #elif self.index == 'H2S':
        #    self.call_plot(self.index)            
            
        #elif self.index == 'PO4':
        #    self.call_plot('PO4')              
                
        elif self.index == 'DON':
            self.call_plot('don') 
                       
        elif self.index == 'NH4':
            self.call_plot('nh4') 
              
        elif self.index == 'NO3':
            self.call_plot('no3') 
            
        elif self.index == 'SO4':
            self.call_plot('so4')            
                     
        elif self.index == 'Fe2':
            self.call_plot('fe')            
        
        elif self.index == 'Mn2' :
            self.call_plot('mn')            
            
        elif self.index == 'Ni':           
            self.call_plot('ni')
                 
        elif self.index in ('Hg0','Hg2','Hg2_tot_diss'):
            self.call_plot('hg_tot')
            
        elif self.index == 'MeHg' or self.index =='MeHg_tot_diss':
            self.call_plot('mehg')            


         
    def call_plot(self,var): 
        
        try: 
            self.plot_f(self.ax00,self.df_1507[var],self.df_1507.depth)
            self.plot_f(self.ax10,self.df_1507[var],self.df_1507.depth)  
            self.plot_f(self.ax20,self.df_1507[var],self.df_1507.sed_depth)
        except : 
            pass      
               
        try:        
            self.plot_f(self.ax00,self.df_2009[var],self.df_2009.depth)
            self.plot_f(self.ax10,self.df_2009[var],self.df_2009.depth)  
            self.plot_f(self.ax20,self.df_2009[var],self.df_2009.sed_depth)   
        except :
            pass  
                    
        try:    
            self.plot_f(self.ax00,self.df_1808[var],self.df_1808.depth)
            self.plot_f(self.ax10,self.df_1808[var],self.df_1808.depth)  
            self.plot_f(self.ax20,self.df_1808[var],self.df_1808.sed_depth)
        except: 
            pass  
                      
        try:                     
            self.plot_f(self.ax00,self.df_2010[var],self.df_2010.depth)
            self.plot_f(self.ax10,self.df_2010[var],self.df_2010.depth)  
            self.plot_f(self.ax20,self.df_2010[var],self.df_2010.sed_depth)    
        except: 
            pass  
                       
    def plot_f(self,axis,varf,depthf):  

        axis.plot(varf,depthf,'ro-',
            mfc = self.mfc,mec = self.mec,mew = self.mew,
            zorder = 10)          
        