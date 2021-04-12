* This code will randomly generate a maze first and
  then spawn a player sprite. The player must find 
  their way to the end of the maze before the selected 
  algorithm can. There will be easy (DFS) and medium
  (Dijkstra's) and hard (A*) difficulties. The GUI
  will be made using pygame.

* Algorithms needed:
    * Recursive backtracking to generate the maze.
    * Depth-first search
    * Dijkstra's
    * A*

* Classes needed:
    * GUI class
    * Tile (node) class
    * player class

* Additional functions needed:
    * Draw function that continually updates GUI
    * Recreate path function
    * Create initial grid
    * heuristic for A* (taxicab)