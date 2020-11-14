import tkinter as tk
from src.gui.app_gui import AppGUI

if __name__ == '__main__':
    root = tk.Tk()
    app = AppGUI(root)
    app.mainloop()
