
import pandas as pd
 
class field:
    def __init__(self,index,ax00,ax10,ax20):
        self.index = index 
        self.ax00 = ax00
        self.ax10 = ax10
        self.ax20 = ax20   
        
        self.mfc ='#b71c1c'  # marker facecolor
        self.mec = '#5b0e0e' # marker edgecolor    
        self.mew = 0.7       # markeredgewidth
           
        self.df_1808 = pd.read_csv('field_data\BBL_18-08-2009.txt',
                sep = '\t',
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','SO4','DON','NH4','NO3','no2','Fe2','Mn2','Ni',
                'hg_tot','mehg'])           
        self.df_1808.depth = self.df_1808.sed_depth/100 + 9    
    
        self.df_1507 = pd.read_csv('field_data\BBL_15-07-2009.txt',
                sep='\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','SO4','DON','NH4','NO3','no2','Fe2',
                'Mn2','Ni','hg_tot','mehg' ])
        
        self.df_2009 = pd.read_csv('field_data/bbl_porewater_2009.txt',
                sep = '\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','SO4','DON','NH4','Fe2','Mn2','Ni',
                'hg_tot','mehg'])
    
        self.df_2010 = pd.read_csv('field_data/bbl_porewater_2010.txt',
                sep = '\t', 
                names = ['depth', "sed_depth",'pH','H2S','Alk',
                'PO4','DON','NH4','NO3','SO4','Fe2','Mn2','Ni'])      
          
        xl = pd.ExcelFile(r'field_data/Water_column_18-08-2009.xlsx')
        self.o2_1808 = xl.parse("Sheet1", skiprows=2)     
         
        xl1 = pd.ExcelFile(r'field_data/Water_column_15-07-2009.xlsx')
        self.o2_1507 = xl1.parse("Sheet1", skiprows=3)   
        
        self.read() 
        
    def read(self):                                                
        if self.index in ('Alk','pH','H2S','PO4','DON','NH4',
                          'NO3','SO4','Fe2','Mn2','Ni'):
            self.call_plot(self.index)
                
        elif self.index in ('Hg0','Hg2','Hg2_tot_diss'):
            self.call_plot('hg_tot')
            
        elif self.index in ('MeHg','MeHg_tot_diss'):
            self.call_plot('mehg')    
                    
        elif self.index == 'O2':
            self.plot_f(self.ax00,self.o2_1808['mkM'],self.o2_1808['meters'])
            self.plot_f(self.ax10,self.o2_1808['mkM'],self.o2_1808['meters'])    
            self.plot_f(self.ax00,self.o2_1507['mkM'],self.o2_1507['meters'])
            self.plot_f(self.ax10,self.o2_1507['mkM'],self.o2_1507['meters'])                     
 
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
        