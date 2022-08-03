from queue import PriorityQueue

CLEAR = " "
CLOSED = "X"
OPEN = "O"
BARRIER = "#"
START = "S"
END = "E"
PATH = "="

class Node:
    def __init__(self, row, col, total_rows):
        self.row = row
        self.col = col
        self.state = CLEAR
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):#Esta funcion nos devuelve la posicion de nuestro nodo
        return self.row, self.col

    def isClosed(self):#Esta funcion nos dice se nuestro nodo está marcado como cerrado
        return self.state == CLOSED
    
    def isOpen(self):#Esta funcion nos dice se nuestro nodo está marcado como abierto
        return self.state == OPEN

    def isBarrier(self):#Esta funcion nos dice se nuestro nodo está marcado como una barrera
        return self.state == BARRIER

    def isStart(self):#Esta funcion nos dice se nuestro nodo está marcado como el inicio
        return self.state == START

    def isEnd(self):#Esta funcion nos dice se nuestro nodo está marcado como el final
        return self.state == END

    def reset(self):#Esta función lo que hace es que cambia de vuelta el color del nodo a blanco
        self.state = CLEAR
        
    def makeClosed(self):#Esta funcion pone el nodo como cerrado
        self.state = CLOSED
    
    def makeOpen(self):#Esta funcion pone el nodo como abierto
        self.state = OPEN

    def makeBarrier(self):#Esta funcion pone el nodo como una barrera
        self.state = BARRIER

    def makeStart(self):#Esta funcion pone el nodo como el inicio
        self.state = START

    def makeEnd(self):#Esta funcion pone el nodo como el final
        self.state = END
    
    def makePath(self):#Esta funcion pone el nodo como camino
        self.state = PATH

    def updateNeighbors(self, grid): #Esta funcion checa todos los vecinos de nuestro nodo y los añade a una lista, a menos que sean una barrera
        self.neighbors=[]
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier(): #Abajo
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #Arriba
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier(): #Derecha
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): #Izquierda
            self.neighbors.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other): #Esta funcion sirve para qeu cada que comparen este nodo con otro con un mayor que, devuelva falso
        return False

        


def algorithm(grid, start, end):
    counter=0
    openSet=PriorityQueue()
    openSet.put((0,counter,start))
    cameFrom = {}
    gScore={node:float("inf") for row in grid for node in row}
    gScore[start] = 0
    fScore={node:float("inf") for row in grid for node in row}
    fScore[start] = h(start.get_position(), end.get_position())

    openSetFind= {start}

    while not openSet.empty():
        currentNode = openSet.get()[2]
        openSetFind.remove(currentNode)

        if currentNode == end:
            reconstruct(cameFrom, end)
            end.makeEnd()
            start.makeStart()
            return True
        for neighbor in currentNode.neighbors:
            tempG = gScore[currentNode] + 1
            if tempG < gScore[neighbor]:
                cameFrom[neighbor] = currentNode
                gScore[neighbor] = tempG
                fScore[neighbor] = tempG + h(neighbor.get_position(), end.get_position())
                if neighbor not in openSetFind:
                    counter += 1
                    openSet.put((fScore[neighbor], counter, neighbor))
                    openSetFind.add(neighbor)
                    neighbor.makeOpen()

        if currentNode != start:
            currentNode.makeClosed()
    return False

def h(p1, p2):#Tenemos 2 nodos y esta funcion se encarga de intentar calcular la distancia en L entre ellos
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) #Lo que hace esto es que no devuelve la suma de las restas absolutas, es decir que si la resta da un negativo, se vuelve positivo

def reconstruct(cameFrom, currentNode):
    while currentNode in cameFrom:
        currentNode = cameFrom[currentNode]
        currentNode.makePath()
        
def makeGrid(rows): #Esta funcion representa una taba 2d de nuestros nodos, para poder acceder a ellos
    grid = [] #creamos una lista vacía
    for i in range(rows):
        grid.append([]) #Por cada fila que queramos hacemos una lista vacia dentro de nuestra lista
        for n in range(rows):
            node = Node(i, n, rows)
            grid[i].append(node)#En la lista creada dentro de la lista, por cada columna(que siendo un cuadrado es lo mismo), ponemos un nuevo nodo
    return grid

def printGrid(grid, rows):
    graphGrid=[]

    for i in range(rows):
        graphGrid.append([]) 
        for n in range(rows):
            nodeValue= grid[i][n].state
            graphGrid[i].append(nodeValue)
    for row in range(len(graphGrid)):
        print(graphGrid[row])

def findPath(rows, selectedRowStart, selectedColumnStart, selectedRowEnd, selectedColumnEnd, grid = None):
    if grid == None:
        grid = makeGrid(rows)
    start = None
    end = None
    loop = True
    while loop:
        if (selectedRowStart != selectedRowEnd) or (selectedColumnEnd != selectedColumnStart):
            usedCoordinates = {(selectedRowStart, selectedColumnStart), (selectedRowEnd, selectedColumnEnd)}
            print(usedCoordinates)
            break
        else:
            print("The coordinates must not be the same")
            continue

    usedCoordinates = {(selectedRowStart, selectedRowEnd), ()}
        
    for row in grid:
        for node in row:
            node.updateNeighbors(grid)

    start = grid[selectedRowStart][selectedColumnStart]
    end = grid[selectedRowEnd][selectedColumnEnd]
    algorithm(grid, start, end)
    printGrid(grid, rows) 
