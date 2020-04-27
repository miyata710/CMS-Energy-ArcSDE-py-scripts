f='1365'
'''
def extract_data():
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriOHElectricLineSegment',["SHAPE@"],"SUBTYPECD!=7")
    PriOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriUGElectricLineSegment',["SHAPE@"],"SUBTYPECD!=7")
    PriUG=[i[0] for i in cursor]
    Pri_lines=PriOH+PriUG
    lines=[[(i.firstPoint.X,i.firstPoint.Y),(i.lastPoint.X,i.lastPoint.Y)] for i in Pri_lines]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Fuse',["OID@","SHAPE@"])
    fuse=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@"])
    dpd=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@"],"SUBSTATIONDEVICE='Y'")
    start_p=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@"])
    swi=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@"],"TieSwitchIndicator = 'Y'")
    swi_tie=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]   
    return lines,fuse,dpd,swi,swi_tie,start_p
'''
#lines = creates a nested list of tuples with the 1st (x,y) and last (x,y) point
#fu = creates a nested list of tuples with the (x,y) of fuse and an ID for every fuse
#dp = creates a nested list of tuples with the (x,y) of DPD and an ID for every DPD
#swi = creates a nested list of tuples with the (x,y) of switch and an ID for every switch
#swi_tie = creates a nested list of tuples with the (x,y) of tie switch and an ID for every tie switch
#start = creates a nested list of tuples with the (x,y) of dpd at the substation and an ID for the dpd at the substation

def extract_data():
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\PriOH',["SHAPE@"],"NOT SUBTYPECD =7")
    PriOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\PriUG',["SHAPE@"],"NOT SUBTYPECD =7")
    PriUG=[i[0] for i in cursor]
    Pri_lines=PriOH+PriUG
    lines=[[(i.firstPoint.X,i.firstPoint.Y),(i.lastPoint.X,i.lastPoint.Y)] for i in Pri_lines]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\Fuse',["OID@","SHAPE@"])
    fuse=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\DPD',["OID@","SHAPE@"])
    dpd=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\DPD',["OID@","SHAPE@"],"SUBSTATIONDEVICE='Y'")
    start_p=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\Switch',["OID@","SHAPE@"])
    swi=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\Switch',["OID@","SHAPE@"],"TieSwitchIndicator = 'Y'")
    swi_tie=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]   
    return lines,fuse,dpd,swi,swi_tie,start_p

lines,fu,dp,sw,sw_t,start=extract_data()

def get_pt(edges):
    import functools 
    lines=[]
    p_s=list(set([functools.reduce(lambda x,y:x+y,edges)][0]))
    print 'number of points: ',len(p_s)
    hash_pts=dict([[p_s[n],n] for n in range(len(p_s))])
    print 'number of hash dict: ',len(hash_pts)
    pts_dict={}
    for k in hash_pts:
        pts_dict[hash_pts[k]]=k
    print 'number of pts: ',len(pts_dict)
    for i in edges:
        pt1=hash_pts[i[0]]
        pt2=hash_pts[i[1]]   
        line=[pt1,pt2] 
        lines.append(line)
    print 'number of lines: ',len(lines)
    return pts_dict,lines

p_dict,line_id=get_pt(lines)

pts_list=p_dict.items()
pts_list.sort(key=lambda r:r[1][0])#sort based on x value,1s
l=len(pts_list)

dup_del=[]
repl=[]
for i in range(1,l):
    if abs(pts_list[i][1][0]-pts_list[i-1][1][0])<0.01:
        if abs(pts_list[i][1][1]-pts_list[i-1][1][1])<0.01:
            print "warning: connection issues happens in ",pts_list[i],pts_list[i-1]
            # convert pts_list[i-1] to pts_list[i]
            # update line_id list
            d1=pts_list.pop(i-1)
            dup_del.append(d1[0])
            repl.append(pts_list[i][0]) 

print len(dup_del),len(repl)

            for j in line_id:
                if j[0]==pts_list[i-1][0]:
                    j[0]=pts_list[i][0] 
                if j[1]==pts_list[i-1][0]:
                    j[1]=pts_list[i][0] 
            pts_list.pop(i-1)


