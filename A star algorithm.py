import heapq
import matplotlib.pyplot as plt 
import numpy as np

# Maze definition (0 = path, 1 = wall)
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

rows, cols = len(maze), len(maze[0])

# Start (bottom-right corner) and Goal (top-left corner)
start = (rows-1, cols-1)
goal = (0, 0)

# Directions (up, right, down, left)
directions = [(-1,0),(0,1),(1,0),(0,-1)]

class Node:
    def __init__(self, pos, dir_idx, g, h, parent=None):
        self.pos = pos
        self.dir_idx = dir_idx
        self.g = g
        self.h = h
        self.f = g+h
        self.parent = parent
    def __lt__(self, other): return self.f < other.f

def heuristic(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def astar():
    start_node = Node(start, 0, 0, heuristic(start, goal)) # facing up initially
    open_list = [start_node]
    closed = set()

    while open_list:
        current = heapq.heappop(open_list)
        if current.pos == goal:
            return reconstruct(current)
        
        state = (current.pos, current.dir_idx)
        if state in closed: continue
        closed.add(state)

        for turn in [0, 1, -1]:  # forward, right, left
            new_dir = (current.dir_idx + turn) % 4
            dr, dc = directions[new_dir]
            nr, nc = current.pos[0]+dr, current.pos[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc]==0:
                new_node = Node((nr,nc), new_dir, current.g+1,
                                heuristic((nr,nc), goal), current)
                heapq.heappush(open_list, new_node)
    return None

def reconstruct(node):
    path = []
    while node:
        path.append(node.pos)
        node = node.parent
    return path[::-1]

# Solve maze
path = astar()

if path:
    print("Path found:", path)
    # Visualization
    maze_img = np.array(maze)
    plt.imshow(maze_img, cmap="gray_r")
    path_r, path_c = zip(*path)
    plt.plot(path_c, path_r, color="red")
    plt.scatter(start[1], start[0], c="green", s=100) # start
    plt.scatter(goal[1], goal[0], c="blue", s=100)   # goal
    plt.gca().invert_yaxis()
    plt.show()
else:
    print("No path found.")
