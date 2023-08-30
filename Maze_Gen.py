import pygame, time
from random import choice


##### Determine Window Resolution and Tile Size, Calculate Column/Rows Based On Resolution
maze_size = [30,30]
TILE = 200
while maze_size[0]*TILE > 1800 or maze_size[1]*TILE > 1000:
    TILE= TILE-1
maze_size = (maze_size[0]*TILE+3,maze_size[1]*TILE+3)
RES = WIDTH, HEIGHT = maze_size
cols, rows = WIDTH // TILE, HEIGHT // TILE


##### Initialize Pygame to use Pygame's Functions
pygame.init() 
sc = pygame.display.set_mode(RES) #Set display Windows Width/Height Parameter


##### Create An Graph made of Individual Interactive Cells
class Cell:
    def __init__(self, x,y): #Determine Cell's Properties: [Coordinate, Walls, Visited]
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    def draw(self): #Determine Cell's Visuals [Width/Height, Border Color]
        x,y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('slate blue'), (x,y), (x + TILE, y), 5)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('slate blue'), (x + TILE, y), (x + TILE, y + TILE), 5)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('slate blue'), (x + TILE, y + TILE), (x, y + TILE), 5)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('slate blue'), (x, y + TILE), (x, y), 5)
    
    def check_cell(self, x, y): #Locate Specific Cell By Position
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
        
def remove_walls(current, next): #Remove The wall between the current and next cell
    def wall_setFalse(a,b):
        current.walls[a], next.walls[b] = False, False
    dx , dy = current.x - next.x, current.y - next.y
    if dx == 1:
        wall_setFalse('left','right')
    elif dx == -1:
        wall_setFalse('right','left')
    if dy == 1:
        wall_setFalse('top','bottom')
    elif dy == -1:
        wall_setFalse('bottom','top')
        
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)] #Create a List of Cells with (X,Y) Positions 
current_cell = grid_cells[0] #Start of the List is Cell(0,0)
stack = []


finish = False
##### Actualize the Game
t0 = time.time() ##TIMER START
while True:
    sc.fill(pygame.Color('black')) #Determine BackGround Color
    
    for event in pygame.event.get(): #Retrieve all event that have occurred since this the last time this function was called
        if event.type == pygame.QUIT: #End Loop when Press (X) Button
            exit()
    
    
    [cell.draw() for cell in grid_cells] #Draw The Cell Graph
    current_cell.visited = True

    
    
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
            
            grid_cells[choice(range(cols))].walls['top'] = False
            grid_cells[choice(range(cols))+(rows-1)*(cols)].walls['bottom'] = False
            finish = True
            t1 = time.time() ##TIMER END
            total = t1-t0
            print(total)
        else:
            
            grid_cells[choice(range(rows))*(cols)].walls['left'] = False
            grid_cells[choice(range(rows))*(cols)+cols-1].walls['right'] = False
            finish = True
            t1 = time.time() ##TIMER END
            total = t1-t0
            print(total)
            
    elif len(stack) == 0: # Make Orange Cell Disappear
        grid_cells[0].visited = True
        grid_cells[0].draw()
    
    pygame.display.flip() #Update Contents of Entire Display