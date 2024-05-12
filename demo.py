import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import heapq
import time

class Grid(tk.Canvas):
    def __init__(self, master, rows, cols, cell_size, img_size):
        super().__init__(master, width=cols * cell_size, height=rows * cell_size)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.img_size = img_size
        self.grid = [[0] * cols for _ in range(rows)]
        self.start = None
        self.goal = None
        self.obstacles = set()
        self.car_img = Image.open("car_image.jpg")
        self.car_image = ImageTk.PhotoImage(self.car_img.resize((self.img_size, self.img_size)))
        self.bind("<Button-1>", self.on_click)
        self.load_images()
        self.draw_grid()

    def load_images(self):
        car_image = Image.open("car_image.jpg")
        self.car_img = ImageTk.PhotoImage(car_image.resize((self.img_size, self.img_size)))

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def clear_points(self):
        self.start = None
        self.goal = None
        self.obstacles.clear()
        self.delete("point")  # Xóa tất cả các điểm đã chọn trên lưới
        self.grid = [[0] * self.cols for _ in range(self.rows)]  # Cập nhật lại lưới
        self.draw_grid()  # Vẽ lại lưới sau khi xóa

    def on_click(self, event):
        i = event.y // self.cell_size
        j = event.x // self.cell_size
        if self.grid[i][j] == 0:
            if self.start is None:
                self.start = (i, j)
                self.draw_point(i, j, "green", self.car_image)
            elif self.goal is None:
                self.goal = (i, j)
                self.draw_point(i, j, "red", None)
            else:
                self.obstacles.add((i, j))
                self.draw_point(i, j, "black", None)

    def draw_point(self, i, j, color, image):
        x0, y0 = j * self.cell_size, i * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        if image:
            self.create_image(x0, y0, anchor=tk.NW, image=image, tags="point")
        else:
            self.create_rectangle(x0, y0, x1, y1, outline="black", fill=color, tags="point")
        self.grid[i][j] = 1 if color == "green" else 2


class App:
    def __init__(self, master, rows, cols, cell_size, img_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.img_size = img_size
        self.grid = Grid(master, rows, cols, cell_size, img_size)
        self.grid.pack()
        self.start_button = tk.Button(master, text="Chọn điểm xuất phát và đích", command=self.find_path)
        self.start_button.pack()
        self.restart_button = tk.Button(master, text="Restart", command=self.restart)
        self.restart_button.pack()
        self.d_star_button = tk.Button(master, text="D star", command=self.run_d_star)
        self.d_star_button.pack()

    def restart(self):
        self.grid.clear_points()

    def find_path(self):
        if self.grid.start is not None and self.grid.goal is not None:
            if hasattr(self, "algorithm"):
                if  self.algorithm == "D*":
                    path = self.dstar(self.grid.goal, self.grid.start, self.grid.obstacles)
                else:
                    messagebox.showinfo("Thông báo", "Vui lòng chọn thuật toán trước khi tìm đường")
                    return

                if path:
                    self.move_car(path)
                else:
                    messagebox.showinfo("Thông báo", "Không có đường để đi")
            else:
                messagebox.showinfo("Thông báo", "Vui lòng chọn thuật toán trước khi tìm đường")



    def run_d_star(self):
        self.algorithm = "D*"
        self.find_path()



    def dstar(self, start, goal, obstacles):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        came_from = {}

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
    def move_car(self, path):
        # Vẽ hình ảnh của xe ở điểm xuất phát
        start_i, start_j = path[0]
        self.grid.draw_point(start_i, start_j, "green", self.grid.car_image)
        self.master.update()
        time.sleep(0.2)

        # Di chuyển hình ảnh của xe từ điểm xuất phát đến điểm đích
        for node in path[1:-1]:
            i, j = node
            self.grid.draw_point(i, j, "blue", self.grid.car_image)
            self.master.update()
            time.sleep(0.2)  # Đợi một lát trước khi di chuyển đến ô tiếp theo

    def heuristic(self, a, b):
        # Sử dụng heuristic Euclidean distance
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    def is_valid_neighbor(self, neighbor, obstacles):
        i, j = neighbor
        return 0 <= i < self.rows and 0 <= j < self.cols and neighbor not in obstacles


def main():
    rows = 10
    cols = 10
    cell_size = 30
    img_size = 30  # Kích thước hình ảnh của xe
    root = tk.Tk()
    app = App(root, rows, cols, cell_size, img_size)
    root.mainloop()


if __name__ == "__main__":
    main()
