# Spectrum Cell Serivce Towers
This project process raw data downloaded from Canada’s TAFL (Technical and Administrative Frequency List) database and presents it visually using a web map. This document will highlight the process used to create a story map of the locations of cellular antennas across the country of Canada and whom they belong to. Raw data was retrieved from Industry Canada’s website and processed with Python. Finally, the Leaflet, Esri Leaflet, and Materialize CSS API were used to create the web mapping application. 

# Raw Data
From Industry Canada’s website, a Technical and Administrative Frequency List (TAFL) text file can be downloaded containing information regarding all of the spectrum licences (http://spectrum.ic.gc.ca/tafl/taflindex.html#National). Under the National TAFL, the file containing this information is named labeled Spectrum Licences Site Information. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26052421/201490593-be63cb11-8a3e-47ba-9b0c-46afc81d5499.png"/>
</p>

# Processing Raw Data using Python
The downloaded .zip file contains a text (.txt) file and requires manual processing to convert it into a usable format. Thus, Python was used to create a comma separated value (.csv) file following the File Layout specified by Industry Canada. 

In additional to converting the raw data to .csv format, additional processing is required:

1)	The coordinates specifying the location of each antenna is given in degrees, minutes, and seconds format. These coordinate values are converted to decimal degrees format. 
2)	Each record within the data represents one antenna at a given location (specified by coordinates) and for each given location, there could be multiple antennas attached to a tower. This will generate many redundant points in the final layer and thus, only one record is kept for each specific set of coordinates. 
3)	Since only one record will represent one location, new fields were created to store the Receiving Frequency values for each antenna that is present at that site. All other fields were deleted for simplicity. To normalize the raw data, each Receiving Frequency field was rounded down and duplicate values were removed.
4)	A field NO, was created to track how many unique Receiving Frequency values were extracted from the raw data.

## parse.py ##

This Python script reads a Spectrum Licences (Site Information) text file, parses, and produces a .csv file containing the information for each site along with the converted geographic coordinates in decimal degree format.

## formatCSV.py ##

This Python script reads the output from parse.py and formats the original values (such as cell service provider names) to a more presentable format.

## createPoints.py ##

This Python script leverages Esri’s Arcpy Python library to use the coordinates found in the formatted .csv file to create a shapefile (.shp).

# Converting Comma Separated File to Shapefile
Using a Python script, the .csv file is converted to a shapefile. Open the shapefile in ArcMap to check if the coordinates of each point feature is correct and if there are any other problems. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26052421/201490602-f0123c8c-e5a6-4c02-b845-7c54869fc3fc.png"/>
</p>

# Upload Shapefile as a Service
Once the shapefile has been verified, upload it as a service. 

# Creating a Web Mapping Application Using Leaflet and Esri Leaflet
From an empty HyperText Markup Language (HTML) template, the Leaflet and Esri Leaflet Javascript API were used to create a simple web application (app) with clustering. Due to the large number of point features present in the data, clustering was deemed an effective way to represent the data. 

With reference to the reac.TOR application created by Esri Canada’s Cameron Plouffe, Michael Luubert, and Krista Amolins, pie clustering was incorporated. Pie cluster allows users to visualize how point features of a specific class are found within that cluster. 

Using the Leaflet API reference (http://leafletjs.com/reference.html), customizations such as icon symbology, queries, basemap changes, scale, and etc. could be added with ease.

<p align="center">
  <img src="https://user-images.githubusercontent.com/26052421/201490603-d5033ad0-fa19-42bd-9461-e7cf8f76b9bf.png"/>
</p>

# Styling With Materialize CSS
Using Materialize, a modern design may be applied to the web app. In this case, a header was applied, the query and basemap changer incorporated into the header, and information button, and finally a floating action button to geolocate the user’s device.

<p align="center">
  <img src="https://user-images.githubusercontent.com/26052421/201490608-0dd21c46-e552-42ac-818f-26e8e690f608.png"/>
</p>
