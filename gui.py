import tkinter as tk
from grid import Grid
from app import App

def main():
    rows = 10
    cols = 10
    cell_size = 30
    root = tk.Tk()
    app = App(root, rows, cols, cell_size)
    root.mainloop()

if __name__ == "__main__":
    main()
