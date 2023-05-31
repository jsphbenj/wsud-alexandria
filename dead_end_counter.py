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
arcpy.env.workspace = "C:\\Users\\joeyb\\OneDrive\\Public\\Documents\\ArcGIS\\Projects\\DAAD1\\DAAD1.gdb\\"
bounds_fc = "basins"
roads_fc  = "all_roads"

# identify the dead ends in fc
arcpy.management.CreateFeatureclass("C:\\Users\\joeyb\\OneDrive\\Public\\Documents\\ArcGIS\\Projects\\DAAD1\\DAAD1.gdb\\", "dead_ends")
arcpy.management.FeatureVerticesToPoints(roads_fc, "dangle_pts", "DANGLE")