#!{9: ['f', 7], 7: ['s', 4], 13: ['f', 113], 6: ['s', 2], 1: ['f', 28]}

myDict = {9: ['f', 7], 7: ['s', 4], 13: ['f', 113], 6: ['s', 2], 1: ['f', 28]}
fList = []
sList = []
dList = []

for key in myDict:
    if myDict[key][0] == 'f':
        fList.append(myDict[key][1])
    elif myDict[key][0] == 's':
        sList.append(myDict[key][1])
    elif myDict[key][0] == 'd':
        dList.append(myDict[key][1])

fTup = tuple(fList)
sTup = tuple(sList)
dTup = tuple(dList)

#extract data switch, fuse, dpd
def queryData(tup):
    where = 'WHERE OBJECTID IN {}'.format(tup)
    if tup == fTup:
        cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Fuse',["OID@","SHAPE@"],where+" AND PHASEDESIGNATION= 7")
        fuse=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    elif tup == dTup:
        cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@"],where+" AND PHASEDESIGNATION= 7")
        dpd=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    elif tip == sTup:
        cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@"],where+" AND PHASEDESIGNATION= 7")
        swi=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]

  

