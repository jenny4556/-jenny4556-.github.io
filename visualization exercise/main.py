import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import folium
import requests
import json

def createImmigrationMap():
    #A func creating a worold map using Folium, highlighting in colour countries with the highest immigration rates to Canada
    URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'

    response = requests.get(URL)
    # Ensure the request was successful
    if response.status_code == 200:
        world_geo = response.json()  # Convert response to Python dictionary
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")


    world_map = folium.Map(location=[0, 0], zoom_start=2)
    df.drop(df[df["Country"] == "Total"].index, axis=0, inplace=True)
    df.drop(df[df["Country"] == "Unknown"].index, axis=0, inplace=True)

    df_countries = df['Country']

    #df_json = world_geo['features'][:]['properties']['name']

    df_json = []
    for i in range(len(world_geo['features'])):
        df_json.append(world_geo['features'][i]['properties']['name'])

    filtered = df_countries.isin(df_json)

    notInJason = []
    for i in range(1, len(filtered)):
        if filtered[i] == False:
            notInJason.append(df_countries.iloc[i])

    #TO-DO: replace country names that don't match between df['County'] and JSON

    folium.Choropleth(
        geo_data=world_geo,  # GeoJSON data
        name="choropleth",
        data=df,  # Example data
        columns=["Country", "Total"],  # This should match your actual data structure
        key_on="feature.properties.name",  # Ensure it matches GeoJSON structure
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Immigration to Canada"
    ).add_to(world_map)

    folium.LayerControl().add_to(world_map)

    world_map.save('immigrationMap.html')


def bubbleChartforBrazilAndArgentina():
    #a func to create bubble charts on the same canvas for both Argentina and Brazil - the purpose it to assess the impact of Argentina's great
    #depression impact (1998-2002) on the immigration rates to Canada. This is being compared to the Argentina's neighbour, Brazil, to see if the
    #plot can indicate a difference between these 2 rates
    df1 = df[years].T
    df1.columns = df.iloc[:, 0]
    df1.index = map(int, df1.index) #cast years index to int
    df1.index.name = 'Year' #label the index
    df1.reset_index(inplace=True) # reset index to bring the Year in as a column - index back to 0, 1, 2...

    #normalizing weights, using the mix-max approach
    norm_brazil = (df1['Brazil'] - df1['Brazil'].min()) / (df1['Brazil'].max() - df1['Brazil'].min())
    norm_argentina = (df1['Argentina'] - df1['Argentina'].min()) / (df1['Argentina'].max() - df1['Argentina'].min())

    # Brazil
    ax0 = df1.plot(kind='scatter',
                        x='Year',
                        y='Brazil',
                        figsize=(8, 8),
                        alpha=0.5,  # transparency
                        color='green',
                        s=norm_brazil * 2000 + 10,  # pass in weights 
                        xlim=(1975, 2015)
                        )

    # Argentina
    ax1 = df1.plot(kind='scatter',
                        x='Year',
                        y='Argentina',
                        alpha=0.5,
                        color="blue",
                        s=norm_argentina * 2000 + 10,
                        ax=ax0
                        )

    ax0.set_ylabel('Number of Immigrants')
    ax0.set_title('Immigration from Brazil and Argentina from 1980 to 2013')
    ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')
    plt.show()


def createWaffleChart(categories, values, height, width, colormap, value_sign=''):
    # compute the proportion of each category with respect to the total
    total_values = sum(values)
    category_proportions = [(float(value) / total_values) for value in values]

    # compute the total number of tiles
    total_num_tiles = width * height # total number of tiles
    
    # compute the number of tiles for each catagory
    tiles_per_category = [round(proportion * total_num_tiles) for proportion in category_proportions]
    
    # initialize the waffle chart as an empty matrix
    waffle_chart = np.zeros((height, width))

    # define indices to loop through waffle chart
    category_index = 0
    tile_index = 0

    # populate the waffle chart
    for col in range(width):
        for row in range(height):
            tile_index += 1

            # if the number of tiles populated for the current category 
            # is equal to its corresponding allocated tiles...
            if tile_index > sum(tiles_per_category[0:category_index]):
                # ...proceed to the next category
                category_index += 1       
            
            # set the class value to an integer, which increases with class
            waffle_chart[row, col] = category_index

    # use matshow to display the waffle chart
    colormap = plt.cm.coolwarm
    plt.matshow(waffle_chart, cmap=colormap)
    plt.colorbar()

    # get the axis
    ax = plt.gca()

    # set minor ticks
    ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
    ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
    
    # add dridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    plt.xticks([])
    plt.yticks([])

    # compute cumulative sum of individual categories to match color schemes between chart and legend
    values_cumsum = np.cumsum(values)
    total_values = values_cumsum[len(values_cumsum) - 1]

    # create legend
    legend_handles = []
    for i, category in enumerate(categories):
        if value_sign == '%':
            label_str = category + ' (' + str(values[i]) + value_sign + ')'
        else:
            label_str = category + ' (' + value_sign + str(values[i]) + ')'
            
        color_val = colormap(float(values_cumsum[i])/total_values)
        legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

    # add legend to chart
    plt.legend(
        handles=legend_handles,
        loc='lower center', 
        ncol=len(categories),
        bbox_to_anchor=(0., -0.2, 0.95, .1)
    )
    plt.show()


def waffleChatForScandinavian():
    #a func creating a waffle chart for Scandinavian immigration rates to Canada, showing the proportion of immigration rates from Denmark, Norawy,
    #and Sweden in the total Scandinavian immigration rates
    df.index = df.iloc[:, 0]
    df_dsn = df.loc[['Denmark', 'Norway', 'Sweden'], :]
    # compute the proportion of each category with respect to the total
    total_values = df_dsn['Total'].sum()
    category_proportions = df_dsn['Total'] / total_values

    # print out proportions
    pd.DataFrame({"Category Proportion": category_proportions})

    createWaffleChart(df_dsn.index.values, df_dsn['Total'], 10, 40, plt.cm.coolwarm)


def plotPieChartForContinents():
    #a func producing a pie chart representing immigration rates to Canada by continents
    df_continents = df.groupby('Continent', axis=0).sum()
    df_continents.drop('World', inplace=True)
    colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
    explode_list = [0.1, 0, 0, 0, 0.1, 0.1] # ratio for each continent with which to offset each wedge.

    df_continents['Total'].plot(kind='pie', autopct='%1.1f%%', startangle=90, shadow=True, labels=None, pctdistance=1.12,    
    colors=colors_list, explode=explode_list)

    plt.title('Immigration to Canada by Continent [1980 - 2013]', y=1.12) 
    plt.axis('equal') # Sets the pie chart to look like a circle.
    plt.legend(labels=df_continents.index, loc='upper left') 
    plt.show()


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

#df_developed = findDevelopingOrDeveloped(years, 'Developed regions')
#df_developing = findDevelopingOrDeveloped(years, 'Developing regions')
#plotDevelopingVsDeveloped(df_developing, df_developed)
#plotPieChartForContinents()
#waffleChatForScandinavian()
#bubbleChartforBrazilAndArgentina()
createImmigrationMap()
