import os, csv

records = []

filePath = os.getcwd()
with open("{}\\spectrum_lic.csv".format(filePath), "r") as csvFile:
    inReader = csv.reader(csvFile)
    for row in inReader:
        records.append(row)

csvFile.close()

# Build dictionaries
# Key Value : (Latitiude, Longitude) <- tuple
coordinates = {} # an integer represent the amount of antennas present for a given location
locations = {} # a string representing the location of the tower
frequencies = {} # list representing the receiving frequencies the tower receives
licensees = {} # a string representing the licensee (company)
co_codes = {} # a string representing the company code
target = {"Rogers Communicati" : "Rogers Wireless", \
          "ROGERS COMMUNICATI" : "Rogers Wireless", \
          "FIDO SOLUTIONS INC" : "Rogers Wireless", \
          "Data & Audio-Visua" : "Rogers Wireless", \
          "TELUS Communicatio" : "Telus Mobility", \
          "Bell Mobility Inc." : "Bell Mobility", \
          "BELL MOBILITY INC." : "Bell Mobility", \
          "Bragg Communicatio" : "EastLink", \
          "ICE WIRELESS INC." : "Ice", \
          "Lynx Mobility Inc." : "Lynx", \
          "MTS Inc." : "MTS", \
          "MTS Inc.- Attn: Do" : "MTS", \
          "NEXICOM INC." : "Nexicom", \
          "NEXICOM MOBILITY I" : "Nexicom", \
          "SASKTEL MOBILITY(C" : "SaskTel", \
          "SASKTEL(AWS/PCS)" : "SaskTel", \
          "SASKTEL(BRS)" : "SaskTel", \
          "SASKTEL(PCS)" : "SaskTel", \
          "SOGETEL MOBILITE I" : "Sogetel", \
          "TBayTel" : "TBayTel", \
          "Tbaytel - Accounts" : "TBayTel", \
          "Vid\xe9otron s.e.n.c.": "Videotron", \
          "WIND Mobile Corp." : "Wind Mobile"}

def getProvider(licensee):
    if(licensee in target):
        return target[licensee]
    return " "

# Iterate through spectrum licence csv file and build dictionaries 
for record in records[1:]: # begin on index 1 to avoid the header
    coord = (record[7], record[8])
    # Format the receiving frequencies to integer and round down
    # Retrieve other relevant attributes
    RX = (int(record[2])/100) * 100
    licensee = record[24]
    co_code = record[23]
    location = record[5]
    # Populate dictionaries
    if(coord in coordinates): 
        coordinates[coord] += 1
        if(RX not in frequencies[coord]):
            frequencies[coord].append(RX)
    else:
        coordinates[coord] = 1
        locations[coord] = location
        frequencies[coord] = [RX]
        licensees[coord] = licensee
        co_codes[coord] = co_code

# Remove unwanted frequencies
for tower in frequencies:
    keepFrequencies = []
    for frequency in frequencies[tower]:
        if(frequency < 10000):
            keepFrequencies.append(frequency)
    frequencies[tower] = keepFrequencies

header = ["LATITUDE", "LONGITUDE", "LOCATION", "CO_CODE", "LICENSEE", \
          "Provider", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "NO"]

# Create csv file to populate
with open("spectrum_lic_all.csv", "wb") as outFile:
    outWriter = csv.writer(outFile, lineterminator = "\n")
    outWriter.writerow(header)

    count = 0

    for each in coordinates:
        count += 1
        # Retrieve attributes from dictionaries
        lat = each[0]
        lon = each[1]

        location = locations[each]
        co_code = co_codes[each]
        licensee = licensees[each]
        provider = getProvider(licensee)

        rxFrequencies = frequencies[each]
        rxFrequencies.sort()

        # Build list to write to csv file
        write = [lat, lon, location, co_code, licensee, provider]

        for rx in rxFrequencies:
            write.append(rx)

        for i in range(8 - len(rxFrequencies)):
            write.append(0)

        write.append(len(rxFrequencies))
        if((count % 100) == 0):
            print count

        # Only interested in the records/towers with frequencies
        if(len(rxFrequencies) > 0) and (provider != " "):
            outWriter.writerow(write)

# close csv file
outFile.close()
print("Done")
        
