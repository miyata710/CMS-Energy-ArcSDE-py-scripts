'''
This script has been developed for the purpose of calculating the values for the Measured Length & Length Source fields.
####
'''
#Necessary modules 
import arcpy
import os

#create function for calculating the value for "Measured Length" field
def calculateML(feederID,dataPath,userWorkspace):
    #assign correct SQL statemnet
    if dataPath == priOH:
        SQL =  """(FEEDERID = '{0}') AND (SUBTYPECD <> 7)""".format(feederID)
        
    elif dataPath == priUG:
        SQL =  """(FEEDERID = '{0}') AND (SUBTYPECD <> 7)""".format(feederID)

    else:
        SQL =  """(FEEDERID = '{0}')""".format(feederID)
    
    searchFields = ["OBJECTID","SHAPE@LENGTH"]
    updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]
    feederField = "FEEDERID"
    measureField = "MEASUREDLENGTH"

    myDict = {}
    searchCursor = arcpy.da.SearchCursor(dataPath,searchFields,SQL)
    
    for row in searchCursor:
        objID = row[0]
        objLength =row[1]
        myDict[objID] = objLength
    del searchCursor

    #set workspace
    workspace = userWorkspace

    # Start an edit session. Must provide the worksapce.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data

    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()

    updateCursor = arcpy.da.UpdateCursor(dataPath,updateFields,SQL)
    for item in updateCursor:
        myLength = myDict[item[0]]
        item[1] = round(myLength*3.28084) #!added round() function at Tierney's request.
        item[2] = "FM" #!still in question
        updateCursor.updateRow(item)
    del updateCursor

    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
#### End function ####

#### Get input from user ####
# Script input parameters:
sdeWorkspace = arcpy.GetParameterAsText (0) #SDE Connection file
txt_input = arcpy.GetParameterAsText (1) # .txt file with feederIDs

#makes a list of feeder IDs from a TXT file
feederList = []

if txt_input :
    fhand = open(txt_input)
    for i in fhand:
        i = i.strip()
	feederList.append(str(i))
    fhand.close()

#Data Paths
#!!! do we need to add OH/UG Connector lines to this script???
#!!! SUBTYPECD <> 7
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(sdeWorkspace)
#!!!SUBTYPECD <> 7
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(sdeWorkspace)
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(sdeWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(sdeWorkspace)

#!dataList = [priOH, priUG, secOH, secUG]
dataList = [priOH]
#### Call and Execute calculate ML function on ALL necessary FCs####
for feeder in feederList:
    for data in dataList:
        calculateML(feeder, data, sdeWorkspace)
