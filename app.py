
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5 import QtTest

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

class ListNode:
    def __init__(self,val,dist,nextnode):
        self.val=val
        self.dist=dist
        self.nextnode=nextnode


class AdjList:
    def __init__(self,V):
        self.listarr=[None]*V

    def insert_edge(self,src,dest,dist):
        newnode=ListNode(dest,dist,self.listarr[src])
        self.listarr[src]=newnode

    def print_adjlist(self):
        print('Printing List')
        for i in self.listarr:
            j=i
            while(j):
                print('|',j.val,j.dist,end='|->')
                j=j.nextnode
            print('None')

    
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,640)
        self.gridh=640
        self.gridw=640
        self.gridx=160
        self.gridy=0
        self.boxh=20
        self.boxw=20
        self.rows=self.gridh//self.boxh
        self.cols=self.gridw//self.boxw
        self.count=0
        self.drawGrid()
        self.sidepanel=PanelWidget(self)
        self.speed=50

    def drawGrid(self):
        self.gridwid=GridWidget(self,self.gridh,self.gridw,self.boxh,self.boxw,self.gridx,self.gridy)

    def re_initGrid(self):
        self.count=0
        self.gridwid.re_init()
        self.sidepanel.clear_soln()

    def mousePressEvent(self,event):
        x,y=event.x(),event.y()
        if x<160:return
        row=(y-self.gridy)//self.boxh
        col=(x-self.gridx)//self.boxw
        boxnumber=row*self.cols+col
        color='(240,240,240)'
        if not self.count:
            self.gridwid.setsrc(boxnumber)
            self.gridwid.changeBoxColor(boxnumber,'red')
        elif self.count==1:
            self.gridwid.setdst(boxnumber)
            self.gridwid.changeBoxColor(boxnumber,'green')
        else:
            self.gridwid.changeBoxColor(boxnumber,'black')
            self.gridwid.deleteBox(boxnumber)
        self.count+=1
        

    def mouseMoveEvent(self,event):
        x,y=event.x(),event.y()
        if self.count>1 and x>=160:
            row=(y-self.gridy)//self.boxh
            col=(x-self.gridx)//self.boxw
            color='grey'
            boxnumber=row*self.cols+col
            self.gridwid.changeBoxColor(boxnumber,'black')
            self.gridwid.deleteBox(boxnumber)

    def callSolver(self,algo):
        solver=Solver(self.gridwid,self.sidepanel)

        if algo=='A*':solver.A_star(1024)
        elif algo=='Dijkstra':solver.dijkstra(1024)

        solver.find_path(self.gridwid.getsrc(),self.gridwid.getdst())
        ans=solver.getans()
        self.sidepanel.display_ans(ans)

    def clearSoln(self):
        self.gridwid.clear_soln()
        self.sidepanel.clear_soln()


    

class PanelWidget():
    def __init__(self,MainWindow):
        self.MainWindow=MainWindow
        self.setupUi()

    def setupUi(self):
        self.panel=QtWidgets.QFrame(self.MainWindow)
        self.panel.setGeometry(QtCore.QRect(0,0,160,640))
        self.panel.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.speedSlider = QtWidgets.QSlider(self.MainWindow)
        self.speedSlider.setGeometry(QtCore.QRect(30, 50, 100, 22))
        self.speedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider.setObjectName("speedSlider")
        self.speedSlider.valueChanged.connect(self.display_speed)

        self.sliderlabel = QtWidgets.QLabel(self.MainWindow)
        self.sliderlabel.setGeometry(QtCore.QRect(30, 70,100, 31))
        self.sliderlabel.setObjectName("sliderlabel")
        self.sliderlabel.setText('Visualizer Speed=1')

        self.label2 = QtWidgets.QLabel(self.MainWindow)
        self.label2.setGeometry(QtCore.QRect(10, 120,60, 31))
        self.label2.setObjectName("label2")
        self.label2.setText('Select Algo:')  

        self.comboBox = QtWidgets.QComboBox(self.MainWindow)
        self.comboBox.setGeometry(QtCore.QRect(75, 120, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Dijkstra")
        self.comboBox.addItem("A*")

        self.solveButton = QtWidgets.QPushButton(self.MainWindow)
        self.solveButton.setGeometry(QtCore.QRect(10, 170, 100, 23))
        self.solveButton.setObjectName("solveButton")
        self.solveButton.setText("Solve")
        self.solveButton.clicked.connect(lambda:self.MainWindow.callSolver(self.comboBox.currentText()))

        self.resetButton = QtWidgets.QPushButton(self.MainWindow)
        self.resetButton.setGeometry(QtCore.QRect(10, 250, 100, 23))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.setText("Reset")
        self.resetButton.clicked.connect(self.MainWindow.re_initGrid)

        self.clearButton = QtWidgets.QPushButton(self.MainWindow)
        self.clearButton.setGeometry(QtCore.QRect(10, 200, 100, 23))
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setText("Clear Solution")
        self.clearButton.clicked.connect(self.MainWindow.clearSoln)

        self.label3 = QtWidgets.QLabel(self.MainWindow)
        self.label3.setGeometry(QtCore.QRect(10, 280,60, 31))
        self.label3.setObjectName("label3")
        self.label3.setText('')

        
    def get_sliderSpeed(self):
        return self.speedSlider.value()+1

    def display_speed(self):
        self.sliderlabel.setText(f'Visualizer Speed={self.get_sliderSpeed()}')

    def display_ans(self,val):
        if val!=-1:
            self.label3.setText(f'Distance={val}')
        else:
            self.label3.setText('No Route found')
        self.label3.adjustSize()
    
    def clear_soln(self):
        self.label3.setText('')
        

class GridWidget():
    def __init__(self,MainWindow,gridh,gridw,boxh,boxw,gridx,gridy):
        self.MainWindow=MainWindow
        self.src=None
        self.dst=None
        self.gridheight=gridh
        self.gridwidth=gridw
        self.boxheight=boxh
        self.boxwidth=boxw
        self.gridx=gridx
        self.gridy=gridy
        self.setupUi()

    def re_init(self):
        self.src=None
        self.dst=None
        self.clear_obs()

    def clear_obs(self):
        self.boxpresent=[1]*(self.rows*self.cols)
        for boxnum in range(len(self.boxes)):
            self.changeBoxColor(boxnum,'rgb(240,240,240)')

    def clear_soln(self):
        for boxnum in range(len(self.boxes)):
            if self.boxpresent[boxnum] and boxnum!=self.src and boxnum!=self.dst:
                self.changeBoxColor(boxnum,'rgb(240,240,240)')

    def setupUi(self):
        self.boxes=[]
        self.rows=self.gridheight//self.boxheight
        self.cols=self.gridwidth//self.boxwidth
        self.boxpresent=[1]*(self.rows*self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                x=self.gridx+j*self.boxwidth
                y=self.gridy+i*self.boxheight
                box=QtWidgets.QFrame(self.MainWindow)
                box.setGeometry(QtCore.QRect(x,y, self.boxwidth, self.boxheight))
                box.setFrameShape(QtWidgets.QFrame.StyledPanel)
                box.setStyleSheet('background-color:rgb(240,240,240)')
                self.boxes.append(box)

    def changeBoxColor(self,boxnum,color):
        self.boxes[boxnum].setStyleSheet(f'background-color:{color}')

    def setsrc(self,boxnum):
        self.src=boxnum

    def getsrc(self):
        return self.src

    def setdst(self,boxnum):
        self.dst=boxnum

    def getdst(self):
        return self.dst

    def deleteBox(self,boxnum):
        self.boxpresent[boxnum]=0


class Solver:
    def __init__(self,widget,sidepanel):
        self.graph=AdjList(1024)
        self.parent={}
        self.ans={}
        self.src=widget.src
        self.dst=widget.dst
        self.widget=widget
        self.boxpresent=widget.boxpresent
        self.sidepanel=sidepanel
        self.connect_nodes()

    def connect_nodes(self):
        for row in range(32):
            for col in range(32):
                src=row*32+col
                if self.boxpresent[src]:
                    if row<31 and col>0 and self.boxpresent[src+31]:
                        self.graph.insert_edge(src,src+31,2**0.5)#dl
                    if row>0 and col>0 and self.boxpresent[src-33]:
                        self.graph.insert_edge(src,src-33,2**0.5)#ul
                    if row>0 and col<31 and self.boxpresent[src-31]:
                        self.graph.insert_edge(src,src-31,2**0.5)#ur
                    if row<31 and col<31 and self.boxpresent[src+33]:
                        self.graph.insert_edge(src,src+33,2**0.5)#dr
                    if row>0 and self.boxpresent[src-32]:
                        self.graph.insert_edge(src,src-32,1)#u
                    if row<31 and self.boxpresent[src+32]:
                        self.graph.insert_edge(src,src+32,1)#d
                    if col>0 and self.boxpresent[src-1]:
                        self.graph.insert_edge(src,src-1,1)#l
                    if col<31 and self.boxpresent[src+1]:
                        self.graph.insert_edge(src,src+1,1)#r


    def dijkstra(self,v):
        minhp=myHeap(v)
        minhp.insert_node(heapNode(self.src,0))
        while(minhp.arr):
            curr=minhp.extract_min()
            self.ans[curr.val]=curr.dist
            nbr=self.graph.listarr[curr.val]
            while(nbr):
                if not minhp.node_present(nbr.val):
                    minhp.insert_node(heapNode(nbr.val,nbr.dist+curr.dist))
                    self.parent[nbr.val]=curr.val
                elif nbr.val not in self.ans and minhp.get_dist(nbr.val)>curr.dist+nbr.dist:
                    minhp.reduce_dist(nbr.val,curr.dist+nbr.dist)
                    self.parent[nbr.val]=curr.val
                nbr=nbr.nextnode
            if curr.val==self.dst:break
            if curr.val!=self.src:self.widget.changeBoxColor(curr.val,'rgb(242,146,146)')
            QtTest.QTest.qWait(int(100/self.sidepanel.get_sliderSpeed()))

    def euc(self,s):
        sy=s//32
        sx=s%32
        dy=self.dst//32
        dx=self.dst%32
        d1=(abs(sy-dy))**2
        d2=(abs(sx-dx))**2
        ans=(d1+d2)**(0.5)
        return ans
        

    def A_star(self,v):
        minhp=myHeap(v)
        minhp.insert_node(heapNode(self.src,self.euc(self.src)))
        while(minhp.arr):
            curr=minhp.extract_min()
            self.ans[curr.val]=curr.dist
            nbr=self.graph.listarr[curr.val]
            currdist=curr.dist-self.euc(curr.val)
            while(nbr):
                if not minhp.node_present(nbr.val):
                    minhp.insert_node(heapNode(nbr.val,nbr.dist+currdist+self.euc(nbr.val)))
                    self.parent[nbr.val]=curr.val
                elif nbr.val not in self.ans and minhp.get_dist(nbr.val)-self.euc(nbr.val)>currdist+nbr.dist:
                    minhp.reduce_dist(nbr.val,currdist+nbr.dist+self.euc(nbr.val))
                    self.parent[nbr.val]=curr.val
                nbr=nbr.nextnode
            if curr.val==self.dst:break
            if curr.val!=self.src:self.widget.changeBoxColor(curr.val,'rgb(242,146,146)')
            QtTest.QTest.qWait(int(100/self.sidepanel.get_sliderSpeed()))


    def find_path(self,src,dst):
        if dst in self.parent and src!=dst:
            self.find_path(src,self.parent[dst])
        if dst!=self.dst and dst!=self.src:
            self.widget.changeBoxColor(dst,'blue')

    def print_graph(self):
        for node in self.graph.listarr[self.src:self.src+1]:
            edge=node
            while(edge):
                print(edge.val,'->',end='')
                edge=edge.nextnode
            print('None')

    def getans(self):
        if self.dst in self.ans:
            return self.ans[self.dst]
        else:
            return -1

        
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win1=MyWindow()
    win1.show()
    sys.exit(app.exec_())
    
main()