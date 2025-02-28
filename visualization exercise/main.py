import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plotImigrationFromACountry(country):
    #a func that takes a country name as a string and plots the distribution of imigration rates to Canada from theat country over years 1980-2013
    try:
        countryRow = df[df['Country']==country].index[0]
        plt.plot(yearsCols.iloc[0], yearsCols.loc[countryRow])
        plt.xlabel('Years')
        plt.ylabel('Number of imigrants from ' + country + 'to Canada')
        plt.show()
    except Exception as e:   
        print('ERROR: Invalid country name. Check your spelling.')

    
#data from https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Canada.xlsx
path = r"C:\Users\XC00355\Documents\Canada.xlsx"

xls = pd.ExcelFile(path)
df = pd.read_excel(xls, sheet_name= 'Canada by Citizenship', skiprows=19)

#renaming columns to row 2-
newHeaders = []
for column in range(len(df.columns)):
    newHeaders.append(df.iloc[0, column])

df.columns = newHeaders
with warnings.catch_warnings():
    warnings.filterwarnings('ignore')
    #dropping unnecessary columns providing no insight
    df.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)
    #replacing column names to be more representative
    df.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region'}, inplace=True)
    #drop 1st row as it contains duplicated values from the headers
    df.drop(labels=0, axis=0, inplace=True)

#checking for missing data - no missing data
#print(df.isnull().sum())

#add a column with cumulative number of imigrants to Canada over the period of 1980-2013
yearsCols = df.iloc[:, 4:33]
df['Total'] = yearsCols.sum(axis=1)
#plotImigrationFromACountry('aaa')

#create a list of highest immigration rates to Canada over 1980-2014
top10 = df['Total'].sort_values(ascending=False)

top10.drop(columns = ['Continent', 'Region', 'DevName'], axis=1, inplace=True)

yearsList = list(map(str, range(1980, 2013)))
top102 = top10.transpose()
top103 = df.head(10)
print(top103)




