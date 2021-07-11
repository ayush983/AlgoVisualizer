class heapNode:
	def __init__(self,val,dist):
		self.val=val
		self.dist=dist

class myHeap:
	def __init__(self,v):
		self.arr=[]
		self.pos=[-1]*(v+1)
		self.length=0

	def swap_nodes(self,i,j):
		self.arr[i],self.arr[j]=self.arr[j],self.arr[i]

	def swap_pos(self,i,j):
		self.pos[i],self.pos[j]=self.pos[j],self.pos[i]

	def heapify_siftup(self,i):
		pidx=(i-1)//2
		if pidx>=0 and self.arr[pidx].dist>self.arr[i].dist:
			self.swap_nodes(pidx,i)
			self.swap_pos(self.arr[i].val,self.arr[pidx].val)
			self.heapify_siftup(pidx)

	def insert_node(self,ele):
		self.arr.append(ele)
		self.length+=1
		self.pos[ele.val]=self.length-1
		self.heapify_siftup(self.length-1)
	
	def heapify_siftdown(self,i):
		if 2*i+2<self.length and self.arr[2*i+1].dist>self.arr[2*i+2].dist:
			minidx=2*i+2
		elif 2*i+1<self.length:
			minidx=2*i+1
		else:
			return
		if self.arr[i].dist>self.arr[minidx].dist:
			self.swap_nodes(i,minidx)
			self.swap_pos(self.arr[i].val,self.arr[minidx].val)
			self.heapify_siftdown(minidx)

	def print_heap(self):
		print(self.arr)

	def extract_min(self):
		minval=self.arr[0]
		self.swap_nodes(0,self.length-1)
		self.swap_pos(self.arr[0].val,self.arr[self.length-1].val)
		self.arr.pop()
		self.length-=1
		self.heapify_siftdown(0)
		return minval

	def node_present(self,i):
		if self.pos[i]==-1:return 0
		return 1

	def reduce_dist(self,i,d):
		self.arr[self.pos[i]].dist=d
		self.heapify_siftup(self.pos[i])

	def get_dist(self,i):
		return self.arr[self.pos[i]].dist

'''
h=myHeap(8)
h.insert_node([1,16])
h.insert_node([6,15])
h.insert_node([8,14])
h.insert_node([3,13])
h.insert_node([2,12])
h.print_heap()
h.reduce_dist(8,7)
#minval=h.extract_min()
h.print_heap()
'''
class ListNode:
	def __init__(self,val,dist,nextnode):
		self.val=val
		self.dist=dist
		self.nextnode=nextnode


class AdjList:
	def __init__(self,V):
		self.listarr=[None]*V

	def insert_node(self,src,dest,dist):
		newnode=ListNode(dest,dist,self.listarr[src])
		self.listarr[src]=newnode

		newnode1=ListNode(src,dist,self.listarr[dest])
		self.listarr[dest]=newnode1

	def print_adjlist(self):
		print('Printing List')
		for i in self.listarr:
			j=i
			while(j):
				print('|',j.val,j.dist,end='|->')
				j=j.nextnode
			print('None')

	def delete_node(self,src,dest):
		curr=self.listarr[src]
		prev=None
		while(curr.val!=dest):
			prev=curr
			curr=curr.nextnode
		if prev:
			prev.nextnode=curr.nextnode
		else:
			self.listarr[src]=curr.nextnode
		

		curr=self.listarr[dest]
		prev=None
		while(curr.val!=src):
			prev=curr
			curr=curr.nextnode
		if prev:
			prev.nextnode=curr.nextnode
		else:
			self.listarr[dest]=curr.nextnode
'''
mygraph=AdjList(4)
mygraph.insert_node(0,1,1)
mygraph.insert_node(0,2,1)
mygraph.insert_node(0,3,3)
mygraph.insert_node(1,3,1)
parent={}
'''
#mygraph.print_adjlist()
#nextnode=myList.listarr[0].nextnode
#myList.listarr[0].nextnode=nextnode.nextnode
#print(myList.listarr[0].nextnode)
#myList.delete_node(0,2)
#myList.print_adjlist()
def dijkstra(src,v):
	ans={}
	minheap=myHeap(v)
	minheap.insert_node(heapNode(src,0))
	for _ in range(v):
		closest=minheap.extract_min()
		ans[closest.val]=closest.dist
		neighbour=mygraph.listarr[closest.val]
		while(neighbour):
			if not minheap.node_present(neighbour.val):
				minheap.insert_node(heapNode(neighbour.val,neighbour.dist))
				parent[neighbour.val]=closest.val
			elif neighbour.val not in ans and minheap.get_dist(neighbour.val)>closest.dist+neighbour.dist:
				minheap.reduce_dist(neighbour.val,closest.dist+neighbour.dist)
				parent[neighbour.val]=closest.val
			neighbour=neighbour.nextnode
	print(ans)
	print(parent)

def find_path(src,dest):
	if src!=dest:
		find_path(src,parent[dest])
	print(dest)

dijkstra(0,4)
find_path(0,3)










