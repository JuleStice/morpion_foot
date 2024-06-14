import tkinter as tk
from tkinter import messagebox, simpledialog

class MorpionFootball:
    def __init__(self, root):
        self.grid_size = 3
        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.column_categories = ["Argentine", "Brésil", "France"]
        self.row_categories = ["Coupe du monde", "Copa America", "Ligue des Champions"]
        self.players_db = {
            "Messi": {"country": "Argentine", "competitions": ["Coupe du monde", "Copa America", "Ligue des Champions"]},
            "Pele": {"country": "Brésil", "competitions": ["Coupe du monde", "Copa America"]},
            "Zidane": {"country": "France", "competitions": ["Coupe du monde", "Ligue des Champions"]},
        }
        self.current_player = "Joueur 1"
        self.create_widgets(root)

    def create_widgets(self, root):
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(root, text="", width=15, height=5, 
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row+1, column=col)
                self.buttons[row][col] = button
        
        for col, category in enumerate(self.column_categories):
            label = tk.Label(root, text=category)
            label.grid(row=0, column=col)

        for row, category in enumerate(self.row_categories):
            label = tk.Label(root, text=category)
            label.grid(row=row+1, column=self.grid_size)
    
    def make_move(self, row, col):
        player_name = tk.simpledialog.askstring("Input", f"{self.current_player}, entrez le nom du joueur:")
        if self.grid[row][col] == "" and self.check_validity(player_name, self.column_categories[col], self.row_categories[row]):
            self.grid[row][col] = player_name
            self.buttons[row][col].config(text=player_name)
            if self.check_winner(player_name):
                messagebox.showinfo("Gagné", f"{self.current_player} a gagné!")
                self.root.quit()
            self.switch_player()
        else:
            messagebox.showwarning("Erreur", "Mouvement invalide ou case déjà occupée!")

    def check_validity(self, player, country, competition):
        if player in self.players_db:
            player_info = self.players_db[player]
            if player_info["country"] == country and competition in player_info["competitions"]:
                return True
        return False

    def check_winner(self, player):
        for row in self.grid:
            if all([cell == player for cell in row]):
                return True
        for col in range(self.grid_size):
            if all([self.grid[row][col] == player for row in range(self.grid_size)]):
                return True
        if all([self.grid[i][i] == player for i in range(self.grid_size)]) or all([self.grid[i][self.grid_size - 1 - i] == player for i in range(self.grid_size)]):
            return True
        return False

    def switch_player(self):
        self.current_player = "Joueur 1" if self.current_player == "Joueur 2" else "Joueur 2"

# Main code
if __name__ == "__main__":
    root = tk.Tk()
    app = MorpionFootball(root)
    root.mainloop()