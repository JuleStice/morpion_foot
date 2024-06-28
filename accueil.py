import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Accueil:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion Foot")
        self.root.geometry("800x600")
        
        # Background image
        self.bg_image = Image.open("images/stadium.jpg")  # Assurez-vous que l'image est dans le même répertoire
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Title
        self.title_frame = tk.Frame(self.root, bg="blue", bd=10, relief=tk.RIDGE)
        self.title_frame.place(relx=0.5, rely=0.1, anchor="center")
        self.title_label = tk.Label(self.title_frame, text="Morpion Foot", font=("Rockwell", 36, "bold"), bg="blue", fg="white")
        self.title_label.pack()

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="grey")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.play_button = tk.Button(self.button_frame, text="Jouer", font=("Helvetica", 14), command=self.launch_game)
        self.play_button.grid(row=0, column=0, padx=20, pady=10)
        self.play_button.bind("<Enter>", lambda e: self.on_hover(e, "darkblue", "white"))
        self.play_button.bind("<Leave>", lambda e: self.on_leave(e, "SystemButtonFace", "black"))

        self.stats_button = tk.Button(self.button_frame, text="Statistiques", font=("Helvetica", 14), command=self.show_stats)
        self.stats_button.grid(row=1, column=0, padx=20, pady=10)
        self.stats_button.bind("<Enter>", lambda e: self.on_hover(e, "lightgreen", "white"))
        self.stats_button.bind("<Leave>", lambda e: self.on_leave(e, "SystemButtonFace", "black"))

        self.options_button = tk.Button(self.button_frame, text="Options", font=("Helvetica", 14), command=self.show_options)
        self.options_button.grid(row=2, column=0, padx=20, pady=10)
        self.options_button.bind("<Enter>", lambda e: self.on_hover(e, "brown", "white"))
        self.options_button.bind("<Leave>", lambda e: self.on_leave(e, "SystemButtonFace", "black"))

    def on_hover(self, event, bg_color, fg_color):
        event.widget.config(bg=bg_color, fg=fg_color)

    def on_leave(self, event, bg_color, fg_color):
        event.widget.config(bg=bg_color, fg=fg_color)

    def launch_game(self):
        self.root.destroy()
        import game
        game.main()

    def show_stats(self):
        self.root.destroy()
        import stats
        stats.main()

    def show_options(self):
        self.root.destroy()
        import options
        options.main()

def main():
    root = tk.Tk()
    app = Accueil(root)
    root.mainloop()

if __name__ == "__main__":
    main()
