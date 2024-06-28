import tkinter as tk
from PIL import Image, ImageTk


class Options:
    def __init__(self, root):
        self.root = root
        self.root.title("Options")
        self.root.geometry("800x600")

        self.bg_image = Image.open("images/room.jpg")  # Assurez-vous que l'image est dans le même répertoire
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)


        self.options_frame = tk.Frame(self.root, bg="grey")
        self.options_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.modify_player_button = tk.Button(self.options_frame, text="Ajouter / Modifier Joueur", font=("Helvetica", 14), command=self.modify_player)
        self.modify_player_button.grid(row=0, column=0, padx=20, pady=10)

        self.back_button = tk.Button(self.options_frame, text="Retour", font=("Helvetica", 14), command=self.go_back)
        self.back_button.grid(row=1, column=0, padx=20, pady=10)

    def modify_player(self):
        self.root.destroy()
        import modif_player
        modif_player.main()

    def go_back(self):
        self.root.destroy()
        import accueil
        accueil.main()

def main():
    root = tk.Tk()
    app = Options(root)
    root.mainloop()

if __name__ == "__main__":
    main()
