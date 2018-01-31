'''
Created on 29. jan. 2018

@author: ELP
'''

import pandas as pd
df_1507 = pd.read_csv('field_data\BBL_15-07-2009.txt',sep='\t', 
                names = ['depth', "sed_depth",'pH','h2s','alk',
                'po4','so4','don','nh4','no3','no2','fe',
                'mn','ni','hg_tot','mehg' ])
df_2009 = pd.read_csv('field_data/bbl_porewater_2009.txt',
                sep = '\t', names = ['depth', "sed_depth",'pH','h2s','alk',
                'po4','so4','don','nh4','fe','mn','ni',
                'hg_tot','mehg'])

df_1808 = pd.read_csv('field_data/bbl_porewater_2009.txt',
            sep = '\t',
            names = ['depth', "sed_depth",'pH','h2s','alk',
            'po4','so4','don','nh4','no3','no2','fe','mn','ni',
            'hg_tot','mehg'])    
#df_o2_1808 = pd.read_csv(r'field_data/Water_column_18-08-2009.xlsx')
xl = pd.ExcelFile(r'field_data/Water_column_18-08-2009.xlsx')
o2_1808 = xl.parse("Sheet1", skiprows=2)      
xl1 = pd.ExcelFile(r'field_data/Water_column_15-07-2009.xlsx')
o2_1507 = xl1.parse("Sheet1", skiprows=3) 
#df = pd.read_excel(r'field_data/Water_column_18-08-2009.xlsx', sheet_name=0, header=0, skiprows=None, skip_footer=0)    
print( o2_1507) #.Mkm) 

    