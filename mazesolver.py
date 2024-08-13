import heapq
import tkinter as tk

class Node:
    def __init__(self, row, col, parent=None):
        self.row = row
        self.col = col
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost from current node to goal)

    def __lt__(self, other):
        # Comparison function for priority queue
        return (self.g + self.h) < (other.g + other.h)

def heuristic(node, goal):
    # Manhattan distance heuristic
    return abs(node.row - goal.row) + abs(node.col - goal.col)

def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = [Node(start[0], start[1])]
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)

        if (current.row, current.col) == goal:
            path = []
            while current:
                path.append((current.row, current.col))
                current = current.parent
            return path[::-1]

        closed_set.add((current.row, current.col))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = current.row + dr, current.col + dc

            if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 0 \
                    and (new_row, new_col) not in closed_set:
                neighbor = Node(new_row, new_col, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor, Node(goal[0], goal[1]))
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

    return None  # No path found

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        self.canvas = tk.Canvas(root, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.maze = [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0]
            
        ]

        self.start_point = (0, 0)
        self.goal_point = (6, 6)

        self.draw_maze()
        self.solve_button = tk.Button(root, text="Solve", command=self.solve_maze)
        self.solve_button.grid(row=1, column=0)

    def draw_maze(self):
        cell_size = 80
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                color = "white" if self.maze[row][col] == 0 else "black"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def solve_maze(self):
        result = astar(self.maze, self.start_point, self.goal_point)
        if result:
            self.highlight_path(result)
        else:
            self.show_message("No path found.")

    def highlight_path(self, path):
        cell_size = 80
        for row, col in path:
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="gray")

    def show_message(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Message")
        label = tk.Label(popup, text=message)
        label.pack(pady=10)
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()







