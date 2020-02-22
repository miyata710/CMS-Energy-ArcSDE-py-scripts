'''
This script has been developed for the purpose of calculating the values for the Measured Length & Length Source fields in 
a batch process.
'''
#create function for calculating the value for "Measured Length" field
def calculateML(feederID,dataPath):
    searchFields = ["OBJECTID","SHAPE@LENGTH"]
    updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]
    feederField = "FEEDERID"
    measureField = "MEASUREDLENGTH"
    for feeder in feederID:
        SQL = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder)
        myDict = {}
        searchCursor = arcpy.da.SearchCursor(dataPath,searchFields,SQL)
        for row in searchCursor:
            objID = row[0]
            objLength =row[1]
            myDict[objID] = objLength
        del searchCursor

        #set workspace
        workspace = #SDE connection file
        
        # Start an edit session. Must provide the worksapce.
        edit = arcpy.da.Editor(workspace)
        
        # Edit session is started without an undo/redo stack for versioned data
        
        edit.startEditing(False, True)
        
        # Start an edit operation
        edit.startOperation()
        
        updateCursor = arcpy.da.UpdateCursor(dataPath,updateFields,SQL)
        for item in updateCursor:
            myLength = myDict[item[0]]
            item[1] = round(myLength*3.28084) 
            item[2] = "FM"
            updateCursor.updateRow(item)
        del updateCursor
        
        # Stop the edit operation.
        edit.stopOperation()
        
        # Stop the edit session and save the changes
        edit.stopEditing(True)
        
        
#### Function Parameters ####
feederID = [

]

priOH = r'xxxxxx\Primary Overhead Conductor'
priUG = r'xxxxxx\Primary Underground Conductor'
secOH = r'xxxxxx\Secondary Overhead Conductor'
secUG = r'xxxxxx\Secondary Underground Conductor'

#### Call and Execute calculate ML function on ALL necessary FCs####
calculateML(feederID, priOH)
calculateML(feederID, priUG)
calculateML(feederID, secOH)
calculateML(feederID, secUG)

### EOlson 05/2019 ###
### rosemary.erin.o@gmail.com ###
