import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotDevelopingVsDeveloped(df_developing, df_developed):
    #a func plotting the results found in the func indDevelopingOrDevelop
    _, ax = plt.subplots(figsize = (8,8))
    df_developing.plot.bar()
    df_developed.plot.bar(color='red')
    ax.grid(True)
    labels = ['Developing countries', 'Developed countries']
    ax.legend(labels=labels)
    plt.xlabel('Years')
    plt.ylabel('Immigration rates')
    plt.title('Imigration rates to Canada from developed vs developing countries')
    plt.show()


def findDevelopingOrDeveloped(years, categoryName):
    #a func finding a cumulative immigration rates to Canada for either Developing or Developed countries, returning a dataframe with said cumulative
    #results (against the period of interests)
    #takes in as args the list of the period of columns specifying the period of interest and a string determining whether to look for Developing
    #or Developed countries
    df_dev = df[df["DevName"] == categoryName]
    df_dev.drop(columns={'Continent', 'Region', 'DevName', 'Total'}, axis=1, inplace=True)
    df_dev.index = df_dev.iloc[:, 0]
    df_dev.rename(columns={'Country': '0'}, inplace=True)

    df_dev = df_dev.T
    df_dev['Total-dev'] = df_dev.sum(axis=1)
    df_dev.index = df_dev.index.astype(int)
    df_dev = df_dev.loc[years, 'Total-dev']

    return df_dev


def plotCumulativeImmigrationRates(years):
    #a func creating a bar chart showing cumulative immigration rates to Canada over years, taking in a list of columns specifying the period of
    #interest
    df_selected = df.drop(columns={'Continent', 'Region', 'DevName'}, axis=1)
    df_selected.index = df_selected.iloc[:, 0]
    df_selected.rename(columns= {'Country': '0', 'Total': '1'}, inplace = True)
    df_selected = df_selected.T
    df_selected.index = df_selected.index.astype(int)
    df_total = df_selected.loc[years, 'Total']

    df_total.plot(kind='bar')
    plt.xlabel('Years')
    plt.ylabel('Cumulative immigration rates to Canada')
    plt.show()


def plotImigrationsOverYeas(years):
    #a func creating an area plot of 10 countries with highest immigration rates to Canada over 1980-2014, taking in a list of columns specyfing 
    #the period of interest
    df.sort_values(['Total'], ascending=False, axis=0, inplace=True)
    top10 = df.drop(df[df["Country"] == "Total"].index, axis=0, inplace=True)
    top10 = df['Country'].head(10)
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

years = list(map(int, range(1980, 2014))) 

#plotImigrationFromACountry('aaa')
#plotImigrationsOverYeas(years)
#plotCumulativeImmigrationRates(years)

#TO-DO: create a bar chart for the last 5 years to show the cumulative immigration rates for developed and underdeveloped countries
df_developed = findDevelopingOrDeveloped(years, 'Developed regions')
df_developing = findDevelopingOrDeveloped(years, 'Developing regions')
plotDevelopingVsDeveloped(df_developing, df_developed)


#TO-DO: create the bar chart as per labs











