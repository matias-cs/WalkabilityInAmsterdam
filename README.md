# Walkability In Amsterdam
Files to reproduce the results of the paper: Developing a city-specific walkability index through a participatory approach.

## Steps
- Run the Python code in the file Walk-Index.py
- Join the ID field of the resulting CSV file with the ID field of the OSM Walkable Streets geopackage

## Files
- Walk-Index.py: Python code to merge the CSV files, normalise, scale and calculate the scores and sub-scores.
- OpenAmenities.csv: CSV file containing the number of amenities with open fronts that face the street.
- Obstacles.csv: CSV file containing the number of obstacles on every street, found by intersecting the sidewalk area with the location of elements such as lighting poles and masts.
- StreetInfo.csv: CSV file containing one row per street segment. Each column displays information about the street segment that has been added in QGIS using buffer, zonal statistics, catchment areas or location-based joins.
- OSM Walkable Streets: OSM walkable street network divided into segments of 50m or less and without the segments that have a length of less than 1m.

## Description of the process to create the StreetInfo file:
The StreetInfo file contains the results of the addition of different datasets to the street network using one of the following 4 methods:
- Method A: Buffer - Creates a 15m buffer around the street centerline and counts the number of objects of interest that fall into the buffer.
- Method B: Count elements in catchment areas - Using the walkable network layer a 350m catchment area is calculated around the points of interest. The number of catchment areas that overlap with the street centroid is counted.
- Method C: Zonal Statistics - The pixels that overlap with the 15m buffer of the walkable network layer are summarized. The values overlapping every buffer are averaged to obtain the score.
- Method D: Join by location - Attributes for every street segment are taken from the areas with the biggest overlap with the target dataset.

### Datasets:
#### Pedestrian Network
The pedestrian network of the municipality of Amsterdam is downloaded from OpenStreetMap using the OSMnx plugin (Boeing, 2017) in Python. Since there are street segments that vary greatly in length, the lines are segmented every 50 meters and the parts measuring less than 1 meter are disregarded. The pedestrian network is therefore analysed in segments of 50 meters or less.
#### Traffic safety
Traffic safety is measured through the collection of road accidents involving pedestrians in 2019, 2020 and 2021. The count of accident points is associated with every street segment making it possible to identify areas where more accidents occur. The information on accidents is collected from the Rijkswaterstaat website. GIS method A is used to add this information to the walkable network layer.
#### Obstacles
Obstacles data was obtained from several sources such as the BGT and OpenStreetMap. The location of trees, mailboxes, light posts, bollards, urban furniture, electricity closets, trash cans, bus stops, etc is collected from the BGT. Meanwhile, the location of terraces is obtained from the Open Data portal of the municipality of Amsterdam and the location of public furniture from OpenStreetMap. The points are combined into a single layer and filtered to obtain only the ones that fall inside the geometry of the sidewalks. GIS method A is used to add this information to the walkable network layer. Finally, the number of obstacles in the sidewalk is normalised by dividing it by the street segment length and added to the network shape file.
#### Wide sidewalks
Information on sidewalk width was calculated from the shape files containing the geometry of all pedestrian paths and areas in the city in 2021. A series of QGIS tools are combined into a model that first skeletonizes the sidewalk geometries to obtain the centerlines and then measures the distance from the centreline to the edges of the sidewalk every meter. The different width measures are averaged in every street and the information is added to the corresponding segment of the walkable network using GIS method A. This method is inspired by the sidewalk width tool developed by Harvey (2021) for the city of New York.
#### Street lighting
Street light locations are obtained from the Open Data portal of the municipality of Amsterdam. To begin, lights that were less than 1 meter from each other were grouped into a single point. Then, a 10-meter buffer representing the average area covered by a street light was drawn. Finally, the number of buffers that every street segment touches is counted and the value is normalised by dividing it by the segment length. GIS method A is used to add this information to the walkable network layer.
#### Low speed
The maximum speed of the roads of Amsterdam is collected from the Open Data portal of the municipality. The speed information is then added to the walkable network shape file through a location-based join as described in the GIS method D. 
Proximity to amenities
The location of popular amenities such as supermarkets, shops, schools, general practitioners, markets, churches, etc. is downloaded from the OpenStreetMap database. According to the KIM Institute for Transport Analysis (2019), the acceptable walking distance to shops is between 300 and 1000 meters. Therefore, a catchment area of 350 meters around every amenity is calculated using the pedestrian network. Finally, the number of amenities accessible from the centroid of every street segment is counted and the information is added to the walkable network layer as described in the GIS method B.
#### Crime Safety
Crime safety indicators for 2021 are obtained from a study made by the municipality of Amsterdam and reflect the perceived safety in every neighbourhood. The scores ranging from 0 to 10 were added to the walkable network layer using a location-based join in QGIS as described in the GIS method D.
Proximity to public transport
Public transport stop locations are downloaded from the open GTFS service of the Netherlands (OV API, 2023). According to the KIM Institute for Transport Analysis (2019), the acceptable walking distance to public transport stops is 350 meters. Therefore, a catchment area of 350 meters around every point is calculated using the pedestrian network. Finally, the number of stops accessible from the centroid of every street segment is counted and the information is added to the walkable network layer as described in the GIS method B.
#### Well-maintained sidewalks
Sidewalk maintenance data is partially available through the municipality Open Data portal. The data for 2021 stems from the study “Wonen in Amsterdam” commissioned by the municipality of Amsterdam (Gemeente Amsterdam, 2021). The data reflects the average score that residents give in response to the question: How do you assess the state of maintenance of the streets and sidewalks in your neighbourhood? (1 = more than unsatisfactory, 10 = more than satisfactory). Answers are available only for neighbourhoods with at least 20 respondents reported. Because of the study design, 353 out of 514 neighbourhoods report a score. For the neighbourhoods that miss a score, the average score of 6,7 is assigned. Finally, the scores ranging from 0 to 10 were added to the walkable network layer using a location-based join in QGIS (GIS method D).
#### Many shops and restaurants open on the street
This measure is different to the proximity to amenities because it only counts land uses that are on the street and usually have an inside-outside visual connection. Therefore, schools, churches, general practitioners, etc are not included in this metric. The rest of the amenity points facing the street (e.g. shops and restaurants) are counted using GIS method A, and the resulting value is normalised by dividing it by the length of the street segment. Then, the information is added to the walkable network layer. 
#### Urban furniture
Urban furniture location is obtained from OpenStreetMap. The number of benches in every street segment is counted using GIS method A and the resulting value is normalised by dividing it by the length segment. Then, the information is added to the walkable network layer.
#### Presence of parks and plazas
Information on parks and plazas is available in the Open Data portal from the municipality of Amsterdam. The information on the presence of parks and plazas next to a street was added to the walkable network layer using a location-based join (GIS method D). Only segments at 15 or less meters from the park or plaza edges are marked as close to parks and plazas.
#### No parked vehicles on the street
The municipality of Amsterdam offers a dataset containing the “Parking Pressure” of every street in the city. This term refers to what percentage of the parking capacity is occupied during the performance of the parking study. When there are 100 parking spaces within an area and 70 parking of them are occupied, the parking pressure is 70% at that time (4-traffic.nl, 2021). The parking pressure information is added to the walkable network layer using a location-based join (GIS method D). 
#### Trees and bushes
Data on the presence of greenery is obtained from the “Groenkaart van Nederland” available on the RIVM (National Institute for Public Health and the Environment) website. The map shows the percentage of green contained in every square of a 10x10-meter grid. This information was added to the walkable network layer using zonal statistics that calculated the average green percentage of every street segment and a buffer area of 15 meters around it as described in GIS method C.
#### Short blocks, frequent intersections
This measure refers to having good connectivity and is usually measured by the intersection or street density of the neighbourhood (Hajrasouliha & Yin, 2015). Since a distance of 350 meters was already used as an “acceptable walking distance” for public transport stops and amenities ((KiM Netherlands Institute for Transport Policy Analysis, 2019 ), a line density analysis was performed in QGIS using a 350-meter radius. The line density analysis shows how many street segments exist in a certain area and it is considered a proxy measure for connectivity and ease of navigation (Hajrasouliha & Yin, 2015). The line density analysis output is a raster grid of 10x10 meters that contains the number of lines counted in a 350-meter radius around that cell. This information was added to the walkable network layer using zonal statistics (GIS method C) that calculated the average line density of every street segment and a buffer area of 15 meters around it.
