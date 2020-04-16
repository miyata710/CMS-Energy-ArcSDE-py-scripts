'''
########## PRODUCTION SCRIPT ##########
This script is being developed for the purpose of updating the Operating Voltage fields for select feature classes. Operating voltages
are only updated on feeder IDs without isolators and any feeder IDs that contain isolators will be printed at the end of the program. 
'''

########## FUNCTION TO UPDATE OPERATING VOLTAGE OF FEATURE CLASSES ##########

def updateOpVoltage(opVoltage,dataPath,feederID,userWorkspace):
    #assign correct SQL statemnet
    if dataPath == capacitor:
        SQL =  """(FEEDERID = '{0}') AND (SUBTYPECD = 1 OR SUBTYPECD = 2) AND (OPERATINGVOLTAGE IS NULL OR NOT OPERATINGVOLTAGE= '{1}')""".format(feederID,opVoltage)

    elif dataPath == transformer:
        SQL =  """(FEEDERID = '{0}') AND (SUBTYPECD <> 10) AND (INSTALLATIONTYPE <> 'UN' OR INSTALLATIONTYPE IS NULL) AND (OPERATINGVOLTAGE IS NULL OR NOT OPERATINGVOLTAGE= '{1}')""".format(feederID,opVoltage)

    elif dataPath == rb:
        SQL =  """(FEEDERID = '{0}') AND (SUBTYPECD = 1 OR SUBTYPECD = 5 OR SUBTYPECD = 8 OR SUBTYPECD = 11)AND (OPERATINGVOLTAGE IS NULL OR NOT OPERATINGVOLTAGE= '{1}')""".format(feederID,opVoltage)

    else:
        SQL =  """(FEEDERID = '{0}') AND (OPERATINGVOLTAGE IS NULL OR NOT OPERATINGVOLTAGE= '{1}')""".format(feederID,opVoltage)
    
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
    
    for row in updateCursor:
        row[0] = str(opVoltage)
        updateCursor.updateRow(row)
    del updateCursor
    
    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
 ########## END OF FUNCTION ########## 

########## SECONDARY LINE OP VOLTAGE FUNCTION ##########
def secOpVoltage(dataPath,feederID,userWorkspace):
    
    #create an update cursor and update "OPERATINGVOLTAGE" field with opVoltage value
    SQL =  """(FEEDERID = '{0}') AND (OPERATINGVOLTAGE IS NULL OR NOT OPERATINGVOLTAGE= 30)""".format(feederID)
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
    
    for row in updateCursor:
        row[0] = "30" 
        updateCursor.updateRow(row)
    del updateCursor
    
    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)

########## END OF FUNCTION ##########

# Script input parameters:
#!sdeWorkspace = arcpy.GetParameterAsText (0) #SDE Connection file
#!txt_input = arcpy.GetParameterAsText (1) # .txt file with feederIDs 
sdeWorkspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'

#makes a list of feeder IDs from a TXT file
feederList = ['142702','142703']
'''
if txt_input :
    fhand = open(txt_input)
    for i in fhand:
        i = i.strip()
	feederList.append(str(i))
    fhand.close()
'''
####Data paths being updated by updateOpVoltage() function####
dynProDev = "{0}\\ELECDIST.ElectricDist\\ELECDIST.DynamicProtectiveDevice".format(sdeWorkspace)
fuse = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Fuse".format(sdeWorkspace)
miscNetFeat = "{0}\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature".format(sdeWorkspace)
#!!!capacitors from PF correcting  subtypes 1, 2
capacitor = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PFCorrectingEquipment".format(sdeWorkspace)
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(sdeWorkspace) #updates OH Connector line
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(sdeWorkspace) #updates UG Connector line
switch = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Switch".format(sdeWorkspace)
#!!!SUBTYPECD <> 10 and (INSTALLATIONTYPE <> 'UN' or INSTALLATIONTYPE is null)
transformer = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Transformer".format(sdeWorkspace)
#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = "{0}\\ELECDIST.ElectricDist\\ELECDIST.VoltageRegulator".format(sdeWorkspace)

#main data paths to loop through
dataList = [dynProDev, fuse, miscNetFeat, capacitor, priOH, priUG, switch, transformer, rb]

#### Data paths updated by secOpVoltage() function ####
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(sdeWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(sdeWorkspace)

#list of secondary data to loop through
secList = [secOH, secUG]

####Input tables####
#!!! SUBTYPECD = 10
isolator = "{0}\\ELECDIST.ElectricDist\ELECDIST.Transformer".format(sdeWorkspace)
circuitSource = "{0}\\ELECDIST.CircuitSource".format(sdeWorkspace)

#variable for tracking feeder IDs with isolators
hasIsolator = []

for feeder in feederList: 
    ####Check input feederID for Isolators####
    #variables used for SQL statement
    SQL = """SUBTYPECD = 10 AND FEEDERID = '{0}'""".format(feeder)
    
    cursor = arcpy.da.SearchCursor(isolator, "FEEDERID", SQL)

    #counter for counting number of rows returned from cursor
    count = 0 

    for row in cursor:
        count += 1
    del cursor

    if count == 0: #execute code to find correct operating voltage

        #determine correct operating voltage value from circuit source table 
        SQL = """FEEDERID = '{0}'""".format(feeder)
    
        cursor = arcpy.da.SearchCursor(circuitSource, "OPERATINGVOLTAGE", SQL)
    
        for row in cursor:
            operatingVoltage = row[0]
        del cursor
        #!plan for if operating voltage = NULL?
    
        for data in dataList:
            #call to function to update operating voltage 
            updateOpVoltage(operatingVoltage,data,feeder,sdeWorkspace)
    
        for sec in secList: 
            #call secOpVoltage function
            secOpVoltage(sec,feeder,sdeWorkspace)

    else:
        hasIsolator.append(feeder)
    
if len(hasIsolator) > 0:
    #Print full list of feederIDs with isolators
    print ("Feeder ID's with isolators:")
    print hasIsolator
### EOlson 09/2019 ###
### rosemary.erin.o@gmail.com ###
