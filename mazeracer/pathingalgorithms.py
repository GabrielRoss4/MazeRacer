from queue import PriorityQueue, LifoQueue
import pygame
from random import shuffle
from time import sleep


# All pathing algorithms will take in a lambda draw function

def reconstruct_path(draw, path_map: dict, start_node, end_node):
    cur_node = path_map[end_node]
    while cur_node != start_node:
        cur_node.set_path()
        cur_node = path_map[cur_node]
        draw()
        sleep(0.01)

def a_star(grid, draw, start_node, end_node):
    def heuristic(p1, p2):
        '''
        Calculates the heuristic for the a_star function
        * p1, p2: <tuple> x, y coordinates of two nodes
        '''
        x1, y1 = p1
        x2, y2 = p2
        return abs(y2-y1) + abs(x2-x1)

    '''
    Uses the A* algorithm to find the shortest path from start to end
    * draw: <func> Lambda function that updates the UI as the algorithm runs
    * grid: <list[list]> List of lists which are the rows and columns of the board
    * start_node: <Node> start node 
    * end_node: <Node> end node
    '''

    count = 0
    open_set = PriorityQueue()

    # This will allow us to check which nodes are in the open_set at the moment
    # as a prio queue has no method allowing us to check this
    open_set_hash = set()

    # The open set will be a prio queue of tuples, each of which contains
    # the node's F score, count, and the node itself
        # * F score is the sum of the H score (the estimated distance from the end
        #   via the heuristic) and the G score (distance from the start node)
        # * The count is just a measure of when the node was added to the queue
        #   and will be used to break tiebreakers when two nodes have the same
        #   F score

    # Initialize the f score and count of the start node to be 0. Add it to the
    # open set so it is the first node we examine when we start iterating through
    # the grid.
    open_set.put((0, count, start_node))
    open_set_hash.add(start_node)

    # The path map is a hash map containing the predecessor node of each node.
    # This will allow us to trace the path back from the end node.
    path_map = dict()

    # g_score_map will be a hash map of the G score of every single node.
    # This will be initialized to infinity.
    g_score_map = {node: float("inf") for row in grid for node in row}
    g_score_map[start_node] = 0

    f_score_map = {node: float("inf") for row in grid for node in row}
    f_score_map[start_node] = heuristic(start_node.get_coords(), end_node.get_coords())

    while open_set.qsize() != 0:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur_node = open_set.get()[2]
        open_set_hash.remove(cur_node)

        if cur_node == end_node:
            reconstruct_path(draw, path_map, start_node, end_node)
            return 0

        for neighbor in cur_node.get_unwalled_neighbors(grid):
            cur_g_score = g_score_map[cur_node] + 1

            if cur_g_score < g_score_map[neighbor]:
                g_score_map[neighbor] = cur_g_score
                f_score_map[neighbor] = cur_g_score + heuristic(neighbor.get_coords(), end_node.get_coords())
                path_map[neighbor] = cur_node

                if neighbor not in open_set_hash:
                    # Increment count every single time a node is added to the open set
                    # allowng us to determine the order in which nodes were added
                    count += 1
                    open_set.put((f_score_map[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    # This is just to let the neighbor node know that it has been added
                    # to the open set and to adjuset its color as such
                    neighbor.set_open()

        # If the node is not the start node we let the node know that it has been removed from
        # the open set and is now in the closed set. The purpose of this is so that the node
        # adjusts its color properly in response to being removed from the open set. We don't
        # do this to the start node as we don't want to overwrite its color
        if cur_node != start_node:
            cur_node.set_closed()

        # Redraw the grid every time we loop through 
        draw()
        sleep(0.05)

    return 0

'''
* CONSIDER INSTEAD OF CALLING THE RECONSTRUCT PATH METHOD IN EACH ALGO METHOD HAVING EACH ALGO RETURN THE 
  PATH AND THEN JUST CALL THE RECONSTRUCT PATH METHOD IN THE MAINLOOP 
'''


def dijkstras(grid, draw, start_node, end_node):
    '''
    Algorithm is just a_star without heuristic function. Documentation
    sparse here as much of it would just be repeating what is already
    in a_star
    '''
    open_set = PriorityQueue()
    open_set_hash = set()
    count = 0
    path_map = dict()
    g_score_map = {node: float("inf") for row in grid for node in row}
    g_score_map[start_node] = 0

    open_set.put((g_score_map[start_node], count, start_node))
    open_set_hash.add(start_node)

    while open_set.qsize() != 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        cur_node = open_set.get()[2]
        open_set_hash.remove(cur_node)

        if cur_node == end_node:
            reconstruct_path(draw, path_map, start_node, end_node)
            return 0

        for neighbor in cur_node.get_unwalled_neighbors(grid):
            cur_g_score = g_score_map[cur_node] + 1

            if cur_g_score < g_score_map[neighbor]:
                g_score_map[neighbor] = cur_g_score
                path_map[neighbor] = cur_node


                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score_map[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
                    

        if cur_node != start_node:
            cur_node.set_closed()
    
        draw()
        sleep(0.05)

    return 0

def DFS(grid, draw, start_node, end_node):
    '''
    Uses the Depth-First-Search algorithm to find a path from start 
    to end of maze
    * grid: <list[list]> List of lists which are the rows and columns of the board
    * start_node: <Node> start node 
    * end_node: <Node> end node
    '''
    to_visit = LifoQueue()
    visited_set = set()
    path_map = dict()
    dist_map = dict()

    to_visit.put(start_node)
    visited_set.add(start_node)
    dist_map[start_node] = 0

    found_goal = False

    while to_visit.qsize() != 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        cur_node = to_visit.get()

        for neighbor in cur_node.get_unwalled_neighbors(grid):
            if neighbor not in visited_set:
                path_map[neighbor] = cur_node
                dist_map[neighbor] = dist_map[cur_node] + 1
                if neighbor == end_node:
                    
                    reconstruct_path(draw, path_map, start_node, end_node)
                    return 0

                visited_set.add(neighbor)
                to_visit.put(neighbor)
                neighbor.set_open()

        if cur_node != start_node:
            cur_node.set_closed()

        draw()
        sleep(0.05)


def carve_maze_backtracking(grid, draw):
    '''
    Will use iterative backtracking to randomly carve a maze out of 
    of the given grid
    * grid: <list[list]> List of lists containing nodes of the grid
    * draw: <func> Draws the current version of the grid
    * start_node: <Node> The starting node to begin carving from
    '''
    maze = grid
    open_set = LifoQueue()
    open_set_hash = set()
    visited_set = set()

    start_node = maze[0][0]

    open_set.put(start_node)
    open_set_hash.add(start_node)
    visited_set.add(start_node)
    while open_set.qsize() != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        cur_node = open_set.get()

        rand_neighbors = cur_node.get_walled_neighbors(maze)
        shuffle(rand_neighbors)

        for neighbor in rand_neighbors:
            if neighbor not in open_set_hash and neighbor not in visited_set:
                open_set.put(neighbor)
                open_set_hash.add(neighbor)
                visited_set.add(neighbor)
                cur_node.remove_wall(maze, neighbor)

                draw()
                
    return maze

