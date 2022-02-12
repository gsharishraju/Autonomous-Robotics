import pygame
import math
# Class contains functions and properties for the rectangle to move over path
class movrect:
    def __init__(self,startposition,img,path,width):
        self.path=path
        self.mid=len(path)-1
        self.x,self.y=startposition
        self.theta=0
        self.a=20
        self.w=width
        self.u=30
        self.W=0
        self.img=pygame.image.load(img)
        self.pic=self.img
        self.rect=self.pic.get_rect(center=(self.x, self.y))

# Function to calculate x,y,theta values for robot movement and to facilitate robot movement
    def moves(self,dt,event=None):
        self.x+=(self.u*math.cos(self.theta)-self.a*math.sin(self.theta)*self.W)*dt #Referenced from http://www.spencer.eu/papers/palmieriICRA16.pdf
        self.y+=(self.u*math.sin(self.theta)+self.a*math.cos(self.theta)*self.W)*dt
        self.theta+=self.W*dt
        print(f"x {self.x}, y {self.y},theta {self.theta}")
        self.pic=pygame.transform.rotozoom(self.img,math.degrees(-self.theta),1) #https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotozoom
        self.rect=self.pic.get_rect(center=(self.x,self.y))
        a =self.path[self.mid]
        x1=a[0]-self.x
        y1=a[1]-self.y
        self.u=x1*math.cos(self.theta)+y1*math.sin(self.theta) # linear velocity
        self.W=(-1/self.a)*math.sin(self.theta)*x1+(1/self.a)*math.cos(self.theta)*y1 # angular velocity
        if self.dist((self.x,self.y),self.path[self.mid]) <= 35:
            self.mid-=1
        if self.mid <= 0:
            self.mid=0

    def dist(self,p1,p2):
        (x1,y1)=p1
        (x2,y2)=p2
        x1=float(x1)
        x2=float(x2)
        y1=float(y1)
        y2=float(y2)
        px=(x1-x2)**(2)
        py=(y1-y2)**(2)
        distance=(px+py)**(0.5)
        return distance

    def draw(self,map):
        map.blit(self.pic,self.rect)

    def rectmove(self,movrect,environment,dt,event=None):
        movrect.moves(dt,event=event)
        movrect.draw(environment.map)

class Environment:
    def __init__(self,dimensions,map):
        self.height,self.width=dimensions
        self.map=map



