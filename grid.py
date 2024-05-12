import tkinter as tk


class Grid(tk.Canvas):
    def __init__(self, master, rows, cols, cell_size):
        super().__init__(master, width=cols * cell_size, height=rows * cell_size)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0] * cols for _ in range(rows)]
        self.start = None
        self.goal = None
        self.obstacles = set()
        self.bind("<Button-1>", self.on_click)
        self.draw_grid()

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
                self.draw_point(i, j, "green")
            elif self.goal is None:
                self.goal = (i, j)
                self.draw_point(i, j, "red")
            else:
                self.obstacles.add((i, j))
                self.draw_point(i, j, "black")

    def draw_point(self, i, j, color):
        x0, y0 = j * self.cell_size, i * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.create_rectangle(x0, y0, x1, y1, outline="black", fill=color)
        self.grid[i][j] = 1 if color == "green" else 2
