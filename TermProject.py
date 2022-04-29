# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 21:22:49 2022

@author: caraw
"""

# import packages
import arcpy
import os

# set environment
arcpy.env.workspace = "C:/Users/caraw/Documents/GEOG664/TermProject"
arcpy.env.overwriteOutput = True

# use ListFeatureClasses, Describe, and SpatialReference to project all 
# shapefiles in workspace into MD StatePlane
outWorkspace = "/shapefiles_mdsp"
for fc in arcpy.ListFeatureClasses():
    dsc = arcpy.Describe(fc)
    if dsc.spatialReference.Name == "Unknown":
        print(
                "skipped this fc due to undefined coordinate system: " 
                + fc)
    else:
        outfc = os.path.join(outWorkspace, 
                             fc)
        outCS = arcpy.SpatialReference(
                "NAD 1983 StatePlane Maryland FIPS 1900 (US Feet)")
        arcpy.Project_management(
                fc, 
                outfc, 
                outCS)
        
# read in MD counties. Source: MD Food System Map
counties = "/shapefiles_mdsp/Maryland_Counties.shp"

# subset Baltimore City, save as new shapefile, and read in
balt_bdy = arcpy.SelectLayerByAttribute_management(
        counties, 
        "NEW_SELECTION", 
        '"NAME" = \'Baltimore City\'')
arcpy.CopyFeatures_management(
        balt_bdy, 
        "/shapefiles_mdsp/balt_bdy")
balt_bdy = "/shapefiles_mdsp/balt_bdy.shp"

# read in Baltimore City land cover. Source: Maryland Department of Planning
land = "/shapefiles_mdsp/Baci_2010LULC.shp"

# subset Industry type, save as new shapefile, and read in
industry = arcpy.SelectLayerByAttribute_management(
        land, 
        "NEW_SELECTION", 
        '"LU_CODE" = 15')
arcpy.CopyFeatures_management(
        industry, 
        "/shapefiles_mdsp/industry")
industry = "/shapefiles_mdsp/industry.shp"

# subset Water type, save as new shapefile, and read in
water = arcpy.SelectLayerByAttribute_management(
        land, 
        "NEW_SELECTION", 
        '"LU_CODE" = 50')
arcpy.CopyFeatures_management(
        water, 
        "/shapefiles_mdsp/water")
water = "/shapefiles_mdsp/water.shp"

# subset Transportation type, save as new shapefile, and read in
trans = arcpy.SelectLayerByAttribute_management(
        land, 
        "NEW_SELECTION", 
        '"LU_CODE" = 80')
arcpy.CopyFeatures_management(
        trans, 
        "/shapefiles_mdsp/trans")
trans = "/shapefiles_mdsp/trans.shp"

# read in Baltimore City parks. Source: Open Baltimore
parks = "/shapefiles_mdsp/parks_parks.shp"

# use erase to create a polygon mask that will be used to exclude industrial 
# areas, water bodies, transportation, and parks from food deserts
eraseOutput = "/shapefiles_mdsp/industry_erase"
arcpy.Erase_analysis(balt_bdy, 
                     industry, 
                     eraseOutput)
eraseOutput = "/shapefiles_mdsp/industry_water_erase"
arcpy.Erase_analysis("/shapefiles_mdsp/industry_erase", 
                     water, 
                     eraseOutput)
eraseOutput = "/shapefiles_mdsp/industry_water_trans_erase"
arcpy.Erase_analysis("/shapefiles_mdsp/industry_water_erase", 
                     trans, 
                     eraseOutput)
eraseOutput = "/shapefiles_mdsp/balt_mask"
arcpy.Erase_analysis("/shapefiles_mdsp/industry_water_trans_erase", 
                     parks, 
                     eraseOutput)


##########################
## FOOD DESERT CRITERIA ##
##########################

## (1) Average Healthy Food Availability Index (HFAI) is low ##

# CLF actually surveyed and scored each store, but these scores are not
# publicly available. There are two possibilities for getting an imputed
# score. In CLF's 2018 report, they provide an average score and score ranges
# by score type. But it's clear that some store types have large ranges that
# probably depend, in part, on the area of the city in which stores are 
# located. A better option is to use CLF's Food Environment Briefs, which 
# provide the average score by store type for each of the 14 council
# districts. These averages provide more geographic variation in scores. 

# read in Baltimore City food stores. Source: MD Food System Map
stores = "/shapefiles_mdsp/Baltimore_City_Food_Stores_2016.shp"

# remove gas stations, which CLF says they no longer consider for determining
# food deserts
stores = arcpy.SelectLayerByAttribute_management(
        stores, 
        "NEW_SELECTION", 
        '"Type" <> \'Gas Station\'')

# read in Baltimore City Council Districts. Source: Open Baltimore
districts = "/shapefiles_mdsp/council_district_2021_council_district.shp"

# use spatial join to determine which district each store is in
# and read in the result. The field name we will be interested in is
# "area_name" (1-14)
arcpy.SpatialJoin_analysis(stores, 
                           districts, 
                           "/shapefiles_mdsp/stores_districts")
stores = "/shapefiles_mdsp/stores_districts"

# use cursor to assign HFAI score based on district and store type
# again, these scores are from the Food Environment Briefs for each district
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
            
# you'll notice some of the HFAI values above are -999, and that's because
# according to the Food Environment Briefs, not all districts have each
# store type. we can now use a SearchCursor to verify that all the stores 
# are accounted for and none received a -999, which would be a problem
with arcpy.da.SearchCursor(
        stores, 
        ["OBJECTID"],
        '"HFAI" = -999') as cursor:
    for store in cursor:
        print(store[0]) # no stores are printed, so fine to continue
            
# now we need to calculate average HFAI at some area level
# CLF used census block groups in their analysis
            
# read in Maryland block groups. Source: Census TIGER/Line
md_bg = "/shapefiles_mdsp/tl_2021_24_bg.shp" 

# subset Baltimore City block groups, save as new shapefile, and read in
balt_bg = arcpy.SelectLayerByAttribute_management(
        md_bg, 
        "NEW_SELECTION", 
        '"COUNTYFP" = \'510\'')
arcpy.CopyFeatures_management(
        balt_bg, 
        "/shapefiles_mdsp/balt_bg")
balt_bg = "/shapefiles_mdsp/balt_bg.shp"

# use spatial join to calculate average HFAI by block group 
targetFeatures = os.path.join(balt_bg)
joinFeatures = os.path.join(stores)
outfc = os.path.join(outWorkspace, 
                     "Avg_HFAI")
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
Avg_HFAI = "shapefiles_mdsp/Avg_HFAI.shp" 
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

# For each food desert criteria, we will save the final 1/0 result as a 
# raster. The reason for this is that later we need to aggregate all the
# criteria to find which areas have all 3 criteria (food desert). Because
# not all our criteria will be at the same geographic level, saving the output
# of each as a raster easily allows us to combine them at the end
        
# set raster environment settings
arcpy.env.cellSize = "300" # 300 ft is average street block length
arcpy.env.mask = "/shapefiles_mdsp/balt_mask"

# save as raster
inFeature = Avg_HFAI
outRaster = "/rasters/hfai_fd.tif"
field = "HFAI_FD"
arcpy.FeatureToRaster_conversion(inFeature, 
                                 field, 
                                 outRaster)

# apparently mask is not an environment setting for FeatureToRaster, but we 
# can just use extract by mask to mask out industrial areas, water bodies, 
# transportation, and parks
inRaster = "/rasters/hfai_fd.tif"
inMaskData = "/shapefiles_mdsp/balt_mask"
outExtractByMask = arcpy.sa.ExtractByMask(inRaster, 
                                          inMaskData)
outExtractByMask.save("C:/Users/caraw/Documents/GEOG664/TermProject/" +
                      "rasters/hfai_fd_final.tif")

## (2) Distance to supermarker is more than 1/4 mile ##

# subset supermarkets from stores, save as new shapefile, and read in
supermarkets = arcpy.SelectLayerByAttribute_management(
        stores,
        "NEW_SELECTION",
        '"Type" = \'Supermarket\'')
arcpy.CopyFeatures_management(supermarkets,
                              "/shapefiles_mdsp/supermarkets")
supermarkets = "/shapefiles_mdsp/supermarkets.shp"

# create 1/4 mile buffers around supermarkets and dissolve
supermarketsBuffer = "/shapefiles_mdsp/supermarkets_buffer"
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
# this is needed to establish Baltimore City as the boundary of our raster
eraseOutput = "/shapefiles_mdsp/supermarkets_erase"
arcpy.Erase_analysis("/shapefiles_mdsp/balt_mask",
                     supermarketsBuffer,
                     eraseOutput)

# set a new field equal to 1 and then save as raster
# the previously set mask environment setting will work here
inFeature = "shapefiles_mdsp/supermarkets_erase.shp"
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
outRaster = "/rasters/supermarkets_fd.tif"
field = "Smkt_FD"
arcpy.FeatureToRaster_conversion(inFeature,
                                 field,
                                 outRaster)

# reclass raster so that all the null space (i.e., < 1/4 mile to supermarket)
# within the Baltmimore City mask is set to 0. Otherwise, there are errors 
# when trying to do raster math
inRaster = "/rasters/supermarkets_fd.tif"
reclassField = "Value"
remap = arcpy.sa.RemapValue([
        [1, 1],
        ["NODATA", 0]])
outReclassify = arcpy.sa.Reclassify(inRaster,
                                    reclassField,
                                    remap)
outReclassify.save("C:/Users/caraw/Documents/GEOG664/TermProject/rasters/"
                   "supermarkets_fd_final.tif")


## (3) Social Vulnerability Index (SVI) is high ##

# whereas CLF used income and vehicle access as their final two criteria,
# here we use the census tract-level SVI overall percentile ranking. This
# ranking captures socioeconomic status, household composition and disability,
# minority status and language, and housing type and transportation. We will
# use overall percentile ranking >= .9 as our criteria for a food desert.
# This represents the most vulnerable areas

# read in Maryland SVI. Source: CDC
md_svi = "/shapefiles_mdsp/SVI2018_MARYLAND_tract.shp"

# subset Baltimore City, save as new shapefile, and read in
balt_svi = arcpy.SelectLayerByAttribute_management(
        md_svi, 
        "NEW_SELECTION", 
        '"COUNTY" = \'Baltimore City\'')
arcpy.CopyFeatures_management(
        balt_svi, 
        "/shapefiles_mdsp/balt_svi")
balt_svi = "/shapefiles_mdsp/balt_svi.shp"

# use cursor to create binary variable indicating whether RPL_THEMES is >= .75
arcpy.AddField_management(balt_svi, 
                          "SVI_FD", 
                          "SHORT")
with arcpy.da.UpdateCursor(balt_svi, 
                           ["RPL_THEMES", 
                            "SVI_FD"]) as cursor:
    for tract in cursor:
        if tract[0] >= .9:
            tract[1] = 1
        else:
            tract[1] = 0
        cursor.updateRow(tract)

# save as raster
inFeature = balt_svi
outRaster = "/rasters/svi_fd.tif"
field = "SVI_FD"
arcpy.FeatureToRaster_conversion(inFeature, 
                                 field, 
                                 outRaster)

# use extract by mask to mask out industrial areas, water bodies, 
# transportation, and parks
inRaster = "/rasters/svi_fd.tif"
inMaskData = "/shapefiles_mdsp/balt_mask"
outExtractByMask = arcpy.sa.ExtractByMask(inRaster, 
                                          inMaskData)
outExtractByMask.save("C:/Users/caraw/Documents/GEOG664/TermProject/" +
                      "rasters/svi_fd_final.tif")

##########################
## CREATE FOOD DESERTS  ##
##########################

# first list out all the raster names
rasters = []
walk = arcpy.da.Walk(arcpy.env.workspace, 
                     topdown = True, 
                     datatype = "RasterDataset")
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        rasters.append(filename)
print(rasters)

# read in the three rasters we need (i.e., final 1/0 rasters)
fd_1 = arcpy.Raster("/rasters/hfai_fd_final.tif")
fd_2 = arcpy.Raster("/rasters/supermarkets_fd_final.tif")
fd_3 = arcpy.Raster("/rasters/svi_fd_final.tif")

# use raster math to multiply all three 1/0 rasters
fd = fd_1 * fd_2 * fd_3
fd.save("C:/Users/caraw/Documents/GEOG664/TermProject/rasters/fd_final.tif")