import matplotlib.pyplot as plt
import numpy as np
import math
import time
import random
from matplotlib.collections import LineCollection


class Node:
    def __init__(self, parent=None, position=None, direction=None, action=None):
        self.parent = parent
        self.position = position
        self.direction = direction  
        self.action = action        
        self.g = 0  
        self.h = 0  
        self.f = 0  

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction


def get_new_direction(current_direction, turn):
    directions = ['up', 'right', 'down', 'left']
    idx = directions.index(current_direction)
    if turn == 'right':
        return directions[(idx + 1) % 4]
    elif turn == 'left':
        return directions[(idx - 1) % 4]
    return current_direction  


def get_new_position(position, direction):
    moves = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    move = moves[direction]
    return (position[0] + move[0], position[1] + move[1])


def euclidean_distance(a, b):
   return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
#def manhattan_distance(a, b):
#   return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(maze, start, end):
    start_direction = 'up' 
    start_node = Node(None, start, start_direction, "Start")
    end_node = Node(None, end, None)

    open_list = [start_node]
    closed_list = []

    while open_list:
        current_node = min(open_list, key=lambda n: n.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current:
                path.append((current.position, current.direction, current.action))
                current = current.parent
            return path[::-1]

        actions = ['forward', 'right', 'left']

        for move_action in actions:
            new_direction = get_new_direction(current_node.direction, move_action if move_action != 'forward' else None)
            new_position = get_new_position(current_node.position, new_direction)

            if (0 <= new_position[0] < len(maze)) and (0 <= new_position[1] < len(maze[0])) and (maze[new_position[0]][new_position[1]] == 0):
                new_node = Node(current_node, new_position, new_direction,
                                f"{'Turn ' + move_action.capitalize() + ' and Move Forward' if move_action != 'forward' else 'Move Forward'}")

                if new_node in closed_list:
                    continue

                new_node.g = current_node.g + 1
                new_node.h = euclidean_distance(new_node.position, end_node.position)
                #new_node.h = manhattan_distance(new_node.position, end_node.position)
                new_node.f = new_node.g + new_node.h

                existing = next((n for n in open_list if n == new_node), None)
                if existing and new_node.g >= existing.g:
                    continue

                open_list.append(new_node)

    return None 


def visualize_maze(maze, path, start, end):
    plt.imshow(maze, cmap='gray_r')
    if path:
        y_path, x_path = zip(*[p[0] for p in path])
        points = np.array([x_path, y_path]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap='autumn', linewidth=3)
        lc.set_array(np.linspace(0, 1, len(segments)))
        plt.gca().add_collection(lc)
    plt.scatter([start[1]], [start[0]], color='green', s=100, label='Start')
    plt.scatter([end[1]], [end[0]], color='blue', s=100, label='End')
    plt.legend()
    plt.title("Random Maze Pathfinding (A*) - Guaranteed Solvable")
    plt.show()


def generate_random_maze(rows, cols, wall_prob=0.3):
    maze = [[1 if random.random() < wall_prob else 0 for _ in range(cols)] for _ in range(rows)]
    maze[0][0] = 0  
    maze[rows-1][cols-1] = 0  
    return maze
for row in generate_random_maze(20, 20):
     print(" ".join(str(cell) for cell in row))


def main():
    rows, cols = 20, 20  
    wall_prob = 0.3
    start = (0, 0)
    end = (rows - 1, cols - 1)

    attempt = 1
    while True:
        print(f"\n🌀 Generating random maze (Attempt {attempt})...")
        maze = generate_random_maze(rows, cols, wall_prob)
        path = astar(maze, start, end)

        if path:
            print(f"✅ Solvable maze found after {attempt} attempt(s)!\n")
            for p, d, a in path:
                print(f"Position: {p}, Facing: {d}, Action: {a}")
            visualize_maze(maze, path, start, end)
            break
        else:
            print("❌ No path found, regenerating...\n")
            attempt += 1
            time.sleep(0.3)


if __name__ == '__main__':
    main()
