# Created by: Joseph Benjamin
# Date: June 2023

# Objective:
# This script will calculate the (1) permeable area and (2) total area
# in both (a) each micro-basin and (b) the area captured by the
# boundary walls in each micro-basin.
# todo add + print messages throughout

import arcpy
import fnmatch
arcpy.env.overwriteOutput = True

# Working in the MBLandClass GDB
arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\WallLandClass.gdb"
mb_fc = arcpy.ListFeatureClasses()
basins = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\MBLandClass.gdb\basins_output"
walls = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb\wall_polygon_mrg"
land_class = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb\PolyLand"
total_area_dict = {"mb_number" : ("perm_area", "total_area")}
wall_area_dict = {"mb_number" : ("perm_area", "total_area")}

# part b

for fc in mb_fc:
    mb_number = fc.replace("wall_landclass_clip_", "MB ")
    '''
    Because Geometry Attributes have already been calculated with a prev script, the following can be excluded to 
    reduce runtime
    arcpy.CalculateGeometryAttributes_management(fc, [["Area", "AREA_GEODESIC"]], area_unit="SQUARE_KILOMETERS")
    '''
    with arcpy.da.SearchCursor(fc, ("Class_name", "Area")) as cursor:
        perm_area = 0 # 1a Calculate Permeable Area in Each Micro Basin
        total_area = 0 # 2a Calculate Total Area in Each MB
        for row in cursor:
            total_area += row[1]
            if row[0] != "Urban":
                perm_area += row[1]
    wall_area_dict[mb_number] = (perm_area, total_area)

# Update the Basins_Output layer with the calculations
for fc in arcpy.env.workspace:
    with arcpy.da.UpdateCursor(basins, ("Name", "WallsPermArea", "WallsTotalArea")) as cursorB:
        for rowB in cursorB:
            mb_name = rowB[0]
            perm_area_update = wall_area_dict[mb_name][0]
            rowB[1] = perm_area_update

            total_area_update = wall_area_dict[mb_name][1]
            rowB[2] = total_area_update
            cursorB.updateRow(rowB)

# part b

# 1b Calculate Permeable Area within Each MB's Walls

# 2b Calculate Total Area within Each MB's Walls