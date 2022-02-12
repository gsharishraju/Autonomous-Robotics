import pygame
from ar_rrt import Graph,Map
from ar_mov import movrect,Environment
import time
from random import randint
img = [r'E:\IUB\Subjects\Autonomous Robotics\Final Project\rectangle.png']
dimensions=(600,1200)
start=(50,50)
goal=(1000,500)
obsdim=70
obsnum=50

def main():
    i=0
    pygame.init()
    map=Map(start,goal,dimensions,obsdim,obsnum) #calling all functions declared in python files to draw map, obstacles
    graph=Graph(start,goal,dimensions,obsdim,obsnum)
    obstacles=graph.makeobs()
    map.drawmap(obstacles)
    t=time.time()
    while (not graph.finalpath()):
        i+=1
        rt=time.time()-t  #timeout to prevent tree from getting stuck in loop at a position with no outlet
        if rt > 15:
            print('Tree stuck')
            raise
        if i%10==0:
            X,Y,Parent=graph.towardsgoal(goal) #Function used to make the roots of tree move faster towards goal
            pygame.draw.circle(map.map,map.grey,(X[-1],Y[-1]),4,0)
            pygame.draw.line(map.map,map.Blue,(X[-1], Y[-1]),(X[Parent[-1]],Y[Parent[-1]]),map.edgethickness)
        else:
            X,Y,Parent=graph.expandgoal() # function used to make the roots of the tree branch out and expand towards goal
            pygame.draw.circle(map.map, map.grey,(X[-1],Y[-1]),4,0)
            pygame.draw.line(map.map,map.Blue,(X[-1], Y[-1]),(X[Parent[-1]],Y[Parent[-1]]),map.edgethickness)
        if i%5==0:
            pygame.display.update()
        i+=1
    time.sleep(3)
    finpath = graph.getfinalpath()
    map.drawPath(finpath)
    pygame.display.update()
    time.sleep(3)
    flag=True
    dt = 0
    tt=pygame.time.get_ticks()
    environment=Environment(dimensions,map.map)
    robot=movrect(start,img[0],finpath,width=10)

    while flag:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                flag=False
            robot.rectmove(robot,environment,dt,event)
        robot.rectmove(robot,environment,dt)
        pygame.display.update()
        dt=(pygame.time.get_ticks()-tt)/1000
        tt=pygame.time.get_ticks()

if __name__ == '__main__':
    main()

