
colour = ['black'] * N 
#print len(colour)
distance =[9999] * N
#print len(distance)

# Breath First Search Algorithm

colour[start_p]='red'

directed_gr=copy.deepcopy(undirected_gr)
distance[start_p]=0

# rever_gr stores predecessor of every vertax
revers_gr = [0 for i in range(N)] 

#print len(distance),len(colour),len(directed_gr)

qu=list() 
	
for v in directed_gr[start_p]:
    distance[v]=1
    qu.append(v)
    revers_gr[v]=start_p

while len(qu)>0:
    u=qu.pop(0)
    colour[u]='red'
    for v in undirected_gr[u]:        
        if distance[v]<distance[u]:
            directed_gr[u].remove(v)
        elif colour[v]=='black':
            qu.append(v)
            if distance[v]>distance[u]+1:
                distance[v]=distance[u]+1
                revers_gr[v]=u

# print directed_gr==undirected_gr
# print revers_gr[start_p] 
 
