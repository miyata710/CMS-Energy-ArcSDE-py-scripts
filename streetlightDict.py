
#this block of code retrieves a list of feederIDs that need to have their streetlight's traced

circuitBound = r'Org Bounds\Circuit Boundaries'
hqList = ['FRE', 'GVL', 'TRA', 'JAC', 'LAN', 'BEN','KAL','LDG','GRE', 'MDL', 'BIG','CLR','BCY','FLT','HST','SAG','BNC','MUS','GRA',
'HML','CAD','WBR','UNK','BCK','TWS','OWS','GRN']

#for storing a list of every single feederID we need to conduct trace on
feederList = []

for i in hqList:
  SQL = """HDQ = '{}'""".format(i)
  #!print SQL
  cursor = arcpy.da.SearchCursor(circuitBound, "FEEDERID", SQL) 
  for row in cursor:
    feederList.append(row)
  del cursor
  

#creat new clean list
newList = []
for j in feederList:
  j = j[-1]
  j = str(j)
  newList.append(j)
print newList

#Now we need to search the streetlight FC by feederID.
#We will have a single dictionary where feederid is key and a list of streetlight OBJIDs associated with that feeder will be value.


streetlight = r'Structures Group Layer\Streetlight'
myDict = {}
for k in newList:
  SQL = """FEEDERID = '{}'""".format(k)
  
  objList = []
  cursor = arcpy.da.SearchCursor(streetlight, "OBJECTID", SQL) 
  for row in cursor:
    row = row[-1]
    objList.append(row)
  del cursor
  
  myDict[k] = objList
  
print myDict

### Need to update Streetlight FeederID field ###
#data
streetlight = r'E:\Data\Streetlight_TLM\Data\PROD_DATABASE_04032020.gdb\ElectricDist\Streetlight'
workHQ = r'E:\Data\ESME\Landbase.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
#list of releavnt HQ
#!hqList = ['FRE', 'GVL', 'TRA', 'JAC', 'LAN', 'BEN','KAL','LDG','GRE', 'MDL', 'BIG','CLR','BCY','FLT','HST','SAG','BNC','MUS','GRA',
#!'HML','CAD','WBR','UNK','BCK','TWS','OWS','GRN']
hqList = ['BIG','CLR','BCY','FLT','HST','SAG','BNC','MUS','GRA','HML','CAD','WBR','UNK','BCK','TWS','OWS','GRN']
#streetlight SQL statement
SQL = """FEEDERID IS NULL""" 
for hq in hqList:
  SQL1 = """BOUNDARYNAMECD = '{}'""".format(hq) 
  
  #make a layer of specific work HQ
  hqLyr = arcpy.MakeFeatureLayer_management(workHQ,'in_memory\\hqData_lyr', SQL1)
 
  # make a layer of streetlights w/ null feederID
  lightLyr = arcpy.MakeFeatureLayer_management(streetlight,'in_memory\\lightData_lyr', SQL)
  
  #select by location
  lightDataSel = arcpy.SelectLayerByLocation_management(lightLyr,"COMPLETELY_WITHIN",hqLyr,"","NEW_SELECTION")
  
  #update work HQ field in streetlight layer
  #inputDataLyr OBJID's List
  dataUpdateList = []

  #loop through lightDataSel and append object IDs to list
  with arcpy.da.SearchCursor(lightDataSel, ["OBJECTID"]) as cursor:
    for row in cursor:
      dataUpdateList.append(row[0])
  
  for j in dataUpdateList:  
    with arcpy.da.UpdateCursor(streetlight, ["WORKHEADQUARTERS"], """OBJECTID ={0}""".format(j)) as cursor:
      for row in cursor:
        row[0] = hq
        cursor.updateRow(row)
  arcpy.Delete_management(hqLyr)
  arcpy.Delete_management(lightLyr)
  
  
