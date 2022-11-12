"Takes a CSV as input, write a SHP as output"
import arcpy
import os

csv_input = r"...\spectrum_lic_all.csv"
shp_output_dir = os.path.dirname(csv_input)
temp_layer = os.path.splitext(os.path.basename(csv_input))[0] # == "input"

# OP NOTE - you say "coordinates" and I assumed you meant WGS84 latitude/longitude. If not, this is NOT your projection
WGS84_PROJ = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];IsHighPrecision"
# OP NOTE - if the latitude/longitude fields aren't named as such you'll need to update this
arcpy.MakeXYEventLayer_management(csv_input, "LONGITUDE", "LATITUDE", temp_layer, WGS84_PROJ)
# OP note: this exports a feature to a directory as a shapefile.
# You don't specify the name directly, it's just taken from the existing `temp_layer` name
arcpy.FeatureClassToShapefile_conversion(temp_layer, shp_output_dir)
arcpy.Delete_management(temp_layer) # clean up layer, for completeness
