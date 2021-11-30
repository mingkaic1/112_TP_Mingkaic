# --------------------
# GRAPH.PY
# - Graph class
#   - Data structure for representing map as a graph (implemented as a
#     dictionary)
#   - Encapsulates pathfinding algorithm(s)
# --------------------

class Graph():
    def __init__(self, maze):
        self.graphDict = {}
        self.makeGraphDict(maze)

    def makeGraphDict(self, maze):
        for row in range(maze.numRows):
            for col in range(maze.numCols):
                cell = maze.getCell(row, col)
                if (cell.walls[0] == False):
                    self.graphDict[(row, col)] = self.graphDict.get((row, col), []) + [(row - 1, col)]
                if (cell.walls[1] == False):
                    self.graphDict[(row, col)] = self.graphDict.get((row, col), []) + [(row, col - 1)]
                if (cell.walls[2] == False):
                    self.graphDict[(row, col)] = self.graphDict.get((row, col), []) + [(row + 1, col)]
                if (cell.walls[3] == False):
                    self.graphDict[(row, col)] = self.graphDict.get((row, col), []) + [(row, col + 1)]

    def findPath(self, startNode, endNode, algorithmNum = 0):
        if algorithmNum == 0:
            return self.findPathDijkstra(startNode, endNode)

    def findPathDijkstra(self, startNode, endNode):
        priorityQueue = PriorityQueue()
        currentNode = startNode
        currentCost = 0
        visitedNodes = set()
        reachedVia = {}
        # Keep looping until currentNode reached endNode
        while (currentNode != endNode):
            # Loop through each neighbor node
            for neighborNode in self.graphDict[currentNode]:
                # If neighborNode has already been visited, skip
                if neighborNode in visitedNodes:
                    continue
                totalCost = currentCost + 1
                # If neighborNode has a previously calculated cost in priorityQueue
                prevCost = priorityQueue.getCost(neighborNode)
                if prevCost != None:
                    # If new cost is better (lower) than prevCost
                    if totalCost < prevCost:
                        priorityQueue.override(currentNode, totalCost)
                        reachedVia[neighborNode] = currentNode
                    # (If new cost isn't as good as prevCost, don't do anything)
                # If neighborNode has no previously calculated cost in priorityQueue
                else:
                    priorityQueue.add(neighborNode, totalCost)
                    reachedVia[neighborNode] = currentNode
            visitedNodes.add(currentNode)
            # Move onto the next lowest-cost node
            currentNode, currentCost = priorityQueue.popTop()
        # Build path by moving currentNode from endNode back to startNode
        path = []
        path.append(currentNode) # Right now, currentNode = endNode
        while currentNode != startNode:
            path.insert(0, reachedVia[currentNode])
            currentNode = path[0]
        return path

# PriorityQueue data structure
#   - Stores list of 2-tuples, where each tuple is (item, cost)
class PriorityQueue():
    def __init__(self):
        self.data = []

    def __repr__(self):
        return self.data

    # Add item to the appropriate position on the list
    def add(self, item, cost):
        if self.data == []:
            self.data.append((item, cost))
            return
        indexToInsert = 0
        while self.data[indexToInsert][1] > cost:
            indexToInsert += 1
        self.data.insert(indexToInsert, (item, cost))

    # Return the top priority item and cost (lowest cost)
    def getTop(self):
        return self.data[-1]

    # Pop the top priority item and cost (lowest cost)
    def popTop(self):
        return self.data.pop()

    # Get the cost of the given item. If item does not exist, return None
    def getCost(self, item):
        for i in range(len(self.data)):
            if self.data[i][0] == item:
                return self.data[i][1]
        return None