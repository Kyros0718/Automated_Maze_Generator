import pygame
from random import choice


##### MAZE ATTRIBUTES
maze_size = [30,30]

maze_wall_color = 'slate blue'
background_color = 'black'
entrance_color = "white"
exit_color = entrance_color

maze_size = [maze_size[0]+4,maze_size[1]+4]
wall_thickness = int(10-(max(maze_size)-4)*(2/25))
if wall_thickness <= 0:
    wall_thickness = 1


##### Determine Window's Resolution and Tile Size, Calculate Column/Rows Based On Resolution
TILE = 200
while maze_size[0]*TILE > 1800 or maze_size[1]*TILE > 1000: #Scale the maze's cell size to fit within window frame
    TILE= TILE-1
    
maze_size = (maze_size[0]*TILE+3,maze_size[1]*TILE+3)
RES = WIDTH, HEIGHT = maze_size #Set game's resolution size to be the same size as the maze
cols, rows = WIDTH // TILE, HEIGHT // TILE


##### Initialize Pygame to use Pygame's Functions
pygame.init() 
sc = pygame.display.set_mode(RES) #Set display Windows Width/Height Parameter


##### Construct a Graph made of Individual Interactive Cells
class Cell:
    def __init__(self, x,y): #Determine Cell's Properties: [Coordinates, Walls, Visited, Entrance, Exit]
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.entrance = {'top': False, 'left': False}
        self.exit = {'right': False, 'bottom': False}


    def draw(self): #Determine Cell's Visuals [Width/Height, Border Color]
        x,y = self.x * TILE, self.y * TILE
        hole = TILE*2-wall_thickness
        wall_adj = wall_thickness//2
        
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x,y), (x + TILE, y), wall_thickness)
            if self.entrance['top']:
                pygame.draw.line(sc, pygame.Color(entrance_color), (x+wall_adj,y), (x-wall_adj + TILE, y), hole)
                 
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x + TILE, y), (x + TILE, y + TILE), wall_thickness)
            if self.exit['right']:
                pygame.draw.line(sc, pygame.Color(exit_color), (x + TILE, y+wall_adj), (x + TILE, y + TILE-wall_adj), hole)    
                
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x + TILE, y + TILE), (x, y + TILE), wall_thickness)
            if self.exit['bottom']:
                pygame.draw.line(sc, pygame.Color(exit_color), (x-wall_adj + TILE, y + TILE), (x+wall_adj, y + TILE), hole)   
                
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x, y + TILE), (x, y), wall_thickness)
            if self.entrance['left']:
                pygame.draw.line(sc, pygame.Color(entrance_color), (x, y + TILE-wall_adj), (x, y+wall_adj), hole)
                
                
    def check_cell(self, x, y): #Locate a Cell By its Position
        find_index = lambda x,y: x+y*cols
        if x < 0 or x > cols-1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x,y)]
    
    
    def check_neighbors(self): #Search For New Cell from current cell by Randomized Choice
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x+1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        list(map(lambda x: neighbors.append(x) if x and not x.visited else False, [top,right,bottom,left]))
            
        return choice(neighbors) if neighbors else False
        
        
def remove_walls(current, next): #Remove The Wall between the current and next cell
    def wall_setFalse(a,b):
        current.walls[a], next.walls[b] = False, False
    dx , dy = current.x - next.x, current.y - next.y
    dxd = {1: ['left','right'], -1: ['right','left']}
    dyd = {1: ['top','bottom'], -1: ['bottom','top']}
    
    wall_setFalse(*(dxd.get(dx) or dyd.get(dy)))


##### Generate the cells to form a graph
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)] #Create a List of Cells with (X,Y) Positions 

current_cell = grid_cells[0] #Start of the List is Cell(0,0)
stack = []


##### Initiate First Move to add to stack
current_cell.visited = True
next_cell = current_cell.check_neighbors() # Visit A New Neighboribng Cell
next_cell.visited = True
stack.append(current_cell)
remove_walls(current_cell, next_cell)
current_cell = next_cell #Make New Cell the current Cell


##### Create Maze with Algorithm
finish = False
while stack: #Generate Maze until stack is empty
    next_cell = current_cell.check_neighbors() # Visit A New Neighboribng Cell
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell #Make New Cell the current Cell

    elif stack:
        current_cell = stack.pop()
    
    if len(stack) == 0 and finish == False: #Create Start/Finish Entrance and Exit
        if choice([1,2]) == 1:
            en_cell = grid_cells[choice(range(cols))]
            ex_cell = grid_cells[choice(range(cols))+(rows-1)*(cols)]
            
            en_cell.walls["top"] = False
            ex_cell.walls["bottom"] = False
            
            en_cell.entrance["top"] = True
            ex_cell.exit["bottom"] = True

        else:
            en_cell = grid_cells[choice(range(rows))*(cols)]
            ex_cell = grid_cells[choice(range(rows))*(cols)+cols-1]
            
            en_cell.walls["left"] = False
            ex_cell.walls["right"] = False
            
            en_cell.entrance["left"] = True
            ex_cell.exit["right"] = True
            
            finish = True


##### Actualize the Game
while True:
    sc.fill(pygame.Color(background_color)) #Determine BackGround Color
    
    for event in pygame.event.get(): #Retrieve all event that have occurred since this the last time this function was called
        if event.type == pygame.QUIT: #End Loop when Press (X) Button
            exit()
    
    
    [cell.draw() for cell in grid_cells] #Draw The Cell Graph
    
    
    pygame.display.flip() #Update Contents of Entire Display




