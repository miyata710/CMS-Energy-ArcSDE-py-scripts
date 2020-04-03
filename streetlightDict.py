'''
this block of code retrieves a list of feederIDs that need to have their streetlight's traced
'''
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
  
  
