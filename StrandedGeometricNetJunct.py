'''
This script is used to find and retreive the object IDs of geometric network junctions that are intersected by a line FC.
***When using this script be sure not to save any changes to the .mxd
'''
#Arcmap settings
arcpy.env.addOutputsToMap = False

###input data paths###

#OH Connector Line
OHline = r'Customers & Transformers\Transformer Connector Lines\OH Connector Line'

#UG Connector Line
UGline = r'Customers & Transformers\Transformer Connector Lines\UG Connector Line'

#Primary Overhead dataset
priOH = r'Primary Lines\Primary Overhead Conductor'

#Primary Underground dataset
priUG = r'Primary Lines\Primary Underground Conductor'

#Secondary Overhead dataset
secOH = r'Customers & Transformers\Secondary Overhead Conductor'

#Secondary Underground dataset
secUG = r'Customers & Transformers\Secondary Underground Conductor'

#Geometric Network junctions dataset
geoNetJunct = r'Misc Network Features\ELECDIST.ElectricGeomNetwork_Junctions'

###Find geometric network junctions attached to lines --> delete all others###

#list of geometric network junctions that are intersected by a layer in selectByList
geoNetJunctIntersectedList = []

#list of feature classes used in select by location analysis to find intersected geometric network junctions
selectByList = [OHline, UGline, priOH, priUG, secOH, secUG]

#Start looping through FCs

for i in selectByList:

    #create layer to select from
    myLyr = arcpy.MakeFeatureLayer_management(geoNetJunct, 'geoNetJunct_lyr')
    
    #select by location
    mySelection = arcpy.SelectLayerByLocation_management(myLyr,"INTERSECT",i,"","NEW_SELECTION")

    #search cursor used to append list of tap dot object IDs that are intersected by line feature to list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
        if row[0] not in geoNetJunctIntersectedList:
            geoNetJunctIntersectedList.append(row[0])
    
    del cursor

print geoNetJunctIntersectedList 
