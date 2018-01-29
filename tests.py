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
       
print(df_1808.tt) 
    