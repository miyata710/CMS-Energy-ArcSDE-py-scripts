'''
########## PRODUCTION SCRIPT ##########
This script was developed for the purpose of updating the Operating Voltage fields for select feature classes. Operating 
voltages are only updated on feeder IDs without isolators. Any feeder IDs that contain isolators will be printed at the 
end of the program so GIS Analysts can easily identify and update them manually. 
'''


########## FUNCTION TO UPDATE OPERATING VOLTAGE OF FEATURE CLASSES ##########

def updateOpVoltage(opVoltage,dataPath,feederID): 
  
    #create an update cursor and update "OPERATINGVOLTAGE" field with opVoltage value
    SQL =  """(FEEDERID = '{0}' AND NOT OPERATINGVOLTAGE = {1}) OR (FEEDERID = '{0}' AND OPERATINGVOLTAGE IS NULL)""".format(feederID, opVoltage)
    
    #Start Editing operation
    #set workspace
    workspace = 

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
def secOpVoltage(dataPath,feederID):
    
    #create an update cursor and update "OPERATINGVOLTAGE" field with opVoltage value
    SQL =  """(FEEDERID = '{0}' AND NOT OPERATINGVOLTAGE = 30) OR (FEEDERID = '{0}' AND OPERATINGVOLTAGE IS NULL)""".format(feederID)
    
    #Start Editing operation
    #set workspace
    workspace = 

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
  

####Data paths being updated by updateOpVoltage() function####
dynamicProtectiveDevice = r'xxxxxx\xxxxxx\Dynamic Protective Device'
fuse = r'xxxxxx\xxxxxx\Fuse'
miscNetFeat = r'xxxxxx\Tap Dots, T-points, & Wire Changes'
capacitor = r'xxxxxx\Primary Devices\Capacitors'
priOH = r'xxxxxx\Primary Overhead Conductor'
priUG = r'xxxxxx\Primary Underground Conductor'
switch = r'xxxxxx\xxxxxx\Switch'
transformer = r'xxxxxx\Secondary Transformers'
voltageRegulator = r'xxxxxx\Primary Devices\Regulators & Boosters'

#### Data paths updated by secOpVoltage() function ####
secOH = r'xxxxxx\Secondary Overhead Conductor'
secUG = r'xxxxxx\Secondary Underground Conductor'

####Input tables####
isolator = r'xxxxxx\Primary Devices\Isolator'
circuitSource = #input local path to circuit source table 

#### Initiate for loop to loop through list of Feeder IDs ####
feederIDList = [

]

#variable for tracking feeder IDs with isolators
hasIsolator = []

for feeder in feederIDList: 
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
    
    #call to function to update operating voltage 
    updateOpVoltage(operatingVoltage,dynamicProtectiveDevice,feeder)
    updateOpVoltage(operatingVoltage,fuse,feeder)
    updateOpVoltage(operatingVoltage,miscNetFeat,feeder)
    updateOpVoltage(operatingVoltage,capacitor,feeder)
    updateOpVoltage(operatingVoltage,priOH,feeder)
    updateOpVoltage(operatingVoltage,priUG,feeder)
    updateOpVoltage(operatingVoltage,switch,feeder)
    updateOpVoltage(operatingVoltage,transformer,feeder)
    updateOpVoltage(operatingVoltage,voltageRegulator,feeder)
    
    #call secOpVoltage function
    secOpVoltage(secOH,feeder)
    secOpVoltage(secUG,feeder)

  else:
    hasIsolator.append(feeder)
    
if len(hasIsolator) > 0:
  #Print full list of feederIDs with isolators
  print hasIsolator
  
### EOlson 09/2019 ###
### rosemary.erin.o@gmail.com ###
