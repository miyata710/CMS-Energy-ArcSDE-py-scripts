def temp_move(a):#sp move
    workspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    where="DEVICELOCATION={}".format(a)
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\temp_091601.gdb\ServicePoint',["SHAPE@"],where)
    for row in cursor:
        sp_091601=row[0]        
        
    where="DEVICELOCATION={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=sp_091601
        cursor.updateRow(row)
    edit.stopOperation()


def tlm_move(a):
    workspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    where="TLM='{}'".format(a)
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\temp_091601.gdb\Transformers',["SHAPE@"],where)
    for row in cursor:
        tlm_091601=row[0]        
        
    where="TLM='{}'".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Transformer',["SHAPE@"],where)
    for row in cursor:
        row[0]=tlm_091601
        cursor.updateRow(row)
        
    edit.stopOperation()
