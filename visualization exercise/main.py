import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotImigrationsOverYeas():
    #create a list of highest immigration rates to Canada over 1980-2014
    df.sort_values(['Total'], ascending=False, axis=0, inplace=True)
    top10 = df.drop(df[df["Country"] == "Total"].index, axis=0, inplace=True)
    top10 = df['Country'].head(10)
    years = list(map(int, range(1980, 2014))) 
    df_selected = df[df["Country"].isin(top10)][["Country"] + years].set_index("Country")

    # Transpose the data for plotting
    df_selected = df_selected.T
    df_selected.index = df_selected.index.astype(int)  # Convert years to int
    plt.figure(figsize=(12, 6))
    plt.stackplot(df_selected.index, df_selected.T, labels=df['Country'].head(10), alpha=0.7)

    plt.xlabel("Year")
    plt.ylabel("Number of Immigrants")
    plt.title("Immigration to Canada (1980-2013)")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()


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
path = r"C:\Users\Klaudia\Documents\GitHub\-jenny4556-.github.io\visualization exercise\Canada.xlsx"

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

#plotImigrationsOverYeas()

count, bin_edges = np.histogram(df[2013])
df[2013].plot(kind='hist', figsize=(8, 5), xticks=bin_edges)
plt.show()











