# This script will export all of the dead-end roads within a polygon,
# then count the number of features to give the number of "culdesacs"/
# dead end roads within each micro-basin (mb)

import arcpy
arcpy.env.overwriteOutput = True

'''
# input variables soft
arcpy.env.workspace = arcpy.GetParameterAsText(0)
bounds_fc = arcpy.GetParameterAsText(1)
roads_fc  = arcpy.GetParameterAsText(2)
'''

# input variables hard
arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb"
bounds_fc = "basins1"
roads_fc  = "all_roads"

# identify the dead ends in fc
dangle_fc = "dangle_pts"
arcpy.management.FeatureVerticesToPoints(roads_fc, dangle_fc, "DANGLE")
total_de_count = arcpy.management.GetCount(dangle_fc)
print("Total Count of Dead Ends is " + str(total_de_count))

# dead ends in each microbasin
with arcpy.da.SearchCursor(bounds_fc, ("Name")) as cursor:
    for row in cursor:
        basin_fc = row[0].replace(" ", "_")
        where = '"Name" = ' + "'" + row[0] + "'"
        arcpy.conversion.ExportFeatures(bounds_fc, basin_fc, where)
        dangle_select = arcpy.management.SelectLayerByLocation(dangle_fc, "WITHIN", basin_fc)
        basin_de_count = arcpy.management.GetCount(dangle_select)
        print("Within " + str(basin_fc) + ", there are " + str(basin_de_count) + " dead-end roads.")
