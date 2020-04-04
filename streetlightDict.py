
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
  
print len(feederList)

#creat new clean list
newList = []
for j in feederList:
  j = j[-1]
  j = str(j)
  newList.append(j)


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
  
print len(myDict)

### Need to update Streetlight FeederID field ###
#feederID field is sub + circuit
streetlight = r'Structures Group Layer\Streetlight'
workHQ = r'Org Bounds\Electric Distribution WHQ(Scale<300,000)'

hqList = ['FRE', 'GVL', 'TRA', 'JAC', 'LAN', 'BEN','KAL','LDG','GRE', 'MDL', 'BIG','CLR','BCY','FLT','HST','SAG','BNC','MUS','GRA',
'HML','CAD','WBR','UNK','BCK','TWS','OWS','GRN']

SQL = """FEEDERID IS NULL""" 
cursor = arcpy.da.UpdateCursor(streetlight, ["FEEDERID","SUBSTATIONID","CIRCUITID"], SQL)
for row in cursor:
  row[0] = row[1] + row[2]
  cursor.updateRow(row)
del cursor
