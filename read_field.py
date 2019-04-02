
import pandas as pd
 
class field:
    def __init__(self,index,axis1,axis2): #ax00,ax10,ax20):
        self.axis1 = axis1
        self.axis2 = axis2
        self.index = index
        print (index)
        xls = r'field_data\Horten\HH_180824_chem.xls'
    
        #tonames = ['Nst','Lat'	'Lon'	'Time','Date','Bottle','Pressure','T in situ','Sal',
        #    'Sigma-Theta','Bottom D','pH TOT-lab','pH NBS-lab','O2','DIC','Alk','PO4','Ptot,
        #    'Si','NO3+NO2','NO2','NH4','pH','H2S','CH4','Mn_diss','Mn_part','Fe_diss','Fe_part',
        #    'Na g/l','SO4 g/l','pH, NBS','pCO2','CO2','HCO3-','CO3--']

        self.df = pd.read_excel(xls,skiprows = 1)
        print (self.df.head())
        #               names = ['station','sed_depth','Mn2','Fe2','Ni_tot_diss'])   
        #self.df.sed_depth = self.df.sed_depth/10


        #self.df_red = self.df.where(self.df.station.isin(['B1','B7','B15','B28','B29']) == True)         
        #self.df_blue = self.df.where(self.df.station.isin(['B11','B27','B30']) == True) 
       
        self.mfc ='#b71c1c'  # marker facecolor
        self.mec = '#5b0e0e' # marker edgecolor    
        self.mew = 0.7       # markeredgewidth
                  
        self.read() 
        
    def read(self):                                                
        if self.index in ('PO4','Si'):
            print ('in read')
            self.call_plot(self.index)
                             
    def call_plot(self,var): 
        
        try: 
            self.plot_f(self.axis1,self.df[var],self.df.Pressure,'r')  
            self.plot_f(self.axis2,self.df[var],self.df.Pressure,'r')              
        except : 
            print ('except in call plot')
            pass      
                                      
    def plot_f(self,axis,varf,depthf,col):
          
        axis.plot(varf,depthf,marker = 'o',linestyle = 'none',
            mfc = col,mec = 'k',mew = self.mew,alpha = 0.75,
            zorder = 10)          

'''class field_1p:
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
        self.df_red = self.df.where(self.df.station.isin(['B1','B7','B15','B28','B29']) == True)         
        self.df_blue = self.df.where(self.df.station.isin(['B11','B27','B30']) == True)        
          
        self.read() 
        
    def read(self):                                                
        if self.index in ('Fe2','Mn2','Ni_tot_diss'):
            self.call_plot(self.index)
                              
    def call_plot(self,var): 
        
        try: 
            self.plot_f(self.ax20,self.df_red[var],self.df_red.sed_depth,'r')
            self.plot_f(self.ax20,self.df_blue[var],self.df_blue.sed_depth,'b')                
            #self.plot_f(self.ax20,self.df[var],self.df.sed_depth)
        except : 
            pass      
                   
    def plot_f(self,axis,varf,depthf,col):  
        axis.plot(varf,depthf,marker = 'o',linestyle = 'none',
            mfc = col,mec = 'k',mew = self.mew,
            zorder = 10)      '''

        