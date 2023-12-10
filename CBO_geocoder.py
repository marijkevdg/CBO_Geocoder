#!/usr/bin/env python
# coding: utf-8

#Import Libraries
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

#Reads SD County CBO address data into DataFrame
df = pd.read_excel('SDCounty_CBO.xlsx')

# Function to geocode addresses with retries
def geocode_with_retry(address):
    geolocator = Nominatim(user_agent="geocoder")
    retries = 3  # Number of retries
    for _ in range(retries):
        try:
            location = geolocator.geocode(address, timeout=10)  # Increase timeout if needed
            if location:
                return location.latitude, location.longitude
            elif location == None: #If no location can be found with geolocator, set location to (0,0)
                return 0, 0
            else:
                return None, None
        except (GeocoderTimedOut, GeocoderServiceError):
            pass
    return None, None

# Geocodes addresses and stores coordinates in 'Coordinates' column
df['Coordinates'] = df['Address_Abr'].apply(lambda x: geocode_with_retry(x))

# Splits coordinates into separate 'Latitude' and 'Longitude' columns
df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)

#Saves new dataframe to output excel sheet
df.to_excel('SDCounty_CBO.xlsx')
