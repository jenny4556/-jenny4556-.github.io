import os
import pandas as pd
import numpy as np

#data from https://www.un.org/development/desa/pd/data/international-migration-flows
path = r"C:\Users\XC00355\Documents\undesa_pd_2015_migration_flow_totals.xlsx"

df = pd.read_excel(path, skiprows=15)    

#renaming columns to row 17
newHeaders = []
for column in range(len(df.columns)):
    newHeaders.append(df.iloc[0, column])

df.columns = newHeaders

#checking for missing data - no missing data
#print(df.isnull().sum())

#look for a row for which following columns have following values (col, val): CntName = Poland, Criteria = Residence, Type = Immigrants
PonadInd = 0
for i in df.index:
    if df.loc[i, 'CntName'] == 'Poland':
        if df.loc[i, 'Criteria'] == 'Residence':
            if df.loc[i, 'Type'] == 'Immigrants':
                PolandInd = i

yearsCol = df[0, 1:4]  
print(yearsCol)
        