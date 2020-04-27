#changed this section to use a more restricting SQL cause to only collect data of valid tie switches
SQL= "(TieSwitchIndicator = 'Y') and (not FEEDERID IS NULL AND NOT FEEDERID2 IS NULL)"
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

#creates dictionary of (x,y) values for valid tie switches key = OBJID : value = (x,y)
tie_switch_xy_dict={}
for i in range(len(tie_switch_id)):
    tie_switch_xy_dict[tie_switch_id[i]]=tie_switch_xy[i]

# this extracts the necessary feature class data per feederID
#this code is giving me trouble....
#works "better" coming from prod but still issues
def extract_data(fid):
    where="FEEDERID = '{}'".format(fid)
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriOHElectricLineSegment',["SHAPE@"],"{} AND SUBTYPECD != 7 AND PHASEDESIGNATION = 7".format(where))
    PriOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriUGElectricLineSegment',["SHAPE@"],"{} AND SUBTYPECD != 7 AND PHASEDESIGNATION = 7".format(where))
    #CODE RIGHT BELOW SEEMS TO FAIL???
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


# p_dict,line_id=get_pt(lines)
# revise connectivity
pts_list=p_dict.items()
pts_list.sort(key=lambda r:r[1][0])#sort based on x value,1s                                     

def binary_search(arr,key):
    low=0
    high=len(arr)-1
    while (low<=high):
        mid=(low+high)//2
        a1=arr[mid][1]
        a2=key
        if a1==a2:
            return mid
        elif a2<a1:
            high=mid-1
        elif a2>a1:
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
start_pt=convert_pt(start,pts_list)
start_pt=start_pt.items()[0][0]
# [[321, (602357.8310077637, 246262.91547591984)]]

def create_graph(pts,edges):
    undirected_graph={}
    for v in pts:
        print v
        undirected_graph[v[0]]=[]
    for i in edges:
        print i
        if i[1] not in undirected_graph[i[0]]:
            undirected_graph[i[0]].append(i[1])
        if i[0] not in undirected_graph[i[1]]:
            undirected_graph[i[1]].append(i[0]) 
    return undirected_graph

# un_graph=create_graph(pts_list,line_id)



start_pt
p_dict

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
