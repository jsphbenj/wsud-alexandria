# This script will clip the land classification polygon to each MB, then calculate
# (1) total land area, (2-5) land area for each classification

import arcpy
arcpy.env.overwriteOutput = True

# input variables
arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb"
land_class_gdb = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\MBLandClass.gdb"
bounds_fc = "basins1"
landclass_fc = "RoadsClip"
'''
with arcpy.da.SearchCursor(bounds_fc, ("Name")) as cursor:
    for row in cursor:
        # Makes a landclass layer for every MB
        mb_landclass_clip = land_class_gdb + "\\" + row[0].replace("MB ", "urbanclip_")
        where = "Name = '{}'".format(row[0])
        
        # Create a feature layer from the bounds_fc
        arcpy.management.MakeFeatureLayer(bounds_fc, "bounds_layer")

        # Apply the selection to the feature layer
        arcpy.management.SelectLayerByAttribute("bounds_layer", "NEW_SELECTION", where)

        # Create a new feature layer with the selected features
        arcpy.management.CopyFeatures("bounds_layer", "mb_selection")

        # Create feature layer objects for clipping
        landclass_layer = arcpy.management.MakeFeatureLayer(landclass_fc, "landclass_layer")

        # Perform the clip operation
        arcpy.analysis.Clip(landclass_layer, "mb_selection", mb_landclass_clip)
        print("CLIPPED: " + mb_landclass_clip)
'''
# Calculate Area for EACH Land Class Type

arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\MBLandClass.gdb"
mb_fc = arcpy.ListFeatureClasses()
for fc in mb_fc:
    arcpy.CalculateGeometryAttributes_management(fc, [["Area", "AREA_GEODESIC"]], area_unit="SQUARE_KILOMETERS")
    with arcpy.da.UpdateCursor(fc, ("Class_name", "Area")) as cursorU:
        for rowU in cursorU:
            if rowU[0] == "Urban":
                rounded_area = round(rowU[1], 2)
                print(fc + ", " + str(rounded_area))
