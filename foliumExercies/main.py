import folium
import numpy as np
import pandas as pd
import requests
import io
from folium import plugins

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Police_Department_Incidents_-_Previous_Year__2016_.csv'

response = requests.get(URL)
text = io.StringIO(response.text)

#So the dataframe consists of 150,500 crimes, which took place in the year 2016. In order to reduce computational cost, just work with the 
# first 100 incidents in this dataset.
df_incidents = pd.read_csv(text)
limit = 100
df_incidents = df_incidents.iloc[0:limit, :]

# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42
SanFran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(SanFran_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

SanFran_map.save('SanFran.html')