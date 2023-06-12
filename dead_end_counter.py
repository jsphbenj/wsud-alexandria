# Created by: Joseph Benjamin
# Date: June 2023

# Objective: This script will export all dead-end roads within a polygon,
# then count the number of features to give the number of
# dead end roads within each micro-basin (mb)

import arcpy
arcpy.env.overwriteOutput = True

# Input Variables
arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb"
bounds_fc = "basins1"
roads_fc  = "roads_and_bound"

# Identify the dead ends in the roads, creating a new 'dangle' feature class.
dangle_fc = "dangle_pts"
arcpy.management.FeatureVerticesToPoints(roads_fc, dangle_fc, "DANGLE")
total_de_count = arcpy.management.GetCount(dangle_fc)
print("Total, " + str(total_de_count))

# For each micro-basin, find and print the number of dead ends.
with arcpy.da.SearchCursor(bounds_fc, ("Name")) as cursor:
    for row in cursor:
        basin_fc = row[0].replace(" ", "_")
        where = '"Name" = ' + "'" + row[0] + "'"
        arcpy.conversion.ExportFeatures(bounds_fc, basin_fc, where)
        dangle_select = arcpy.management.SelectLayerByLocation(dangle_fc, "WITHIN", basin_fc)
        basin_de_count = arcpy.management.GetCount(dangle_select)
        print(str(basin_fc) + ", " + str(basin_de_count))