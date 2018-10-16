
import pandas as pd
 
class field:
    def __init__(self,index,ax20): #ax00,ax10,ax20):
        self.ax20 = ax20
        self.index = index
        xls = r'field_data\JOSSINGFJORD_DGT_uM.xlsx'
        self.df = pd.read_excel(xls,header = 1,
                       names = ['station','sed_depth','Mn2','Fe2','Ni_tot_diss'])   
        self.df.sed_depth = self.df.sed_depth/10
        self.mfc ='#b71c1c'  # marker facecolor
        self.mec = '#5b0e0e' # marker edgecolor    
        self.mew = 0.7       # markeredgewidth
                  
        self.read() 
        
    def read(self):                                                
        if self.index in ('Fe2','Mn2','Ni_tot_diss'):
            self.call_plot(self.index)
                             
    def call_plot(self,var): 
        
        try: 
            self.plot_f(self.ax20,self.df[var],self.df.sed_depth)
        except : 
            pass      
                                      
    def plot_f(self,axis,varf,depthf):
          
        axis.plot(varf,depthf,'ro',
            mfc = self.mfc,mec = self.mec,mew = self.mew,
            zorder = 10)          

class field_1p:
    def __init__(self,index,ax20):
        self.index = index 
        self.ax20 = ax20   
        
        self.mfc ='#b71c1c'  # marker facecolor
        self.mec = '#5b0e0e' # marker edgecolor    
        self.mew = 0.7       # markeredgewidth
           
        xls = r'field_data\JOSSINGFJORD_DGT_uM.xlsx'
        self.df = pd.read_excel(xls,header = 1,
                       names = ['station','sed_depth','Mn2','Fe2','Ni_tot_diss'])   
        self.df.sed_depth = self.df.sed_depth/10
        self.read() 
        
    def read(self):                                                
        if self.index in ('Fe2','Mn2','Ni_tot_diss'):
            self.call_plot(self.index)
                              
    def call_plot(self,var): 
        
        try: 
            self.plot_f(self.ax20,self.df[var],self.df.sed_depth)
        except : 
            pass      
                   
    def plot_f(self,axis,varf,depthf):  
        axis.plot(varf,depthf,'ro',
            mfc = self.mfc,mec = self.mec,mew = self.mew,
            zorder = 10)      

        