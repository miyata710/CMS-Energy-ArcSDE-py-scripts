'''
This script was developed to identify and retreive the object IDs of geometric network junctions (ArcFM) that are snapped
to a line feature class. All stranded geometric network junctions can be deleted by the GIS Analyst.
'''
#Arcmap settings
arcpy.env.addOutputsToMap = False

###input data paths###

#OH Connector Line
OHline = r'xxxxxx\xxxxxx\OH Connector Line'

#UG Connector Line
UGline = r'xxxxxx\xxxxxx\UG Connector Line'

#Primary Overhead dataset
priOH = r'xxxxxx\Primary Overhead Conductor'

#Primary Underground dataset
priUG = r'xxxxxx\Primary Underground Conductor'

#Secondary Overhead dataset
secOH = r'xxxxxx\Secondary Overhead Conductor'

#Secondary Underground dataset
secUG = r'xxxxxx\Secondary Underground Conductor'

#Geometric Network junctions dataset
geoNetJunct = r'xxxxxx\ELECDIST.ElectricGeomNetwork_Junctions'

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

### EOlson 01/2020 ###
### rosemary.erin.o@gmail.com ###
