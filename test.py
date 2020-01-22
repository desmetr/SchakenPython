import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Window")

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    bQueen = ttk.Button(win, text="Queen", command=test)
    bQueen.grid(row=1, column=0)

    bRook = ttk.Button(win, text="Rook", command=test)
    bRook.grid(row=1, column=1)

def test():
    print("A")

class Application(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.button_bonus.pack()
        popup_bonus()

root = tk.Tk()

app = Application(root)

root.mainloop()