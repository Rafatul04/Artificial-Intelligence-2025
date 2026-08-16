import heapq
import matplotlib.pyplot as plt
import numpy as np

# Define movement directions
# Up, Right, Down, Left
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Heuristic function (Euclidean)
def heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def is_valid(maze, pos):
    r, c = pos
    return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0

def get_neighbors(maze, pos, direction):
    neighbors = []
    for turn in [-1, 0, 1]:  # Left, Forward, Right
        new_dir = (direction + turn) % 4
        new_r = pos[0] + directions[new_dir][0]
        new_c = pos[1] + directions[new_dir][1]
        new_pos = (new_r, new_c)
        if is_valid(maze, new_pos):
            neighbors.append((new_pos, new_dir))
    return neighbors

def a_star_with_constraints(maze, start, end):
    open_list = []
    closed_set = set()

    # ✅ Try all possible starting directions (Up, Right, Down, Left)
    for start_dir in range(4):
        heapq.heappush(open_list, (heuristic(start, end), 0, start, start_dir, [start]))

    while open_list:
        f, g, pos, direction, path = heapq.heappop(open_list)

        if (pos, direction) in closed_set:
            continue
        closed_set.add((pos, direction))

        if pos == end:
            return path

        for (new_pos, new_dir) in get_neighbors(maze, pos, direction):
            if (new_pos, new_dir) not in closed_set:
                new_g = g + 1
                new_f = new_g + heuristic(new_pos, end)
                heapq.heappush(open_list, (new_f, new_g, new_pos, new_dir, path + [new_pos]))

    return None

def plot_maze(maze, path, start, end):
    maze_img = np.array(maze)
    plt.imshow(maze_img, cmap="binary")
    plt.xticks([]), plt.yticks([])

    if path:
        pr, pc = zip(*path)
        plt.plot(pc, pr, color="red", linewidth=2)
        plt.scatter(start[1], start[0], color="green", s=100, label="Start")
        plt.scatter(end[1], end[0], color="blue", s=100, label="End")
        plt.legend()
    plt.show()

# === TEST MAZE (You can swap any of the three below) ===

maze = [
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
]

start = (9, 9)
end = (9, 0)

# === RUN ===
path = a_star_with_constraints(maze, start, end)

if path:
    print("✅ Path found!")
    print("Steps:")
    for p in path:
        print(p)
else:
    print("❌ No path found.")

plot_maze(maze, path, start, end)
