# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:11:01 2022

@author: caraw
"""

# For the purposes of this Toolbox, some data preparation has already been
# done in the original Python script, e.g., creating the Baltimore City
# shapefile with various land use types erased out, and subsetting Baltimore
# City from some Maryland shapefiles.

#import packages
import arcpy

##########################
## FOOD DESERT CRITERIA ##
##########################

## (1) Average Healthy Food Availability Index (HFAI) is low ##

# read in Baltimore City food stores
stores = arcpy.GetParameterAsText(0) 

# remove gas stations
stores = arcpy.SelectLayerByAttribute_management(
        stores, 
        "NEW_SELECTION", 
        '"Type" <> \'Gas Station\'')

# read in Baltimore City Council Districts
districts = arcpy.GetParameterAsText(1) 

# use spatial join to determine which district each store is in
# and read in the result. The field name we will be interested in is
# "area_name" (1-14)
arcpy.SpatialJoin_analysis(stores, 
                           districts, 
                           arcpy.GetParameterAsText(2))
stores = arcpy.GetParameterAsText(2) 

# use cursor to assign HFAI score based on district and store type
# the store type corresponding to the else statement is "Supermarket"
arcpy.AddField_management(
        stores, 
        "HFAI", 
        "FLOAT")
with arcpy.da.UpdateCursor(
        stores, 
        ["Type", 
         "area_name",
         "HFAI"]) as cursor:
    for store in cursor:
        if store[1] == "1":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 12.2
            elif store[0] == "Convenience Store":
                store[2] = 9.2
            elif store[0] == "Discount Store":
                store[2] = 9.5
            elif store[0] == "Pharmacy":
                store[2] = 11.5
            elif store[0] == "Public Market":
                store[2] = 5.0
            else:
                store[2] = 28.2
            cursor.updateRow(store)
        elif store[1] == "2":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 9.1
            elif store[0] == "Convenience Store":
                store[2] = 9.1
            elif store[0] == "Discount Store":
                store[2] = 8.8
            elif store[0] == "Pharmacy":
                store[2] = 10.8
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 27.5
            cursor.updateRow(store)
        elif store[1] == "3":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 7.5
            elif store[0] == "Convenience Store":
                store[2] = 8.8
            elif store[0] == "Discount Store":
                store[2] = 8.6
            elif store[0] == "Pharmacy":
                store[2] = 8.5
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 28.0
            cursor.updateRow(store)
        elif store[1] == "4":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 9.6
            elif store[0] == "Convenience Store":
                store[2] = 10.0
            elif store[0] == "Discount Store":
                store[2] = 10.0
            elif store[0] == "Pharmacy":
                store[2] = 10.0
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 27.5
            cursor.updateRow(store)
        elif store[1] == "5":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 9.3
            elif store[0] == "Convenience Store":
                store[2] = 11.0
            elif store[0] == "Discount Store":
                store[2] = 7.7
            elif store[0] == "Pharmacy":
                store[2] = 10.3
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 28.3
            cursor.updateRow(store)
        elif store[1] == "6":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 8.5
            elif store[0] == "Convenience Store":
                store[2] = 8.0
            elif store[0] == "Discount Store":
                store[2] = 10.8
            elif store[0] == "Pharmacy":
                store[2] = 9.0
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 26.1
            cursor.updateRow(store)
        elif store[1] == "7":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 7.8
            elif store[0] == "Convenience Store":
                store[2] = 10.5
            elif store[0] == "Discount Store":
                store[2] = 4.6
            elif store[0] == "Pharmacy":
                store[2] = 9.0
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 27.2
            cursor.updateRow(store)
        elif store[1] == "8":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 8.3
            elif store[0] == "Convenience Store":
                store[2] = -999
            elif store[0] == "Discount Store":
                store[2] = 6.8
            elif store[0] == "Pharmacy":
                store[2] = -999
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 28.0
            cursor.updateRow(store)
        elif store[1] == "9":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 8.8
            elif store[0] == "Convenience Store":
                store[2] = 7.5
            elif store[0] == "Discount Store":
                store[2] = 11.1
            elif store[0] == "Pharmacy":
                store[2] = 8.5
            elif store[0] == "Public Market":
                store[2] = 15.0
            else:
                store[2] = 27.5
            cursor.updateRow(store)
        elif store[1] == "10":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 9.4
            elif store[0] == "Convenience Store":
                store[2] = 8.8
            elif store[0] == "Discount Store":
                store[2] = 10.3
            elif store[0] == "Pharmacy":
                store[2] = 9.5
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 27.1
            cursor.updateRow(store)
        elif store[1] == "11":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 8.3
            elif store[0] == "Convenience Store":
                store[2] = 10.1
            elif store[0] == "Discount Store":
                store[2] = 8.8
            elif store[0] == "Pharmacy":
                store[2] = 9.8
            elif store[0] == "Public Market":
                store[2] = 14.7
            else:
                store[2] = 27.5
            cursor.updateRow(store)
        elif store[1] == "12":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 9.4
            elif store[0] == "Convenience Store":
                store[2] = 10.0
            elif store[0] == "Discount Store":
                store[2] = 10.5
            elif store[0] == "Pharmacy":
                store[2] = 9.8
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 27.2
            cursor.updateRow(store)
        elif store[1] == "13":
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 8.0
            elif store[0] == "Convenience Store":
                store[2] = 10.5
            elif store[0] == "Discount Store":
                store[2] = 8.8
            elif store[0] == "Pharmacy":
                store[2] = 11.0
            elif store[0] == "Public Market":
                store[2] = 20.0
            else:
                store[2] = 27.8
            cursor.updateRow(store)
        else:
            if store[0] in ["Corner Store", "Small Grocery"]:
                store[2] = 10.9
            elif store[0] == "Convenience Store":
                store[2] = 9.1
            elif store[0] == "Discount Store":
                store[2] = 9.2
            elif store[0] == "Pharmacy":
                store[2] = 9.3
            elif store[0] == "Public Market":
                store[2] = -999
            else:
                store[2] = 28.5
            cursor.updateRow(store) 

# read in Baltimore City block groups
balt_bg = arcpy.GetParameterAsText(3)

# use spatial join to calculate average HFAI by block group 
targetFeatures = balt_bg
joinFeatures = stores
outfc = arcpy.GetParameterAsText(4)
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(targetFeatures)
fieldmappings.addTable(joinFeatures)
HFAIFieldIndex = fieldmappings.findFieldMapIndex("HFAI")
fieldmap = fieldmappings.getFieldMap(HFAIFieldIndex)
field = fieldmap.outputField
field.name = "Avg_HFAI"
field.aliasName = "Avg_HFAI"
fieldmap.outputField = field
fieldmap.mergeRule = "mean"
fieldmappings.replaceFieldMap(HFAIFieldIndex, 
                              fieldmap)
arcpy.SpatialJoin_analysis(targetFeatures, 
                           joinFeatures, 
                           outfc, 
                           "#", 
                           "#", 
                           fieldmappings)
                           
# use cursor to create binary variable indicating whether Avg_HFAI is <= 9.5
# 9.5 was the cutoff used in CLF analysis
Avg_HFAI = arcpy.GetParameterAsText(4) 
arcpy.AddField_management(Avg_HFAI, 
                          "HFAI_FD", 
                          "SHORT")
with arcpy.da.UpdateCursor(Avg_HFAI, 
                           ["Avg_HFAI", 
                            "HFAI_FD"]) as cursor:
    for bg in cursor:
        if bg[0] <= 9.5:
            bg[1] = 1
        else:
            bg[1] = 0
        cursor.updateRow(bg)

# set raster environment settings
arcpy.env.cellSize = "300"

# save as raster
inFeature = Avg_HFAI
outRaster = arcpy.GetParameterAsText(5)
field = "HFAI_FD"
arcpy.FeatureToRaster_conversion(inFeature, 
                                 field, 
                                 outRaster)

inRaster = arcpy.GetParameterAsText(5)
inMaskData = arcpy.GetParameterAsText(6)
outExtractByMask = arcpy.sa.ExtractByMask(inRaster, 
                                          inMaskData)
outExtractByMask.save(arcpy.GetParameterAsText(7))

## (2) Distance to supermarker is more than 1/4 mile ##

# read in supermarkets
supermarkets = arcpy.GetParameterAsText(8)

# create 1/4 mile buffers around supermarkets and dissolve
supermarketsBuffer = arcpy.GetParameterAsText(9)
bufferDistance = ".25 Miles"
sideType = "FULL"
endType = "ROUND"
dissolveType = "ALL"
arcpy.Buffer_analysis(supermarkets,
                      supermarketsBuffer,
                      bufferDistance,
                      sideType,
                      endType,
                      dissolveType)

# erase the buffers from the Baltimore City boundary mask
eraseOutput = arcpy.GetParameterAsText(10)
arcpy.Erase_analysis(arcpy.GetParameterAsText(6),
                     supermarketsBuffer,
                     eraseOutput)

# save as raster with 1/0 value
arcpy.env.mask = arcpy.GetParameterAsText(6)

inFeature = arcpy.GetParameterAsText(10)
newfield = "Smkt_FD"
fieldtype = "SHORT"
fieldname = arcpy.ValidateFieldName(newfield)
arcpy.AddField_management(inFeature,
                          fieldname,
                          fieldtype)
arcpy.CalculateField_management(inFeature,
                                newfield,
                                1,
                                "PYTHON3")
outRaster = arcpy.GetParameterAsText(11)
field = "Smkt_FD"
arcpy.FeatureToRaster_conversion(inFeature,
                                 field,
                                 outRaster)
inRaster = arcpy.GetParameterAsText(11)
reclassField = "Value"
remap = arcpy.sa.RemapValue([
        [1, 1],
        ["NODATA", 0]])
outReclassify = arcpy.sa.Reclassify(inRaster,
                                    reclassField,
                                    remap)
outReclassify.save(arcpy.GetParameterAsText(12))

## (3) Social Vulnerability Index (SVI) is high ##

# read in Baltimore City SVI
svi = arcpy.GetParameterAsText(13)

# use cursor to create binary variable indicating whether RPL_THEMES is >= .9
arcpy.AddField_management(svi, 
                          "SVI_FD", 
                          "SHORT")
with arcpy.da.UpdateCursor(svi, 
                           ["RPL_THEMES", 
                            "SVI_FD"]) as cursor:
    for tract in cursor:
        if tract[0] >= .9:
            tract[1] = 1
        else:
            tract[1] = 0
        cursor.updateRow(tract)

# save as raster
inFeature = svi
outRaster = arcpy.GetParameterAsText(14)
field = "SVI_FD"
arcpy.FeatureToRaster_conversion(inFeature, 
                                 field, 
                                 outRaster)

# use extract by mask to mask out industrial areas, water bodies, 
# transportation, and parks
inRaster = arcpy.GetParameterAsText(14)
inMaskData = arcpy.GetParameterAsText(6)
outExtractByMask = arcpy.sa.ExtractByMask(inRaster, 
                                          inMaskData)
outExtractByMask.save(arcpy.GetParameterAsText(15))

##########################
## CREATE FOOD DESERTS  ##
##########################

# read in the three rasters we need (i.e., final 1/0 rasters)
fd_1 = arcpy.Raster(arcpy.GetParameterAsText(7))
fd_2 = arcpy.Raster(arcpy.GetParameterAsText(12))
fd_3 = arcpy.Raster(arcpy.GetParameterAsText(15))

# use raster math to multiply all three 1/0 rasters
fd = fd_1 * fd_2 * fd_3
fd.save(arcpy.GetParameterAsText(16))