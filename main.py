import tkinter as tk
from game import MorpionFootball

if __name__ == "__main__":
    root = tk.Tk()
    app = MorpionFootball(root)
    root.mainloop()