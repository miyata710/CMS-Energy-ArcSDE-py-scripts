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
sdeWorkspace = arcpy.GetParameterAsText (0) #SDE Connection file
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
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(sdeWorkspace)
#!!!SUBTYPECD <> 7
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(sdeWorkspace)
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(sdeWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(sdeWorkspace)
dynProDev = "{0}\\ELECDIST.ElectricDist\\ELECDIST.DynamicProtectiveDevice".format(sdeWorkspace)
fuse = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Fuse".format(sdeWorkspace)
switch = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Switch".format(sdeWorkspace)
miscNetFeat = "{0}\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature".format(sdeWorkspace)
#!!!capacitors from PF correcting  subtypes 1, 2
capacitor = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PFCorrectingEquipment".format(sdeWorkspace)
#!!!SUBTYPECD <> 10 and (INSTALLATIONTYPE <> 'UN' or INSTALLATIONTYPE is null)
transformer = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Transformer".format(sdeWorkspace)
#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = "{0}\\ELECDIST.ElectricDist\\ELECDIST.VoltageRegulator".format(sdeWorkspace)

#### Call and Execute function on ALL necessary FCs####
calculateHQ(feederList, priOH, workHQ_input, sdeWorkspace)
calculateHQ(feederList, priUG, workHQ_input, sdeWorkspace)
calculateHQ(feederList, secOH, workHQ_input, sdeWorkspace)
calculateHQ(feederList, secUG, workHQ_input, sdeWorkspace)
calculateHQ(feederList, dynProDev, workHQ_input, sdeWorkspace)
calculateHQ(feederList, fuse, workHQ_input, sdeWorkspace)
calculateHQ(feederList, switch, workHQ_input, sdeWorkspace)
calculateHQ(feederList, miscNetFeat, workHQ_input, sdeWorkspace)
calculateHQ(feederList, capacitor, workHQ_input, sdeWorkspace)
calculateHQ(feederList, transformer, workHQ_input, sdeWorkspace)
calculateHQ(feederList, regulatorBooster, workHQ_input, sdeWorkspace)
