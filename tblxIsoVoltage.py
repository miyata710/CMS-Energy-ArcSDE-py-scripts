'''
########## PDM_Prod.mxd Production server -- script ##########

This script was developed for the purpose of updating the Operating Voltage field on relevant feature classes
for feeder IDs that have isolators on their circuit. This script is run by analysts as they traverse through known
isolators, perform downstream traces, and update the voltages with the proper value assessed from the Seconday Transformer
layer in the .mxd.  
'''

########## FUNCTION TO UPDATE OPERATING VOLTAGE OF FEATURE CLASSES ##########

def updateOpVoltage(opVoltage,dataPath,userWorkspace):

    #construct SQL based on .mxd layer query
    if dataPath == capacitor:
        SQL =  """(NOT OPERATINGVOLTAGE = {0} OR OPERATINGVOLTAGE IS NULL) AND (SUBTYPECD = 1 OR SUBTYPECD = 2)""".format(opVoltage)

    elif dataPath == priOH:
        SQL =  """(NOT OPERATINGVOLTAGE = {0} OR OPERATINGVOLTAGE IS NULL) AND (SUBTYPECD <> 7)""".format(opVoltage)

    elif dataPath == priUG:
        SQL =  """(NOT OPERATINGVOLTAGE = {0} OR OPERATINGVOLTAGE IS NULL) AND (SUBTYPECD <> 7)""".format(opVoltage)

    elif dataPath == transformer:
        SQL =  """(NOT OPERATINGVOLTAGE = {0} OR OPERATINGVOLTAGE IS NULL) AND (SUBTYPECD <> 10) AND (INSTALLATIONTYPE <> 'UN' OR INSTALLATIONTYPE IS NULL) """.format(opVoltage)

    elif dataPath == rb:
        SQL =  """(NOT OPERATINGVOLTAGE = {0} OR OPERATINGVOLTAGE IS NULL) AND (SUBTYPECD = 1 OR SUBTYPECD = 5 OR SUBTYPECD = 8 OR SUBTYPECD = 11)""".format(opVoltage)

    else:
        SQL =  """(NOT OPERATINGVOLTAGE = {0}) OR (OPERATINGVOLTAGE IS NULL)""".format(opVoltage)

    #create an update cursor and update "OPERATINGVOLTAGE" field with opVoltage value
    
    
    #Start Editing operation
    #set workspace
    workspace = userWorkspace

    # Start an edit session. Must provide the worksapce.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data

    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()
    
    #return all records in input dataPath with matching feederid and only provide "OPERATINGVOLTAGE" field for updating
    updateCursor = arcpy.da.UpdateCursor(dataPath, "OPERATINGVOLTAGE", SQL)

    #track number of features per feature class that are updated
    count = 0
    
    for row in updateCursor:
      row[0] = opVoltage
      updateCursor.updateRow(row)
      count += 1
    del updateCursor
    
    # Stop the edit operation and commit edits
    edit.stopOperation()

    #End edit session
    edit.stopEditing(True)

    #print messages based on dataset for count variable
    spltPath = dataPath.split(".")
    spltPath.reverse()
    printThis = spltPath[0]
    #Prints the data path and number of records updated to the tool dialog box
    #!arcpy.AddMessage("{0}: {1}").format(printThis,count)
    print ("{0}: {1}").format(printThis,count)

########## END OF FUNCTION ########## 

########## SECONDARY LINE OP VOLTAGE FUNCTION ##########
def secOpVoltage(dataPath,userWorkspace):
    
    #create an update cursor and update "OPERATINGVOLTAGE" field with opVoltage value
    SQL =  """(NOT OPERATINGVOLTAGE = 30) OR (OPERATINGVOLTAGE IS NULL)"""
    
    #Start Editing operation
    #set workspace
    workspace = userWorkspace

    # Start an edit session. Must provide the worksapce.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data

    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()
    
    #return all records in input dataPath with matching feederid and only provide "OPERATINGVOLTAGE" field for updating
    updateCursor = arcpy.da.UpdateCursor(dataPath, "OPERATINGVOLTAGE", SQL)

    #track number of features per feature class that are updated
    count = 0
    
    for row in updateCursor:
      row[0] = "30" 
      updateCursor.updateRow(row)
      count += 1
    del updateCursor
    
    # Stop the edit operation.
    edit.stopOperation()

    #End edit session
    edit.stopEditing(True)

    #print messages based on dataset for count variable
    spltPath = dataPath.split(".")
    spltPath.reverse()
    printThis = spltPath[0]
    #Prints the data path and number of records updated to the tool dialog box
    #!arcpy.AddMessage("{0}: {1}").format(printThis,count)
    print ("{0}: {1}").format(printThis,count)

########## END OF FUNCTION ##########
  
#### Get input from user ####
# Script input parameters:
#!userWorkspace = arcpy.GetParameterAsText (0)
#!opVoltageValue = arcpy.GetParameterAsText (1)
userWorkspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'
opVoltageValue = 160

opVoltage = str(opVoltageValue)

####Data paths being updated by updateOpVoltage() function####
dynamicProtectiveDevice = "{0}\\ELECDIST.ElectricDist\\ELECDIST.DynamicProtectiveDevice".format(userWorkspace)
fuse = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Fuse".format(userWorkspace)
miscNetFeat = "{0}\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature".format(userWorkspace)
switch = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Switch".format(userWorkspace)

#!!!capacitors from PF correcting  subtypes 1, 2
capacitor = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PFCorrectingEquipment".format(userWorkspace)

#!!! SUBTYPECD <> 7
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(userWorkspace)

#!!!SUBTYPECD <> 7
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(userWorkspace)

#!!!SUBTYPECD <> 10 and (INSTALLATIONTYPE <> 'UN' or INSTALLATIONTYPE is null)
transformer = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Transformer".format(userWorkspace)

#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = "{0}\\ELECDIST.ElectricDist\\ELECDIST.VoltageRegulator".format(userWorkspace)

#### Data paths updated by secOpVoltage() function ####
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(userWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(userWorkspace)

#main data paths
#!listMainData = [dynamicProtectiveDevice, fuse, miscNetFeat, switch, capacitor, priOH, priUG, transformer, rb]
listMainData = [dynamicProtectiveDevice]
#secondary data paths
listSecondaryData = [secOH, secUG]

for i in listMainData:
  print i
  #call to function to update operating voltage 
  updateOpVoltage(opVoltage,i,userWorkspace)
  
for j in listSecondaryData:
    print j
    secOpVoltage(j,userWorkspace)

### EOlson 03/2020 ###
### rosemary.erin.o@gmail.com ###
