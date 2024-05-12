import tkinter as tk
from tkinter import messagebox
import heapq
from grid import Grid
class App:
    def __init__(self, master, rows, cols, cell_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = Grid(master, rows, cols, cell_size)
        self.grid.pack()
        self.start_button = tk.Button(master, text="Chọn điểm xuất phát và đích", command=self.find_path)
        self.start_button.pack()
        self.restart_button = tk.Button(master, text="Restart", command=self.restart)
        self.restart_button.pack()

    def restart(self):

        self.grid.clear_points()  # Xóa các điểm đã chọn
        self.grid.bind("<Button-1>", self.grid.on_click)  # Cho phép chọn điểm trên lưới lại


    def find_path(self):
        if self.grid.start is not None and self.grid.goal is not None:
            path = self.astar(self.grid.start, self.grid.goal, self.grid.obstacles)
            if path:
                self.draw_path(path)
            else:
                messagebox.showinfo("Thông báo", "Không có đường để đi")

    def astar(self, start, goal, obstacles):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        came_from = {}  # Khởi tạo biến came_from

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            closed_set.add(current)

            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current[0] + di, current[1] + dj)
                if not self.is_valid_neighbor(neighbor, obstacles):
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_valid_neighbor(self, neighbor, obstacles):
        i, j = neighbor
        return 0 <= i < self.rows and 0 <= j < self.cols and neighbor not in obstacles

    def draw_path(self, path):
        for node in path[1:-1]:
            i, j = node
            self.grid.draw_point(i, j, "blue")
