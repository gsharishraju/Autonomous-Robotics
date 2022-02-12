#Learnt and tested pygame functions and syntax from https://www.pygame.org/docs/ref/rect.html
#https://csteach488.github.io/assets/docs/extras/pygame/sprites/sprites-animating-images.pdf
#https://coderedirect.com/questions/243829/how-to-spawn-a-sprite-after-a-time-limit-and-how-to-display-a-timer-pygame
#https://towardsdatascience.com/how-does-a-robot-plan-a-path-in-its-environment-b8e9519c738b
#https://swiz23.github.io/Portfolio/rrt.html
#Referred a lot of tutorials but forgot to save the link to them
import random
import math
import pygame

#Contains objects and properties for drawing obstacles and base map with start and goal coordinates
class Map:
    def __init__(self,start,goal,Dimensions,obsdimension,obsnumber):
        self.start =start
        self.goal =goal
        self.Dimensions =Dimensions
        self.height,self.width =self.Dimensions
        self.map = pygame.display.set_mode((self.width,self.height))
        self.map.fill((255,255,255))
        self.obstacles =[]
        self.obsdimension =obsdimension
        self.obsNumber =obsnumber
        self.grey =(70,70,70)
        self.Blue =(0,0,255)
        self.Green =(0,255,0)
        self.Red =(255,0,0)
        self.white =(255,255,255)
        self.black=(0,0,0)
        self.edgethickness=1


#function to draw map and start,goal coordinates
    def drawmap(self, obstacles):
        pygame.draw.circle(self.map,self.Red,self.start,20,0)
        pygame.draw.circle(self.map,self.Green,self.goal,20,0)
        self.drawobstacles(obstacles)

#function used to draw the obstacles on the map
    def drawobstacles(self,obstacles):
        obslist=obstacles.copy()
        while (len(obslist) > 0):
            obstacle=obslist.pop(0)
            pygame.draw.rect(self.map,self.Blue,obstacle)

#function used to draw final path to goal
    def drawPath(self,path):
        for node in path:
            pygame.draw.circle(self.map,self.Red,node,3,0)


class Graph:
    def __init__(self,start,goal,Dimensions,obsdimension,obsnumber):
        (x,y) = start
        self.start=start
        self.goal=goal
        self.goalflag=False
        self.height,self.width=Dimensions
        self.x=[]
        self.y=[]
        self.parent=[]
        # initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        #obstacles
        self.obstacles=[]
        self.obsDimension=obsdimension
        self.obsNumber=obsnumber
        #path
        self.goalstate=None
        self.path=[]

# function used to generate random coordinates for rectangle obstacles
    def makeRect(self):
        x=int(random.uniform(0,self.width-self.obsDimension))
        y=int(random.uniform(0,self.height-self.obsDimension))
        return (x,y)

#Function used to generate random rectangle obstacles. Function also checks to see whether start and goal are placed on obstacles
    def makeobs(self):
        obs=[]
        for i in range(0,self.obsNumber):
            rectangl=None
            collision=True
            while collision:
                upper=self.makeRect()
                rectangl=pygame.Rect(upper,(self.obsDimension,self.obsDimension))
                if rectangl.collidepoint(self.start) or rectangl.collidepoint(self.goal):
                    collision=True
                else:
                    collision=False
            obs.append(rectangl)
        self.obstacles=obs.copy()
        return obs
# function that adds node to the map
    def addnode(self,n,x,y):
        self.x.insert(n,x)
        self.y.append(y)
# function that is used to pop a node
    def removenode(self,n):
        self.x.pop(n)
        self.y.pop(n)
#Function used to establish relationship between parent and child to create an edge
    def addedge(self,parent,child):
        self.parent.insert(child,parent)

    def nodecount(self):
        return len(self.x)
#fUNCTION USED to find distance between two nodes based on euclidean distance
    def distance(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        tx=(float(x1)-float(x2))**2
        ty=(float(y1)-float(y2))**2
        return (tx+ty)**(0.5)
#function used to generate random samples for nodes to placed
    def randomsamples(self):
        x=int(random.uniform(0,self.width))
        y=int(random.uniform(0,self.height))
        return x,y

#Function to find distance between nodes to find  nearest node to current sampled node
    def nearestnode(self,n):
        dis=self.distance(0,n)
        a=0
        for i in range(0,n):
            if self.distance(i,n) < dis:
                dis=self.distance(i,n)
                a=i
        return a #returns the nearest node

#function to check whether node is located inside free space
    def freespace(self):
        n=self.nodecount()-1
        (x,y)=(self.x[n],self.y[n])
        obst=self.obstacles.copy()
        while len(obst)>0:
            rectangle=obst.pop(0)
            if rectangle.collidepoint(x,y):
                self.removenode(n)
                return False
        return True
#fUNCTION to check whether edges collide with obstacles. This is done using interpolation.
    def edgecollision(self,x1,x2,y1,y2):
        obst=self.obstacles.copy()
        while (len(obst) >0):
            rectangl=obst.pop(0)
            for i in range(0,101): #generate checkpoints on edges to detect collision with obstacles.
                q=i/100
                x=x1*q+x2*(1-q)
                y=y1*q+y2*(1-q)
                if rectangl.collidepoint(x,y):
                    return True
        return False
#Function used to connect two nodes together to form an edge
    def connect(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        if self.edgecollision(x1,x2,y1,y2):
            self.removenode(n2)
            return False
        else:
            self.addedge(n1,n2)
            return True

#Generating nodes between two existing nodes to enable smoother path formation
    def centre(self,a,b,max=10):
        d=self.distance(a,b)
        if d>max:
            (xa,ya)=(self.x[a],self.y[a])
            (xb,yb)=(self.x[b],self.y[b])
            (px,py)=(xb-xa,yb-ya)
            theta=math.atan2(py,px)
            (x,y)=(int(xa+max*math.cos(theta)),int(ya+max*math.sin(theta)))
            self.removenode(b)
            if abs(x-self.goal[0])<=max and abs(y-self.goal[1])<= max:
                self.addnode(b,self.goal[0],self.goal[1])
                self.goalstate=b
                self.goalflag=True
            else:
                self.addnode(b,x,y)

#Functions to optimize node formation towards the goal
    def towardsgoal(self,goal):
        n= self.nodecount()
        self.addnode(n,goal[0],goal[1])
        a =self.nearestnode(n)
        self.centre(a,n)
        self.connect(a,n)
        return self.x,self.y,self.parent

    def expandgoal(self):
        a =self.nodecount()
        x,y =self.randomsamples()
        self.addnode(a,x,y)
        if self.freespace():
            x1=self.nearestnode(a)
            self.centre(x1,a)
            self.connect(x1,a)
        return self.x,self.y,self.parent

#Function used to get final path from start to goal
    def finalpath(self):
        if self.goalflag:
            self.path=[]
            self.path.append(self.goalstate)
            a=self.parent[self.goalstate]
            while (a!=0):
                self.path.append(a)
                a=self.parent[a]
            self.path.append(0)
        return self.goalflag

#Function used to get coordinates of final path
    def getfinalpath(self):
        path=[]
        for node in self.path:
            x,y=(self.x[node],self.y[node])
            path.append((x,y))
        return path


