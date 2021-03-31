#https://github.com/SamPusegaonkar/ENPM661/tree/main/Project3
#Output Videos can be found in the 'Output Videos' folder.

import pygame
import math
import heapq
import time
import functools

#Defining Graph Constants
HEIGHT = 300
WIDTH = 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255,0,255)

class Node:
    """
    Node class : This class is built to store the node information.
    A node is simply a location on a map. For each node, its neighbours, parents & distance to reach that node is stored.
    """
    def __init__(self, i ,j, endI, endJ, theta):
        """
        Description: Defining all properties for each node - Neighbours, Parents, Distance.
        """
        self.i = i
        self.j = j
        self.theta = theta
        self.costToCome = float('inf')
        self.costToGo = math.sqrt((i - endI)**2 + (j - endJ)**2)
        self.cost = None
        self.neighbours = {}
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost

class Graph:
    """
    Graph class : This class defines all methods to generate a graph and perform Djikstra's Algorithm.
    """
    def __init__(self, start, end):
        self.visited = {}
        self.endI = end.i
        self.endJ = end.j

    def getNeighbours(self, currentNode):
        """
        Description: Returns neighbours for the currentNode.
        """
        i, j, theta = currentNode.i, currentNode.j, currentNode.theta
        neighbours ={}
        RADIUS = 10


        for deltaTheta in range(-60, 60, 30):
            print(deltaTheta)
            x, y, newTheta = self.getNewCoordiantes(i, j , theta, deltaTheta)
            if (not self.isOutsideArena(x,y)) and (not self.isAnObstacle(x,y)):
                newNode = Node(x, y, self.endI, self.endJ, newTheta)
                neighbours[newNode] = 1
        return neighbours

    def getNewCoordiantes(self, i, j, theta, deltaTheta):
        MAGNITUDE = 10
        newTheta = theta + deltaTheta


        if newTheta > 0:
            newTheta = newTheta % 360
        elif newTheta < 0:
            newTheta = (newTheta+360) % 360

        newI = i + MAGNITUDE * math.cos( (math.pi/180) * newTheta)
        newJ = j + MAGNITUDE * math.sin( (math.pi/180) * newTheta)

        print(newI, newJ, newTheta)
        
        newI = self.getRoundedNumber(newI)
        newJ = self.getRoundedNumber(newJ)
        print(newI, newJ, newTheta)

        print("--------------------------------------")

        return newI, newJ, newTheta

    def getRoundedNumber(self, i):

        decimal = i - int(i)
        if decimal > 0.5:
            return math.ceil(i)
        elif decimal < 0.5:
            return math.floor(i)

    def generateGraph(self,):
        """
        Description: Checks if a point is in the Ellipse. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        #Make background White
        gridDisplay.fill(WHITE)

        #Circle
        pygame.draw.circle(gridDisplay, MAGENTA, [90,HEIGHT - 70], 35)
        
        #Ellipse
        pygame.draw.ellipse(gridDisplay, MAGENTA, [186, HEIGHT - 176, 120, 60], 0)

        #Roatated Rect
        pygame.draw.polygon(gridDisplay, MAGENTA, [(36, HEIGHT - 124), (160, HEIGHT -210), (170, HEIGHT -194),(48,HEIGHT -108)])

        #Broken Rect
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 280), (230, HEIGHT -280), (230, HEIGHT -270),(200,HEIGHT -270)])
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 270), (210, HEIGHT -270), (210, HEIGHT -240),(200,HEIGHT -240)])
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 240), (230, HEIGHT -240), (230, HEIGHT -230),(200,HEIGHT -230)])

    def performDijkstra(self, start, end):
        """
        Description: Defining initial constants - Visited array, Rows, Cols, Target String.
        Input: Starting and ending node for the robot to browse.
        Output: Returns True or False to define if an optimal path can be found or not.
        """
        
        #Checking is start and end  are in obstancle.
        if self.isAnObstacle(start.i,start.j) and self.isAnObstacle(end.i, end.j):
            print("Starting and ending point are inside the obstacle!")
            return
        if self.isAnObstacle(start.i,start.j):
            print("Starting point is inside the obstacle!")
            return 
        if self.isAnObstacle(end.i, end.j):
            print("Ending point is inside the obstacle!")
            return 
        
        if self.isOutsideArena(start.i,start.j):
            print("Starting point is outside the arena!")
            print("Starting point should be between (0,0) and (400,300)")
            return 
        
        if self.isOutsideArena(end.i,end.j):
            print("Ending point is outside the arena!")
            print("Ending point should be between (0,0) and (400,300)")
            return 

        print("Finding path...")
        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            print("--------------------------------------------")
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            if self.isInTargetArea(currentNode.i, currentNode.j):
                self.backTrack(currentNode)
                print("Found a path!")
                return True
            
            if tuple([currentNode.i, currentNode.j]) in self.visited:
                continue
            self.visited[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.costToCome
            neighbours = self.getNeighbours(currentNode)
            currentNode.neighbours = neighbours
            for neighbourNode, newDistance in neighbours.items():

                neighbourNode.costToCome = currentDistance + newDistance
                neighbourNode.cost = neighbourNode.costToCome + neighbourNode.costToGo
                neighbourNode.parent = currentNode
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))
        print("Cannot find a path :(")
        return False

    def visualizeDijkstra(self, start, end):
        """
        Description: Visualization of the algorithm.
        Input: Starting and ending node for the robot to browse.
        Output: A animation of nodes which are browsed and the path generated.
        """

        self.visited = {}
        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):

            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]

            if self.isInTargetArea(currentNode.i, currentNode.j):
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.costToCome)
                return
            
            if tuple([currentNode.i, currentNode.j]) in self.visited:
                continue
            self.visited[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.costToCome
            for neighbourNode, newDistance in currentNode.neighbours.items():
                i = neighbourNode.i
                j = neighbourNode.j
                if (start.i == i and start.j == j) or (end.i == i and end.j == j):
                    pygame.draw.circle(gridDisplay, BLACK, [i,HEIGHT - j], 10)
                    pygame.display.update()  
                # elif (i-20 < start.i < i+20 and j-20 < start.j < j+20) or (i-20 < end.i < i+20 and j-20 < end.j < j+20):       
                #     pygame.display.update() 
                # elif self.isInStartingSquare(start, i, j) and not self.isinStartingCircle(start, i,j):
                #     pygame.draw.rect(gridDisplay, CYAN,[i, HEIGHT - j, 2,2])
                #     pygame.display.update()   
                else:    
                    # pygame.draw.circle(gridDisplay, CYAN, [i,HEIGHT - j], 10)
                    pygame.draw.line(gridDisplay, GREEN, [currentNode.i,HEIGHT - currentNode.j],  [i,HEIGHT - j],  1)
                    pygame.display.update()
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))

        return 

    def isInTargetArea(self, i, j):
        """
        Description: Checks if the currentnode is in target area to terminal the program
        Input: Current Node co-ordinates
        Output: Boolean
        """
        if (i -  self.endI) **2 + (j- self.endJ)**2 - 100 <= 0:
            return True
        else:
            return False



    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """
        while child != None:
            path.append((child.i, child.j))
            #grid[child.i][child.j] = 1
            print(child.i, child.j, "PAth")
            child = child.parent
        return True

    def isinStartingCircle(self, start, i,j):
        """
        Description: Checks if a point is in the starting circle from where the robot will start,
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (i - start.i) **2 + (j-start.j)**2 - 100 <= 0:
            return True
        else:
            return False

    def isInStartingSquare(self, start, i,j):
        """
        Description: Checks if a point is in the starting square from where the robot will start.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (start.i-10 <= i <= start.i + 10) and (start.j -10 <= j <= start.j + 10):
            return True
        else:
            return False

    def isInCircle(self, x,y):
        """
        Description: Checks if a point is in the circle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (x - 90) **2 + (y-70)**2 - 2500 > 0:
            return False
        else:
            return True

    def isInRectangle(self, x,y):
        """
        Description: Checks if a point is in the rotated rectangle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        clearance = 15
        if (y + 1.42*x - 176.55 + clearance + 10) > 0  and (y - 0.7*x - 74.39 + clearance )  > 0 and (y - 0.7*x - 98.81 - clearance) < 0 and (y + 1.42*x - 438.06 - clearance - 10) < 0:
            return True
        else:
            return False

    def isInBrokenRectangle(self, x,y):
        """
        Description: Checks if a point is in the top rectangle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        clearance = 15
        if (x >= (200 - clearance) and x <= (210 + clearance) and y <= (280+ clearance) and y >=(230 - clearance)) or (x>= (210 - clearance) and x <= (230+ clearance) and y >=(270- clearance) and y <= (280+ clearance)) or (y >= (230- clearance) and y <= (240+ clearance) and x >= (210- clearance) and x <= (230+ clearance)):
            return True
        else:
            return False

    def isInEllipse(self, x,y):
        """
        Description: Checks if a point is in the Ellipse. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        a = 75
        b = 45
        h = 246
        k = 145
        if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) < 1:
            return True
        else:
            return False

    def isAnObstacle(self,x,y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return self.isInEllipse(x,y) or self.isInBrokenRectangle(x,y) or self.isInCircle(x,y) or self.isInRectangle(x,y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the areana or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        return True if x < 0 or y < 0 or x > 400 or y > 300 else False

x1 = int(input("Enter the x coordiante of the starting point: "))
y1 = int(input("Enter the y coordiante of the starting point: "))

x2 = int(input("Enter the x coordiante of the ending point: "))
y2 = int(input("Enter the y coordiante of the ending point: "))

#############################################           
#Algorithm Driver  
end = Node(x2, y2, x2, y2, 0)
start = Node(x1, y1, x2, y2, 0)
start.costToCome = 0
start.theta = 0
robot = Graph(start, end)
path = []

#Check if path can be found
if robot.performDijkstra(start, end):
    pass
    pygame.init() #Setup Pygame
    gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra's Algorithm - Rigid Robot")
    exiting = False
    clock = pygame.time.Clock()
    grid = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]
    canvas = Graph(start, end) #Create Canvas
    canvas.generateGraph()
    #robot.visualizeDijkstra(start, end)
    path.reverse()
else:
    #No Path Found
    exiting = True

#############################################
#Running the simulation in loop

while not exiting:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            exiting = True  

    for row in range(WIDTH):
        for column in range(HEIGHT):
            if grid[row][column] == 1:
                pygame.draw.rect(gridDisplay, BLACK,[row, HEIGHT - column, 2,2])

    #Visualizing the final path
    # for index in range(len(path)):
    #     x, y = path[index]
    #     pygame.draw.circle(gridDisplay, BLACK, [x,HEIGHT - y], 10)
    #     pygame.display.update()  
    #     if index != 0 and index != len(path)-1:
    #         pygame.draw.circle(gridDisplay, CYAN, [prevX,HEIGHT - prevY], 10)
    #     time.sleep(.1)
    #     prevX = x
    #     prevY = y
        
 

    clock.tick(2000)
    pygame.display.flip()
    exiting = True
pygame.quit()
#############################################
