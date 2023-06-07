# This script will clip the land classification polygon to each MB, then calculate
# (1) total land area, (2-5) land area for each classification

import arcpy
arcpy.env.overwriteOutput = True

# input variables
arcpy.env.workspace = r"C:\Users\joeyb\OneDrive\Public\Documents\ArcGIS\Projects\DAAD1\DAAD1.gdb"
bounds_fc = "basins1"
landclass_fc = "LandClip"

with arcpy.da.SearchCursor(bounds_fc, ("Name", "OBJECTID")) as cursor:
    for row in cursor:
        # Makes a landclass layer for every MB
        mb_landclass_clip = row[0].replace("MB ", "landclass_")
        where = "'Name' = " + "'" + row[0] + "'"
        mb_selection_fc = "mb_selection"
        arcpy.management.MakeFeatureLayer(bounds_fc, mb_selection_fc, where)
        arcpy.analysis.Clip(landclass_fc, mb_selection_fc, mb_landclass_clip)

        # Calculate Area for EACH Land Class Type
        print(mb_landclass_clip + " Land Classification:")
        with arcpy.da.UpdateCursor(mb_landclass_clip, ("Class_name", "Area")) as cursorU:
            for rowU in cursorU:
                print("FOR LOOP 2 INITIATED")
                arcpy.management.CalculateGeometryAttributes(mb_landclass_clip, ["Area", "AREA_GEODESIC"],
                                                             area_unit="SQUARE_KILOMETERS")
                cursor.updateRow(class_type)
                print(class_type[0] + ": " + class_type[1])
                print("")