'''
These functions were created to aid in the the reconstruction of production level data that was altered back to its original
geographic position.
'''

def temp_move(i):#sp move
    workspace = #SDE connection file
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    SQL ="DEVICELOCATION={}".format(i)
    cursor=arcpy.da.SearchCursor('''#path to archived service point FC''',["SHAPE@"],SQL)
    for row in cursor:
        sp_091601=row[0]        
        
    SQL="DEVICELOCATION={}".format(i)
    cursor=arcpy.da.UpdateCursor('''#path to existing service point FC in production''',["SHAPE@"],SQL)
    for row in cursor:
        row[0]=sp_091601
        cursor.updateRow(row)
    edit.stopOperation()


def tlm_move(i):
    workspace = #SDE connection file
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    SQL="TLM='{}'".format(i)
    cursor=arcpy.da.SearchCursor('''#path to archived transformer FC''',["SHAPE@"],SQL)
    for row in cursor:
        tlm_091601=row[0]        
        
    SQL="TLM='{}'".format(i)
    cursor=arcpy.da.UpdateCursor('''#path to existing transformer FC in production''',["SHAPE@"],SQL)
    for row in cursor:
        row[0]=tlm_091601
        cursor.updateRow(row)  
    edit.stopOperation()

### EOlson 01/2020 ###
### rosemary.erin.o@gmail.com ###
