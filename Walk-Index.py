#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 21:33:38 2023

@author: matiascardoso
"""


#%% PACKAGES
# Basics
import numpy as np                                                          
from math import pi                                                            
import warnings                                                              
import os    

from datetime import datetime, timedelta
from pandas import DataFrame                                                                 

# Visualization
import pandas as pd                                                          
import matplotlib.pyplot as plt                                                
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import numpy as np
import seaborn as sns; sns.set_theme(style='white')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import MaxNLocator

#Set the working directory
os.chdir('/Users/matiascardoso/Desktop/Agile-Reproducibility')

#Read the files
IndexRaw = pd.read_csv('IndexRawV6.csv')
OA = pd.read_csv('OA.csv')
OBS = pd.read_csv('newOBS.csv')
CBS = pd.read_csv('CBS+StreetScore.csv')


#%%Join dataframes
# Perform the join based on a common column
merged_df = OA.merge(IndexRaw, left_on='ID', right_on='ID')
merged_df = OBS.merge(merged_df, left_on='ID', right_on='ID')

#%%Fill NULL
Indexv1 = merged_df.fillna(0)

list(Indexv1)

Indexv1 = Indexv1.rename(columns={'id_unique': 'TrafficSafe'})
Indexv1 = Indexv1.rename(columns={'OBS': 'OBS'})

dropC = ['Obstacles']
Indexv1 = Indexv1.drop(columns=dropC)

#%% Adding intervals (for factors where we have an interval of interest and below or above that interval the situation doesn't affect the walkability) 
Indexv1['SidewalkCo'].where(Indexv1['SidewalkCo'] <= 5, 5, inplace=True) #sidewalks wider than 5 meters
Indexv1['SidewalkCo'].where(Indexv1['SidewalkCo'] >= 0.9, 0, inplace=True) #sidewalks narrower than 0.9 meters
Indexv1['CoAmenitie'].where(Indexv1['CoAmenitie'] <= 20, 20, inplace=True) #more than 20 amenities per street
Indexv1['ParkinPres'].where(Indexv1['ParkinPres'] <= 100, 100, inplace=True) #more than 100% parking pressure


#%%Remove segments of less than 1m length
Indexv2 = Indexv1[Indexv1['length'] > 1]  

#%% Normalising fields
Indexv2 = Indexv2[['ID']].copy()

#Fields that require distance-based normalisation
Indexv2['N-Furniture'] = Indexv1['Benches'] / Indexv1['length']
Indexv2['N-EyesOnStreet'] = Indexv1['AmenitiesO'] / Indexv1['length']
Indexv2['N-Obstacles'] = Indexv1['OBS'] / Indexv1['length']
Indexv2['N-Lighting'] = Indexv1['NewLights'] / Indexv1['length']

#Fields that don't require distance-based normalisation
Indexv2['N-RoadSafety'] = Indexv1['id_count'] #changed name
Indexv2['N-ProxAmenit'] = Indexv1['CoAmenitie'] #changed name
Indexv2['N-Crime'] = Indexv1['IntDens_me']
Indexv2['N-ShortBlocks'] = Indexv1['INDEX2021']
Indexv2['N-OV'] = Indexv1['OV-corr']
Indexv2['N-SidewalkWi'] = Indexv1['SidewalkCo']
Indexv2['N-MaxSpeed'] = Indexv1['MaxSpeed']
Indexv2['N-Green'] = Indexv1['Green']
Indexv2['N-ParkinPres'] = Indexv1['ParkinPres']
Indexv2['N-ParksPlaza'] = Indexv1['ParksPlaza']
Indexv2['N-Maintenance'] = Indexv1['Maintenanc']
Indexv2['W-Sidewalks'] = Indexv1['SidewalkCo']

#%% Adding intervals (for factors that are skewed by outliers)
Indexv2['N-Lighting'].where(Indexv2['N-Lighting'] <= 0.5, 0.5, inplace=True) #No more than 1 light per meter
Indexv2['N-EyesOnStreet'].where(Indexv2['N-EyesOnStreet'] <= 0.05, 0.05, inplace=True) #No more than 1 shop per 10m
Indexv2['N-Furniture'].where(Indexv2['N-Furniture'] <= 0.1, 0.1, inplace=True) #no more than one bench per meter
Indexv2['N-Obstacles'].where(Indexv2['N-Obstacles'] <= 0.1, 0.1, inplace=True) #No more than one obstacle per meter
Indexv2['N-RoadSafety'].where(Indexv2['N-RoadSafety'] <= 1, 1, inplace=True) #No more than one accident per meter
Indexv2['N-OV'].where(Indexv2['N-OV'] <= 10, 10, inplace=True) #No more than 10 public transport stops reachable



#%% Min Max Normalisation
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
Indexv3 = Indexv2
Indexv3[['N-RoadSafety','N-Furniture','N-EyesOnStreet','N-Obstacles','N-Lighting','N-ProxAmenit','N-Crime',
        'N-ShortBlocks','N-OV','N-SidewalkWi','N-MaxSpeed','N-MaxSpeed','N-Green','N-ParkinPres','N-ParksPlaza','N-Maintenance']] = scaler.fit_transform(Indexv3[['N-RoadSafety','N-Furniture','N-EyesOnStreet','N-Obstacles','N-Lighting','N-ProxAmenit','N-Crime',
                'N-ShortBlocks','N-OV','N-SidewalkWi','N-MaxSpeed','N-MaxSpeed','N-Green','N-ParkinPres','N-ParksPlaza','N-Maintenance']])


#%% Inverse columns (for factors that have a negative effect on walkability)
Indexv3['N-MaxSpeed'] = 1 - Indexv3['N-MaxSpeed'] #high car speeds
Indexv3['N-RoadSafety'] = 1 - Indexv3['N-RoadSafety'] #accidents
Indexv3['N-Crime'] = 1 - Indexv3['N-Crime'] #criminality
Indexv3['N-ParkinPres'] = 1 - Indexv3['N-ParkinPres'] #parking pressure
Indexv3['N-Obstacles'] = 1 - Indexv3['N-Obstacles'] #obstacles


#%%Check data distribution(use this to check if there are still outliers skewing the factors)
import pandas as pd
import matplotlib.pyplot as plt

#Original
IndexRaw['OV-corr'].plot(kind='hist', bins=10)  # Plotting a histogram with 10 bins
plt.xlabel('Values')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Distribution of Data')  # Title of the plot
plt.show()  # Display the plot

# With Intervals
Indexv2['N-OV'].plot(kind='hist', bins=10)  # Plotting a histogram with 10 bins
plt.xlabel('Values')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Distribution of Data')  # Title of the plot
plt.show()  # Display the plot
 
# With Intervals
Indexv3['N-OV'].plot(kind='hist', bins=10)  # Plotting a histogram with 10 bins
plt.xlabel('Values')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Distribution of Data')  # Title of the plot
plt.show()  # Display the plot

#%% Calculate the Main Index Scores (using the weights resulting from the participatory activity)
Indexv4 = Indexv3
Indexv4['I-Zscore'] = Indexv4["N-RoadSafety"]*0.094 +Indexv4["N-Obstacles"]*0.093 +Indexv4["N-SidewalkWi"]*0.086 +Indexv4["N-Lighting"]*0.074 +Indexv4["N-MaxSpeed"]*0.073  +Indexv4["N-ProxAmenit"]*0.073 +Indexv4["N-Crime"]*0.071 +Indexv4["N-OV"]*0.068 +Indexv4["N-Maintenance"]*0.065 +Indexv4["N-EyesOnStreet"]*0.059 +Indexv4["N-Furniture"]*0.056 +Indexv4["N-ParksPlaza"]*0.056 +Indexv4["N-ParkinPres"]*0.053 +Indexv4["N-Green"]*0.048  +Indexv4["N-ShortBlocks"]*0.031

#Normalising Index
Indexv4['Non-Scaled']=Indexv4['I-Zscore']
Indexv4[['I-Zscore']] = scaler.fit_transform(Indexv4[['I-Zscore']])


#%% Calculating the Sub-Index Scores (using the weights resulting from the participatory activity)
Indexv5 = Indexv4
Indexv5['Landscape'] = Indexv4['N-Furniture']*0.056+Indexv4[ 'N-Green']*0.048+Indexv4[ 'N-ParksPlaza']*0.056+Indexv4[ 'N-ParkinPres']*0.059+Indexv4['N-EyesOnStreet']*0.053
Indexv5['Traffic Safety'] = Indexv4['N-RoadSafety']*0.094+Indexv4['N-MaxSpeed']*0.073
Indexv5['Proximity'] = Indexv4['N-ProxAmenit']*0.073+Indexv4['N-ShortBlocks']*0.031+Indexv4['N-OV']*0.068
Indexv5['Crime Safe'] = Indexv4['N-EyesOnStreet']*0.059+Indexv4['N-Crime']*0.071+Indexv4['N-Lighting']*0.074
Indexv5['Infrastructure'] = Indexv4['N-Obstacles']*0.093+Indexv4[ 'N-SidewalkWi']*0.086+Indexv4['N-Maintenance']*0.065

#%% Min Max Normalisation
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
Indexv5[['Landscape','Traffic Safety','Proximity','Crime Safe','Infrastructure']] = scaler.fit_transform(Indexv5[['Landscape','Traffic Safety','Proximity','Crime Safe','Infrastructure']])


#%% Save it
Indexv5.to_csv('Index-Walkability.csv', index = False)

#After saving, perform a join-by-field value in QGIS with the shapefiles of the street segments. Join using the fields called "ID"












