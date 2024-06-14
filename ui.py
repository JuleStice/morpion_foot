import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

def setup_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=5)
    style.configure("TLabel", font=("Helvetica", 12), padding=5)
    style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), padding=10)
    style.configure("SearchResult.TLabel", font=("Helvetica", 10), padding=5, background="white", relief="solid", borderwidth=1)

def create_title_label(root, text, row, columnspan):
    label = ttk.Label(root, text=text, font=("Helvetica", 18, "bold"), anchor="center", background="white")
    label.grid(row=row, columnspan=columnspan, pady=10)
    return label