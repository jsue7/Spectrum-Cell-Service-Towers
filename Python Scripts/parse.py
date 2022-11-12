"""
parse.py
Author: Jack Su
Created/Modified: June 16, 2015
Summary: This Python script reads a Spectrum Licences (Site Information) text file, parses,
         and produces a .csv file containing the information for each site along with the
         converted geographic coordinates in decimal degree format. 

A Spectrum Licences (Site Information) text file may be found on Industry Canada's website.
Link: http://spectrum.ic.gc.ca/tafl/taflindex.html#Spectrum

TAFL Data File Layout may be found here: http://spectrum.ic.gc.ca/tafl/tafl/taflds.txt
TAFL Data Field Description may be found here: http://spectrum.ic.gc.ca/tafl/tafl/tafl.txt
"""
import os, csv
from types import FloatType, StringType

def convertCoordinates(lat, lon):
    """
    Precondition: Accepts two floating point representation of the latitude and
                  longitude values in degrees, minutes, seconds format.
    Postcondition: Produces two floating point representation of the latitude and
                   longitude values in decimal degrees format.
    """
    # Raise TypeError if Latitude and/or Longitude are not Floating Point values
    if type(lat) != FloatType and type(lon) != FloatType:
        raise TypeError, "convertCoordinates expects floating point values for Latitude and Longitude," \
                         + " got {} for Latitude and {} for Longitude".format(str(lat), str(lon))
    if type(lat) != FloatType:
        raise TypeError, "convertCoordinates expects a floating point value for Latitude," \
                         + " got {} for Latitude".format(str(lat))
    if type(lon) != FloatType:
        raise TypeError, "convertCoordinates expects a floating point value for Longitude," \
                         + " got {} for Longitude".format(str(lon))
	
    # Extract degree, minute, and secods for latitude and calculate the decimal
    latDD = int(lat / 10000)
    latMM = int((lat % 10000) / 100)
    latSS = lat % 100
    latDecimal = (((latMM * 60) + latSS) / (60 * 60))

    # Extract degree, minute, and secods for longitude and calculate the decimal
    lonDD = int(lon / 10000)
    lonMM = int((lon % 10000) / 100)
    lonSS = lon % 100
    lonDecimal = (((lonMM * 60) + lonSS) / (60 * 60))

    latitude = latDD + latDecimal
    longitude = (lonDD + lonDecimal) * - 1 # Since North America is left of the Prime Meridian (Greenwich), it is a negative value

    return latitude, longitude

def readRecord(aRecord):
    """
    Precondition: Accepts a string representing one record in a TAFL data
                  file and parses the record.
    Postcondition: Parses through the string record and returns the record
                   in a list data type ready to write. Changes the
                   latitude and longitude values from degrees, minutes,
                   seconds to decimal degrees.
                   
                   readRecord returns the string "0" if it satisfies the
                   following conditions:

                   1) Mobile to mobile data only
                   2) Empty 'Transmitting Frequency' field
                   3) Empy 'Receiving Frequency' field
                   4) Empty 'Latitude' field
                   5) Empty 'Longitude' field

                   OR

                   1) Incorrectly formatted record causing error in data type conversion.
    """
    # Raise TypeError if aRecord is not a string data type
    if type(aRecord) != StringType:
        raise TypeError, "readRecord expects a string value for aRecord," \
                         + " got {} for aRecord".format(str(aRecord))
    
    # Check if this record is not mobile to mobile only, and does not have empty
    # fields for the attributes: Transmitting and Receiving Frequency, Latitude,
    # and Longitude
    if(aRecord[100:106] != "RADIUS") and (aRecord[14:26].strip() != "") and \
      (aRecord[0:12].strip() != "") and (aRecord[81:87].strip() != "") and \
      (aRecord[88:95].strip() != ""):
        # Retrieve each attribute
        rxFlag = aRecord[12]
        fStatus = aRecord[28]
        rIdentifier = aRecord[30:41]
        stationLocation = aRecord[42:77].strip()
        cCode = aRecord[78:80]

        # Capture converting errors (string -> integer/float)
        try:
            tx = int(aRecord[0:12]) / 1000000
            rx = int(aRecord[14:26]) / 1000000
            lat = float(aRecord[81:87])
            lon = float(aRecord[88:95])
        except ValueError as e:
            print("{} for record: {}".format(e, aRecord))
            return "0"

        # Convert latitude and longitude to decimal degrees
        try: # Unlikely to trigger as lat and lon values are converted and checked prior to this call
            lat, lon = convertCoordinates(lat, lon)
        except TypeError as e:
            print("{} for record: {}".format(e, aRecord))
			return "0"

        eRPower = aRecord[96:101].strip()
        aGain = aRecord[102:107].strip()
        aAzimuth = aRecord[108:114].strip() 
        aSElevation = aRecord[115:120].strip()
        aHeight = aRecord[121:125].strip()
        aFarm = aRecord[126:130].strip()
        iC = aRecord[131].strip()
        iZF = aRecord[133].strip()
        linkedStation = aRecord[135:141].strip()
        mLinksFlag = aRecord[141].strip()
        sPathEditStatus = aRecord[143].strip()
        aPolarization = aRecord[145].strip()
        dONumber = aRecord[147:149].strip()
        licenceNumber = aRecord[149:156].strip()
        licenceStatus = aRecord[158].strip()
        cINumber = aRecord[161:170].strip()
        licenseeName = aRecord[171:189].strip()
        classOfStation = aRecord[190:196].strip()
        blanks = aRecord[197:202].strip()
        sCallSign = aRecord[203:209].strip()
        numberOrSignature = aRecord[210:215].strip()
        bandwidthType = aRecord[215:224].strip()
        nBandwidth = aRecord[225:229].strip()
        classEmission = aRecord[229:234].strip()
        dFAssigned = aRecord[235:243].strip()
        tTLoss = aRecord[245:250].strip()
        tPower = aRecord[251:256].strip()
        pUnits = aRecord[256:259].strip()
        aPCode = aRecord[260:264].strip()
        aAElevation = aRecord[265:269].strip()
        intCoord = aRecord[270:277].strip()
        filler = aRecord[278].strip()

        # Return record in a list data type 
        return [tx, rxFlag, rx, fStatus, rIdentifier, stationLocation, cCode, lat, lon, \
                eRPower, aGain, aAzimuth, aSElevation, aHeight, aFarm, iC, iZF, linkedStation, \
                sPathEditStatus, aPolarization, dONumber, licenceNumber, licenceStatus, \
                cINumber, licenseeName, classOfStation, sCallSign, numberOrSignature, \
                bandwidthType, dFAssigned, tTLoss, tPower, pUnits, aAElevation, intCoord, filler]
    else:
        return "0"


# Define the file path
filePath = os.getcwd()
dFile = open("{}\\spectrum_lic.txt".format(filePath), "r")

# Read from the TAFL text file and close it
L = dFile.readlines()
dFile.close()
records = L[3:] # create new list without the headers

# Create csv file to populate
with open("spectrum_lic.csv", "wb") as outFile:
    outWriter = csv.writer(outFile, lineterminator = "\n")
    outWriter.writerow(['TX', 'RX only Flag', 'RX', 'F', 'RECID', 'LOCATION', \
                        'IC', 'LATITUDE', 'LONGITUDE', 'ERP', 'GANT', 'AZIM', 'SITE', \
                        'HANT', 'PARC', 'C', 'Z', 'LINKID', 'E', 'P', 'D.O.', \
                        'LICENCE NO', 'LICENCE STATUS', 'CO. CODE', 'LICENSEE', 'CLASSNA', 'IDENT', \
                        'NOMOB', 'BW1', 'DATE', 'TL', 'TXP', 'PANT', \
                        'ELEV', 'ICN', 'FILLER'])

    # Iterate through each record and write to the csv file
    for aRecord in records:
        record = readRecord(aRecord)
        if(record != "0"):
            outWriter.writerow(record)

# close csv file
outFile.close()
