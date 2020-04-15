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
def calculateHQ(feederID,dataPath,workHeadquarters):
    updateFields = ["WORKHEADQUARTERS"]
    feederField = "FEEDERID"
    workHQField = "WORKHEADQUARTERS"
    for feeder in feederID:
        SQL = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder)

        #set workspace
        workspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'
        
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

###Data paths being updated by calculateHQ() function####

#!!! SUBTYPECD <> 7
priOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment".format(userWorkspace)
#!!!SUBTYPECD <> 7
priUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment".format(userWorkspace)
secOH = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment".format(userWorkspace)
secUG = "{0}\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment".format(userWorkspace)
dynProDev = "{0}\\ELECDIST.ElectricDist\\ELECDIST.DynamicProtectiveDevice".format(userWorkspace)
fuse = r'Devices\Protective Devices & Switches\Fuse'
switch = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Switch".format(userWorkspace)
miscNetFeat = "{0}\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature".format(userWorkspace)
#!!!capacitors from PF correcting  subtypes 1, 2
capacitor = "{0}\\ELECDIST.ElectricDist\\ELECDIST.PFCorrectingEquipment".format(userWorkspace)
#!!!SUBTYPECD <> 10 and (INSTALLATIONTYPE <> 'UN' or INSTALLATIONTYPE is null)
transformer = "{0}\\ELECDIST.ElectricDist\\ELECDIST.Transformer".format(userWorkspace)
#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = "{0}\\ELECDIST.ElectricDist\\ELECDIST.VoltageRegulator".format(userWorkspace)

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
