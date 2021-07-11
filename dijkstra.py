import sys
graph=[[0,1,1,3],[1,0,0,1],[1,0,0,1],[3,1,1,0]]


src=2
parent={}
def dijkstra(src,v):
    distarr=[sys.maxsize]*v
    distarr[src]=0
    ans={}
    minnode=0
    while(len(ans)!=len(graph)):
        i=0
        mindist=sys.maxsize
        while(i<len(distarr)):
            if distarr[i]<mindist and i not in ans:
                mindist=distarr[i]
                minnode=i
            i+=1
        ans[minnode]=mindist
        for i in range(len(graph[minnode])):
            if graph[minnode][i] and distarr[i]>graph[minnode][i]+mindist:
                distarr[i]=graph[minnode][i]+mindist
                #parent[i]=minnode
    return ans
ans=dijkstra(0,4)
print(ans)
#print(parent)
'''def findpath(src,dest):
    if src!=dest:findpath(src,parent[dest])
    print(dest)
    '''
findpath(0,3)

        
            
        


