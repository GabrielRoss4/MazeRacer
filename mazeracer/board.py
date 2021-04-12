import pygame
from queue import PriorityQueue
import pathingalgorithms

pygame.init()

BOARD_WIDTH = 800
GRID_SIZE = 20

WINDOW = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
pygame.display.set_caption("Maze Racer")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

'''FIGURE OUT A WAY TO REMOVE WALLS. MUST BE ABLE TO CHECK IF THE NODE ON THE OTHER SIDE OF THE WALL IS VISITED.
    *IDEAS:
        * DICT WITH WALL DIRECTIONS AS KEYS AND BOOL IF THEYRE THERE AS VALUE
        * NODE MAINTAINS LIST OF WALL OBJECTS THAT CAN BE REMOVED
    * NEED WAY FOR NODE TO TELL WHICH OF ITS WALLS ARE UP
    *VALID DIRECTIONS WILL RETURN THE ADJACENT NODES'''

class Node(object):
    def __init__(self, x_grid, y_grid, width, total_rows):
        
        self.x = x_grid
        self.y = y_grid
        self.x_pixel = self.x*(BOARD_WIDTH//GRID_SIZE)
        self.y_pixel = self.y*(BOARD_WIDTH//GRID_SIZE)
        self.width = width
        self.total_rows = total_rows
        self.color = BLACK

        self.has_walls = {
            "left":False,
            "right":False,
            "up":False,
            "down":False
        }
        self.initialize_walls()


        self.valid_neigbors = []
        self.valid_directions = []

    def initialize_walls(self):
        if self.x > 0:
            self.has_walls["left"] = True
        if self.x < GRID_SIZE-1:
            self.has_walls["right"] = True
        if self.y > 0:
            self.has_walls["up"] = True
        if self.y < GRID_SIZE-1:
            self.has_walls["down"] = True

    def get_coords(self):
        return (self.x, self.y)


    def get_unwalled_neighbors(self, grid):
        # This function operates off the assumption that I've properly 
        # removed the wall from the neighbor as well

        '''
        THIS WILL HAVE TO BE REPEATED FOR EVERY NODE MEANING WE WILL HAVE TO DO 
        TWO WALL REMOVALS ANY TIME WE WANT TO REMOVE A WALL. IS THERE ANOTHER
        WAY TO DO THIS? 
            * MAYBE SEPARATE THE WALLS AND NODES SUCH THAT THE WALLS
              ARE THEIR OWN OBJECTS AND ARE DRAWN SEPARATELY. 
                * THIS COULD BE ACCOMPLISHED WITH A DICT THAT MAPS EACH NODE
                  TWO FOUR WALL OBJECTS? I'm kind of liking this idea
        '''
        unwalled_neighbors = []

        if not self.has_walls["left"] and self.x > 0:
            unwalled_neighbors.append(grid[self.y][self.x-1])
        if not self.has_walls["right"] and self.x < GRID_SIZE-1:
            unwalled_neighbors.append(grid[self.y][self.x+1])
        if not self.has_walls["up"] and self.y > 0:
            unwalled_neighbors.append(grid[self.y-1][self.x])
        if not self.has_walls["down"] and self.y < GRID_SIZE-1:
            unwalled_neighbors.append(grid[self.y+1][self.x])

        return unwalled_neighbors

    def get_walled_neighbors(self, grid):
        '''
        This does the opposite of self.get_unwalled_neighbors and only
        returns the neighbors in directions with walls. This is for the
        maze carving function
        '''
        walled_neighbors = []

        if self.has_walls["left"]:
            walled_neighbors.append(grid[self.y][self.x-1])
        if self.has_walls["right"]:
            walled_neighbors.append(grid[self.y][self.x+1])
        if self.has_walls["up"]:
            walled_neighbors.append(grid[self.y-1][self.x])
        if self.has_walls["down"]:
            walled_neighbors.append(grid[self.y+1][self.x])

        return walled_neighbors

    def draw_valid_walls(self):
        if self.has_walls["left"]:
            self.draw_left_wall()
        if self.has_walls["right"]:
            self.draw_right_wall()
        if self.has_walls["up"]:
            self.draw_up_wall()
        if self.has_walls["down"]:
            self.draw_down_wall()

    def remove_wall(self, grid, other):
        # This method will need to remove the walls between these two nodes. 
        # This will entail determining the node's relative positions to one
        # another and removing the walls from both nodes that they share.
        # This may actually be easier with the hash map implementation of 
        # the wall tracking.

        # Naive implementation of the remove walls method. Compares the argument 
        # node to the adjacent nodes in the grid and when it finds the match
        # removes the shared walls from the two nodes
        if type(other) == Node: 
            if self.x > 0 and grid[self.y][self.x-1] == other: #Left
                self.has_walls["left"] = False
                other.has_walls["right"] = False
            elif self.x < GRID_SIZE-1 and grid[self.y][self.x+1] == other: #Right
                self.has_walls["right"] = False
                other.has_walls["left"] = False
            elif self.y > 0 and grid[self.y-1][self.x] == other: #Up
                self.has_walls["up"] = False
                other.has_walls["down"] = False
            elif self.y < GRID_SIZE-1 and grid[self.y+1][self.x] == other: #Down
                self.has_walls["down"] = False
                other.has_walls["up"] = False

    def draw_left_wall(self):
        pygame.draw.line(WINDOW, WHITE, (self.x_pixel, self.y_pixel), (self.x_pixel, self.y_pixel+self.width))
    def draw_right_wall(self):
        pygame.draw.line(WINDOW, WHITE, (self.x_pixel+self.width, self.y_pixel), (self.x_pixel+self.width, self.y_pixel+self.width))
    def draw_up_wall(self):
        pygame.draw.line(WINDOW, WHITE, (self.x_pixel, self.y_pixel), (self.x_pixel+self.width, self.y_pixel))
    def draw_down_wall(self):
        pygame.draw.line(WINDOW, WHITE, (self.x_pixel, self.y_pixel+self.width), (self.x_pixel+self.width, self.y_pixel+self.width))

    def set_end(self):
        self.color = GREEN
    def set_start(self):
        self.color = BLUE
    def set_path(self):
        self.color = GREY
    def set_open(self):
        self.color = GREEN
    def set_closed(self):
        self.color = RED
    def set_visited(self):
        self.color = GREEN
    def set_dequeued(self):
        self.color = BLUE


    def draw(self, surface):
        # First draw the node itself, then draw all the valid walls.
        pygame.draw.rect(WINDOW, self.color, (self.x_pixel, self.y_pixel, self.width, self.width))
        self.draw_valid_walls()



def create_initial_grid():
    grid = []
    for row in range(GRID_SIZE):
        grid.append([])
        for column in range(GRID_SIZE):
            new_node = Node(column, row, BOARD_WIDTH//GRID_SIZE, GRID_SIZE)
            grid[row].append(new_node)

    grid[0][0].set_start()
    grid[GRID_SIZE-1][GRID_SIZE-1].set_end()
    return grid

""" 
Just a test method to ensure grid was properly drawing. Will be using draw as a more general method.

def draw_grid(grid, surface):
    for row in grid:
        for node in row:
            node.draw(surface)
    pygame.display.update """

def draw(grid, surface, grid_rows, width_surface):
    '''
    Redraws the board whenever its called using the contents of the grid

    * surface: <pygame.surface> Surface on which maze is redrawn
    * grid: <list[list]> Grid of nodes defining the board
    * grid_rows: <int> Number of rows & columns in the grid
    * width_surface: <int> Width and height of the surface in pixels
    '''

    for row in grid:
        for node in row:
            # Make each node draw itself
            node.draw(surface)

    # Update the display with the newly drawn nodes.
    pygame.display.update()



def main():
    run = True


    grid = create_initial_grid()
    draw(grid, WINDOW, GRID_SIZE, BOARD_WIDTH)
    lambda_draw = lambda: draw(grid, WINDOW, GRID_SIZE, BOARD_WIDTH)
    maze = pathingalgorithms.carve_maze_backtracking(grid, lambda_draw)

    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pathingalgorithms.a_star(maze, lambda_draw, maze[0][0], maze[GRID_SIZE-1][GRID_SIZE-1])

    pygame.quit()

    

main()