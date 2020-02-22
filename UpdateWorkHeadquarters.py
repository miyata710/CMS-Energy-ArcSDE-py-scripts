'''
This script was developed to update the work headquarters field for the following feature classes in a batch process:
                    1.	Dynamic Protective Device
                    2.	Fuse
                    3.	Miscellaneous Network Features (MNF) 
                    4.	PF Correcting Equipment
                    5.	Primary Overhead Conductor
                    6.	Primary Underground Conductor
                    7.	Secondary Overhead Conductor
                    8.	Secondary Underground Conductor
                    9.	Switch
                    10.	Transformer
                    11.	Voltage Regulator
'''
def calculateHQ(feederID,dataPath,workHeadquarters):
    updateFields = ["WORKHEADQUARTERS"]
    feederField = "FEEDERID"
    workHQField = "WORKHEADQUARTERS"
    for feeder in feederID:
        SQL = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder)

        #set workspace
        workspace = #SDE connection file
        
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
        
        
#### Function Parameters ####
feederID = [

]
workHeadquarters = ''
priOH = r'xxxxxx\Primary Overhead Conductor'
priUG = r'xxxxxx\Primary Underground Conductor'
secOH = r'xxxxxx\Secondary Overhead Conductor'
secUG = r'xxxxxx\Secondary Underground Conductor'
dynProDev = r'xxxxxx\Protective Devices & Switches\Dynamic Protective Device'
fuse = r'xxxxxx\Protective Devices & Switches\Fuse'
switch = r'xxxxxx\Protective Devices & Switches\Switch'
miscNetFeat = r'xxxxxx\Tap Dots, T-points, & Wire Changes'
capacitor = r'xxxxxx\Primary Devices\Capacitors'
transformer = r'xxxxxx\Secondary Transformers'
regulatorBooster = r'xxxxxx\Primary Devices\Regulators & Boosters'

#### Call and Execute function on ALL necessary FCs####
calculateHQ(feederID, priOH, workHeadquarters)
calculateHQ(feederID, priUG, workHeadquarters)
calculateHQ(feederID, secOH, workHeadquarters)
calculateHQ(feederID, secUG, workHeadquarters)
calculateHQ(feederID, dynProDev, workHeadquarters)
calculateHQ(feederID, fuse, workHeadquarters)
calculateHQ(feederID, switch, workHeadquarters)
calculateHQ(feederID, miscNetFeat, workHeadquarters)
calculateHQ(feederID, capacitor, workHeadquarters)
calculateHQ(feederID, transformer, workHeadquarters)
calculateHQ(feederID, regulatorBooster, workHeadquarters)

### EOlson 05/2019 ###
### rosemary.erin.o@gmail.com ###
