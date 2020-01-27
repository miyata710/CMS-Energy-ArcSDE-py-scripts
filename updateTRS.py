#Necessary modules 
import arcpy
import os

#ArcMap Settings
arcpy.env.addOutputsToMap = False

####START FUNCTION####
def checkData(input_feeder,input_data):
  #rowCount used to determine if input data has records with NULL Town Range Section field to be updated
  rowCount = 0
  #checking input data path for null records. If no null records STOP
  if input_data == capacitors:
    #do special search on subtype
    with arcpy.da.SearchCursor(capacitors, "OBJECTID", """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 2) AND (TRS IS NULL)""".format(input_feeder)) as cursor:
      for row in cursor:
        rowCount += 1
      if rowCount == 0:
        return False
      else:
        return True
  elif input_data == isolator:
    with arcpy.da.SearchCursor(isolator, "OBJECTID", """(FEEDERID = {0}) AND (SUBTYPECD = 10) AND (TRS IS NULL)""".format(input_feeder)) as cursor:
      for row in cursor:
        rowCount += 1
      if rowCount == 0:
        return False
      else:
        return True
  elif input_data == rb:
    with arcpy.da.SearchCursor(rb, "OBJECTID", """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 5 OR SUBTYPECD = 8 OR SUBTYPECD = 11) AND (TRS IS NULL)""".format(input_feeder)) as cursor:
      for row in cursor:
        rowCount += 1
      if rowCount == 0:
        return False
      else:
        return True
  else:
    with arcpy.da.SearchCursor(input_data, "OBJECTID", """FEEDERID = '{0}' AND (TRS IS NULL)""".format(input_feeder)) as cursor:
      for row in cursor:
        rowCount += 1
      if rowCount == 0:
        return False
      else:
        return True
####END FUNCTION####

####START FUNCTION####
def trsFunct(feeder,data):  
  trs = r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.SectionPoly'
  #create layer from trs FC to conduct select by location
  trsLyr = arcpy.MakeFeatureLayer_management(trs, 'in_memory\\trsOutput_lyr')

  #create layer from input data 
  if data == capacitors:
    #sql query to select only relevant records
    sql = """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 2) AND (TRS IS NULL)""".format(feeder)
    #make layer from input data
    inputDataLyr = arcpy.MakeFeatureLayer_management(data, 'in_memory\\inputData_lyr', sql)
  elif data == isolator:
    #sql query to select only relevant records
    sql = """(FEEDERID = {0}) AND (SUBTYPECD = 10) AND (TRS IS NULL)""".format(feeder)
    #make layer from input data
    inputDataLyr = arcpy.MakeFeatureLayer_management(data, 'in_memory\\inputData_lyr', sql)
  elif data == rb:
    #sql query to select only relevant records
    sql = """(FEEDERID = {0}) AND (SUBTYPECD = 1 OR SUBTYPECD = 5 OR SUBTYPECD = 8 OR SUBTYPECD = 11) AND (TRS IS NULL)""".format(feeder)
    #make layer from input data
    inputDataLyr = arcpy.MakeFeatureLayer_management(data, 'in_memory\\inputData_lyr', sql)
  else:
    #sql query to select only relevant records
    sql = """FEEDERID = '{0}' AND (TRS IS NULL)""".format(feeder)
    #make layer from input data
    inputDataLyr = arcpy.MakeFeatureLayer_management(data, 'in_memory\\inputData_lyr', sql)

  #conduct select by location (select all TRS polygons that contain features from inputDataLyr)
  trsPolygonSel = arcpy.SelectLayerByLocation_management(trsLyr,"CONTAINS",inputDataLyr,"","NEW_SELECTION")

  #list of TRS polygon object IDs that contain features in the dataPathLyr
  trsDict = {}

  #search cursor used to append list of TRS polygon object IDs that contain features in the dataPathLyr to a list
  with arcpy.da.SearchCursor(trsPolygonSel, ["OBJECTID","SECTIONNAME"]) as cursor:
    for row in cursor:
      trsDict[row[0]] = str(row[1]) #trsDict[OBJECTID] = [SECTIONNAME]

  ####Select By Location of inputDataLyr to individual TRS polygons####
  for i in trsDict: #loops through Object IDs (keys) in dictionary
    sql = """OBJECTID = {0}""".format(i)

    #create layer w/specific object ID from TRS FC to conduct select by location from
    trsSinglePoly = arcpy.MakeFeatureLayer_management(trs, 'in_memory\\trsSinglePoly_lyr', sql)

    #select by location
    singleDataSel = arcpy.SelectLayerByLocation_management(inputDataLyr,"COMPLETELY_WITHIN",trsSinglePoly,"","NEW_SELECTION")

    #inputDataLyr OBJID's List
    dataUpdateList = []

    #loop through singleDataSel and append object IDs to list
    with arcpy.da.SearchCursor(singleDataSel, ["OBJECTID"]) as cursor:
      for row in cursor:
        dataUpdateList.append(row[0])

    #set workspace
    workspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'

    # Start an edit session. Must provide the worksapce.
    edit = arcpy.da.Editor(workspace)

    # Edit session is started without an undo/redo stack for versioned data
    #  (for second argument, use False for unversioned data)
    edit.startEditing(False, True)

    # Start an edit operation
    edit.startOperation()

    #loop through dataUpdateList and update rows with correct TRS section name 
    for j in dataUpdateList: #input dataset Object ID
      with arcpy.da.UpdateCursor(data, "TRS", """OBJECTID ={0}""".format(j)) as cursor: #cursor running on input dataset
        for row in cursor:
          #!sectionName = trsDict[i]
          #!row[0] = sectionName
          row[0] = trsDict[i]
          cursor.updateRow(row) 

    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)

    #delete trsSinglePoly_lyr so we can make another in next iteration
    arcpy.Delete_management(trsSinglePoly)

  #delete remaining layers once function finished so they no longer exist when the function called again      
  arcpy.Delete_management(trsLyr)
  arcpy.Delete_management(inputDataLyr)
####END FUNCTION####

#### Get input from user ####
# Script input parameters:
csv_input = arcpy.GetParameterAsText (0)
single_input = arcpy.GetParameterAsText (1)

#makes a list of feeder IDs from a TXT file
csvList = []
if csv_input :
	fhand = open(csv_input)
	for i in fhand:
		i = i.rstrip()
		csvList.append(str(i))

#makes a list of feeder IDs from a single entry
singleList = []
if single_input :
	singleList = [str(single_input)]
	
#makes a combined list from the CSV file and single entry	
if len(csvList) > 0 and len(singleList) > 0:
	feederList = csvList + singleList
elif len(csvList) > 0 and len(singleList) == 0:
	feederList = csvList
elif len(csvList) == 0 and len(singleList) > 0:
	feederList = singleList

#set data paths
miscNetFeat = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.MiscNetworkFeature'
fuse = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Fuse'
dpd = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice'
switch = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch'
#!!!capacitors from PF correcting  subtypes 1, 2
capacitors = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PFCorrectingEquipment'
#!!!isolator from Transformer fc subtypes 10
isolator = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Transformer'
#!!!rb from voltage regulator fc subtypes 1, 5, 8, 11
rb = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.VoltageRegulator'

#list of all input data paths to loop through
dataPathList = [capacitors, isolator, rb, fuse, dpd, switch, miscNetFeat]
feederList = [
'040901',
'040901',
'040903',
'147601',
'147602'
]
### This is all for checking if the input data needs to be updated ###
for feederID in feederList:
  for inData in dataPathList:
    if checkData(feederID,inData) == True:
      trsFunct(feederID,inData)
    else:
      continue
