'''
This script is being developed for the purpose of updating the work headquarters field for the following feature classes:
                    1.	Dynamic Protective Device
                    2.	Fuse
                    3.	Miscellaneous Network Features (MNF) 
                    4.	PF Correcting Equipment (Capacitor in ArcMap TOC)
                    5.	Primary Overhead Conductor
                    6.	Primary Underground Conductor
                    7.	Secondary Overhead Conductor
                    8.	Secondary Underground Conductor
                    9.	Switch
                    10.	Transformer
                    11.	Voltage Regulator (Regulators and Boosters in ArcMap TOC)
                    
                    **** Maybe remove the "IS NULL" part of the SQL selection so every record for a feederID is updated properly ****

'''
#Necessary modules 
import arcpy
import os

#ArcMap Settings
arcpy.env.addOutputsToMap = False

def calculateHQ(feederID,dataPath,workHeadquarters,userWorkspace):
    #assign correct SQL statemnet
    if dataPath == capacitor:
      SQL =  """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 2)""".format(feederID)

    elif dataPath == priOH:
        SQL =  """(FEEDERID = {0}) AND (SUBTYPECD <> 7)""".format(feederID)
        
    elif dataPath == priUG:
        SQL =  """(FEEDERID = {0}) AND (SUBTYPECD <> 7)""".format(feederID)

    elif dataPath == transformer:
        SQL =  """(FEEDERID = {0}) AND (SUBTYPECD <> 10) AND (INSTALLATIONTYPE <> 'UN' OR INSTALLATIONTYPE IS NULL) """.format(feederID)

    elif dataPath == rb:
        SQL =  """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 5 OR SUBTYPECD = 8 OR SUBTYPECD = 11)""".format(feederID)

    else:
        SQL =  """(FEEDERID = {0})""".format(feederID)
    
    for feeder in feederID:
    
    updateFields = ["WORKHEADQUARTERS"]
    feederField = "FEEDERID"
    workHQField = "WORKHEADQUARTERS"
    #set workspace
    workspace = userWorkspace

    # Start an edit session. Must provide the worksapce.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data
    #  (for second argument, use False for unversioned data)
    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()

    updateCursor = arcpy.da.UpdateCursor(dataPath,updateFields,SQL)
    for row in updateCursor:
        row[0] = workHeadquarters
        updateCursor.updateRow(row)
    del updateCursor

    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
       
#### Get input from user ####
# Script input parameters:
userWorkspace = arcpy.GetParameterAsText (0) #SDE Connection file
txt_input = arcpy.GetParameterAsText (1) # .txt file with feederIDs 
workHQ_input = arcpy.GetParameterAsText (2) # work headquarters code

#makes a list of feeder IDs from a TXT file
feederList = []
if txt_input :
	fhand = open(txt_input)
	for i in fhand:
		i = i.strip()
		feederList.append(str(i))
	fhand.close()

###Data paths being updated by calculateHQ() function####

#!!! SUBTYPECD <> 7
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(userWorkspace)
#!!!SUBTYPECD <> 7
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(userWorkspace)
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(userWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(userWorkspace)
dynProDev = "{0}\\ELECDIST.ElectricDist\\ELECDIST.DynamicProtectiveDevice".format(userWorkspace)
fuse = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Fuse".format(userWorkspace)
switch = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Switch".format(userWorkspace)
miscNetFeat = "{0}\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature".format(userWorkspace)
#!!!capacitors from PF correcting  subtypes 1, 2
capacitor = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PFCorrectingEquipment".format(userWorkspace)
#!!!SUBTYPECD <> 10 and (INSTALLATIONTYPE <> 'UN' or INSTALLATIONTYPE is null)
transformer = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Transformer".format(userWorkspace)
#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = "{0}\\ELECDIST.ElectricDist\\ELECDIST.VoltageRegulator".format(userWorkspace)

#### Call and Execute function on ALL necessary FCs####
calculateHQ(feederList, priOH, workHQ_input)
calculateHQ(feederList, priUG, workHQ_input)
calculateHQ(feederList, secOH, workHQ_input)
calculateHQ(feederList, secUG, workHQ_input)
calculateHQ(feederList, dynProDev, workHQ_input)
calculateHQ(feederList, fuse, workHQ_input)
calculateHQ(feederList, switch, workHQ_input)
calculateHQ(feederList, miscNetFeat, workHQ_input)
calculateHQ(feederList, capacitor, workHQ_input)
calculateHQ(feederList, transformer, workHQ_input)
calculateHQ(feederList, regulatorBooster, workHQ_input)
