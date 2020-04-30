#####Start: Get Tie Switch Feature Information#####

#SQL determines which Tie switches are valid and therefore selected
SQL= "(TieSwitchIndicator = 'Y') and (NOT FEEDERID IS NULL AND NOT FEEDERID2 IS NULL)"
cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\nodeTrace.gdb\Switch',["OID@","SHAPE@","FEEDERID","FEEDERID2"],SQL)
tie_switch_id=[]
tie_switch_xy=[]
tie_switch_feeder1=[]
tie_switch_feeder2=[]

for row in cursor:
    tie_switch_id.append(row[0])
    pt=row[1].firstPoint
    tie_switch_xy.append([pt.X,pt.Y])
    tie_switch_feeder1.append(row[2])
    tie_switch_feeder2.append(row[3])

tie_switch_fd_dict={}
for i in range(len(tie_switch_id)):
    tie_switch_fd_dict[tie_switch_id[i]]=[tie_switch_feeder1[i],tie_switch_feeder2[i]]
'''
tie_switch_xy_dict
{290: [475111.2571292563, 315974.3557968451], 287: [474206.93290441413, 316899.0348377063]}
'''
#creates dictionary of (x,y) values for valid tie switches key = OBJID : value = (x,y)
tie_switch_xy_dict={}
for i in range(len(tie_switch_id)):
    tie_switch_xy_dict[tie_switch_id[i]]=tie_switch_xy[i]

#####End: Tie switch information extraction#####

# this extracts the necessary feature class data per feederID
def extract_data(fid):
    where="FEEDERID = '{}'".format(fid)
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriOHElectricLineSegment',["SHAPE@"],"{} AND SUBTYPECD != 7 AND PHASEDESIGNATION = 7".format(where))
    PriOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriUGElectricLineSegment',["SHAPE@"],"{} AND SUBTYPECD != 7 AND PHASEDESIGNATION = 7".format(where))
    PriUG=[i[0] for i in cursor]
    Pri_lines=PriOH+PriUG
    lines=[[(i.firstPoint.X,i.firstPoint.Y),(i.lastPoint.X,i.lastPoint.Y)] for i in Pri_lines]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Fuse',["OID@","SHAPE@"],where)
    fuse=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@"],where)
    dpd=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@"],where+" and SUBSTATIONDEVICE='Y'")
    start_p=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@"],where)
    swi=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@"],where +" and TieSwitchIndicator = 'Y' and (not FEEDERID IS NULL AND NOT FEEDERID2 IS NULL)")
    sw_t=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i in cursor]
    return lines,fuse,dpd,swi,sw_t,start_p

# lines,fu,dp,sw,sw_t,start=extract_data(f)


def get_pt(edges):
    import functools 
    lines=[]
    p_s=list(set([functools.reduce(lambda x,y:x+y,edges)][0]))
    print 'number of points: ',len(p_s) #! will we need these print statements?
    hash_pts=dict([[p_s[n],n] for n in range(len(p_s))])
    print 'number of hash dict: ',len(hash_pts)#! will we need these print statements?
    pts_dict={}
    for k in hash_pts:
        pts_dict[hash_pts[k]]=k
    print 'number of pts: ',len(pts_dict)#! will we need these print statements?
    for i in edges:
        pt1=hash_pts[i[0]]
        pt2=hash_pts[i[1]]   
        line=[pt1,pt2] 
        lines.append(line)
    print 'number of lines: ',len(lines)#! will we need these print statements?
    return pts_dict,lines


p_dict,line_id=get_pt(lines)
# revise connectivity
pts_list=p_dict.items()
pts_list.sort(key=lambda r:r[1][0])#sort based on x value,1s                                     

#check the x,y distance between the points in sorted point list
#if the x,y distance is less than 0.1 meter, there will be a incorrect connection between two lines
for i in range(1,len(pts_list)):
    if abs(pts_list[i][1][0]-pts_list[i-1][1][0])<0.1: #absolute x distance
        if abs(pts_list[i][1][1]-pts_list[i-1][1][1])<0.1: #absolute y distance
            print pts_list[i],pts_list[i-1]  #! will we need this print statements?
'''
print result:
(56, (472855.1140231551, 315589.41198848665)) (86, (472855.11389515514, 315589.4122444866))
(150, (472859.87639115955, 315585.44347648293)) (8, (472859.8760071596, 315585.4430284829))
56,86 are same point
150,8 are same point
few connected primary 3_phased lines are not connected properly. 
this problem could be solved by replace 86 by 56, replace 8 by 150
following code solve the problem
'''
removed_pt=[]# store the pt needs to be removed
replaced_pt=[]# store the pt needs to replace removed pt
for i in range(1,len(pts_list)):
    if abs(pts_list[i][1][0]-pts_list[i-1][1][0])<0.1: #absolute x distance
        if abs(pts_list[i][1][1]-pts_list[i-1][1][1])<0.1: #absolute y distance
            removed_pt.append(pts_list[i][0])
            replaced_pt.append(pts_list[i-1][0])

#remove the pt in pt_dictionary
for i in range(len(removed_pt)):
    p_dict.pop(removed_pt[i])
#remove the pt in line_id,
for i in line_id:
    if i[0] in removed_pt:
        ind1=removed_pt.index(i[0])
        #print ind1,i
        i[0]=replaced_pt[ind1]
        #print i
    if i[1] in removed_pt:
        ind2=removed_pt.index(i[1])
        #print ind2
        i[1]=replaced_pt[ind2]
        #print i

#sort pt list again
pts_list=p_dict.items()
pts_list.sort(key=lambda r:r[1][0])

print len(pts_list),len(line_id)

def binary_search(arr,key):
    low=0
    high=len(arr)-1
    while (low<=high):
        mid=(low+high)//2
        a1=arr[mid][1]
        a2=key
        if abs(a1[0]-a2[0])<=0.1:
            return mid
        elif a2[0]<a1[0]:
            high=mid-1
        elif a2[0]>a1[0]:
            low=mid+1                   
    return -1  

#assigns every node a number and associates device ID with it
def convert_pt(devices,plist):
    pt_n={}
    for i in devices:
        n=binary_search(plist,i[1])
        if n!=-1:
            #print n,i[0]
            pt_n[plist[n][0]]=i[0]
        #else:
            #print n,i[0] 
    return pt_n
###!!!sort the point list based on x value, search the point recursively, and assign the point number to a device
fu_pid=convert_pt(fu,pts_list)
sw_pid=convert_pt(sw,pts_list)
dp_pid=convert_pt(dp,pts_list)
sw_t_pid=convert_pt(sw_t,pts_list)
#{208: 910738, 30: 794897}
start_pt=convert_pt(start,pts_list)
start_pt=start_pt.keys()[0]
# [[321, (602357.8310077637, 246262.91547591984)]]

def create_graph(pts,edges):
    undirected_graph={}
    for v in pts:
        #print v
        undirected_graph[v[0]]=[]
    for i in edges:
        #print i
        if i[1] not in undirected_graph[i[0]]:
            undirected_graph[i[0]].append(i[1])
        if i[0] not in undirected_graph[i[1]]:
            undirected_graph[i[1]].append(i[0]) 
    return undirected_graph

# un_graph=create_graph(pts_list,line_id)



#start_pt
#p_dict

def bfs(graph, initial):    
    import copy
    directed_g=copy.deepcopy(graph)
    reverse_g={initial:-1}
    queue = [initial] 
    while len(queue)>0:        
        node = queue.pop(0)         
        neighbours = directed_g[node]           
        for neighbour in neighbours:
            reverse_g[neighbour]=node
            queue.append(neighbour)
            if node in directed_g[neighbour]:
                directed_g[neighbour].remove(node)
    return directed_g,reverse_g
d_gr,r_gr=bfs(un_graph,start_pt)



# find path from start to end 

def get_paths(d_gr,r_gr):
    paths=[]
    end_points=[k for k in d_gr if len(d_gr[k])==0]
    for i in end_points:    
        node=r_gr[i]
        r=[i,node] 
        while node>0:
            node=r_gr[node]
            if node!=-1:
                r.append(node)
        paths.append(r)
    print paths
    return paths

routs=get_paths(d_gr,r_gr)
for i in routs:
    i.reverse()


#! what exactly is this returning???
def upstream_trace_device(reversed_graph, tie_switch, devices):
    st_rout={}
    for i in reversed_graph:
        print i
        for j in tie_switch:
            print j
            if j in i:
                print "i'm in here"
                st_rout[j]=i
    print st_rout
    st_near_device=[]     
    for k in st_rout:
        print k 
        k_inx=st_rout[k].index(k)   
        one_tie_sw=[]
        for u in devices:
            print u
            if u in st_rout[k]:
                device_inx=st_rout[k].index(u)
                print device_inx
                one_tie_sw.append([k_inx, device_inx])
        st_near_device.append(one_tie_sw)
    print st_near_device
    return st_near_device

      
#!upstream_trace_device(routs,sw_t_pid.keys(),fu_pid.keys())
upstream_trace_device(routs,sw_t_pid.keys(),p_dict.keys()) 
# find the nearby switches

upstream_trace_device(sw_t_pid.keys(),sw_pid.keys())
