import pygame
import time
import random
import os
import tkinter as tk

pygame.init()

WIDTH, HEIGHT = 750, 750
GRID_SIZE = 20
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player move testing_grounds")

WHITE = (252,252,252)
BLACK = (0,0,0)

class node(object):
    def __init__(self, x, y, width):
        
        self.x = x
        self.y = y
        self.width = WIDTH//GRID_SIZE
        self.wall_hitboxes = dict()

    def create_walls(self):
        pass

    def draw(self):
        pygame.draw.rect(WINDOW, (252,252,252), (self.x, self.y, self.width, self.width))

    def get_wall_hitbox(self, direction):
        pass

    def get_wall_hitbox(self, direction):
        pass


class guy(object):
    def __init__(self, x, y, board_node_width):
        self.x = x
        self.y = y
        self.width = board_node_width//2
        self.hitbox = (self.x, self.y, self.width, self.width)

    def draw(self):
        pygame.draw.rect(WINDOW, (252, 0, 0), (self.x, self.y, self.width, self.width))

    def get_width(self):
        return self.width

    def collision(self, grid, direction):
        # Maybe take in a directional move parameter, that way
        # the method doesn't have to check every single direction
        # upon every move

        # Need some way to check if im running into a wall
            # Can be done by 
                # 1. Creating wall objects that have their own hitbox
                # 2. Having each node determine its own hitboxes (?)
                    # I like this one - have each node define a rectangle
                    # around its walls that is 1 pixel either way - 
                    # maintaining wall hitboxes

        # This needs to work by at each keypress calculate current node
        # occupied (Will just use top right of player box), check the 
        # coords of its walls, then check if there is overlap between
        # a wall and the player - if there is reject the move

        # First determine current node. This will be based off 
        # top left corner of player

        current_node = grid[self.y//GRID_SIZE][self.x//GRID_SIZE]
        # Create a wall_hitboxes 

        cur_wall_hitbox = current_node.get_wall_hitbox(direction)
        cur_wall_hitbox # Making literal test

        


        return False

def redraw_window(guy):

    WINDOW.fill(WHITE)

    guy.draw()
    pygame.display.update()

def create_grid():
    grid = []
    for row in range(GRID_SIZE):
        grid.append([])
        for column in range(GRID_SIZE):
            grid[row].append(node(column, row, WIDTH//GRID_SIZE))

    return grid

def draw(grid):
    for row in grid:
        for node in row:
            node.draw()

def main():
    run = True

    root = tk.Tk()
    DFS_button = tk.Button(root, text="DFS", padx=29, pady=1, anchor=tk.CENTER).pack()
    Djkstras_button = tk.Button(root, text="Djkstra's", padx=17, pady=1, anchor=tk.CENTER).pack()
    Astar_button = tk.Button(root, text="A*", padx=32.25, pady=1, anchor=tk.CENTER).pack()
    # This is also how many times a second we are checking for events (collisions, etc)
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    player_velocity = 5

    dude = guy(500, 500, WIDTH//30)

    clock = pygame.time.Clock()

    grid = create_grid()
    draw(grid)

    while run:
        clock.tick(FPS)
        redraw_window(dude)
        

        root.mainloop()
        # Every cycle through the loop we are calling on pygame to check if an event 
        # has occurred. We can determine what to do based off what type event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.QUIT is associated with the red X at the top right
                run = False
            """ 
            * This is one way to move things around in pygame, but we will use a diff method
            if event.type == pygame.KEYDOWN:
                pass """

        # This returns a dict of all of the keys and tells us whether they're pressed or not
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dude.y - player_velocity >= 0:
            dude.y -= player_velocity
            redraw_window(dude)
        if keys[pygame.K_s] and dude.y + player_velocity < HEIGHT-dude.get_width():
            dude.y += player_velocity
            redraw_window(dude)
        if keys[pygame.K_a]and dude.x - player_velocity >= 0:
            # left
            # Note that this happens 60x per second
            dude.x -= player_velocity
            redraw_window(dude)
        if keys[pygame.K_d] and dude.x + player_velocity < WIDTH-dude.get_width():
            dude.x += player_velocity
            redraw_window(dude)
        
main()