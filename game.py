import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import difflib
from ui import setup_styles, create_title_label
from tkinter import ttk  # Ajout de cette ligne
from players_db import players_db
from difflib import SequenceMatcher



class MorpionFootball:
    
    def __init__(self, root):
        self.root = root
        self.grid_size = 3
        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.current_player = "Joueur 1"
        self.players_db = players_db
        self.colors = {"Joueur 1": "lightcoral", "Joueur 2": "lightblue"}
        self.scores = {"Joueur 1": 0, "Joueur 2": 0}
        self.rounds_to_win = 3
        self.flags, self.clubs = self.load_flags_and_competitions()
        self.row_categories = []
        self.column_categories = []
        self.first_player = "Joueur 1"
        self.labels = []
        self.setup_game()

    def load_flags_and_competitions(self):
        flag_paths = {
            "Argentine": "images/argentina.png",
            "France": "images/france.png",
            "Espagne": "images/spain.png",
            "Angleterre": "images/england.png",
            "Brésil": "images/brazil.png",
            "Portugal": "images/portugal.png",
            "Croatie": "images/croatia.png",
            "Allemagne": "images/germany.png",
            "Belgique": "images/belgium.png",
        }
        
        club_paths = {
         "Real Madrid": "images/real_madrid.png",
            "Bayern Munich": "images/bayern.png",
            "Manchester United": "images/man_united.png",
            "Juventus": "images/juventus.png",
            "Manchester City": "images/man_city.png",
            "AC Milan": "images/ac_milan.png",
            "Atletico Madrid": "images/atletico.png",
            "Borussia Dortmund": "images/dortmund.png",
            "PSG": "images/psg.png",
            "Barcelone": "images/barcelona.png",
            "Coupe du monde": "images/world_cup.png",
            "Copa America": "images/copa_america.png",
            "Ligue des Champions": "images/champions_league.png",
            "Euro": "images/euro.png",
            "Ligue 1": "images/ligue_1.png",
            "Liga": "images/liga.png",
            "Serie A": "images/serie_a.png",
            "Bundesliga": "images/bundesliga.png",
            "Chelsea": "images/chelsea.png",
            "+100 buts": "images/goals.png"
        }
        
        flags = {}
        for name, path in flag_paths.items():
            image = Image.open(path)
            image = image.resize((50, 30), Image.LANCZOS)  # Resize to 50x30
            flags[name] = ImageTk.PhotoImage(image)
        
        clubs = {}
        for name, path in club_paths.items():
            image = Image.open(path)
            image = image.resize((50, 50), Image.LANCZOS)  # Resize to 50x50
            clubs[name] = ImageTk.PhotoImage(image)
        
        return flags, clubs

    def setup_game(self):
        self.create_widgets()
        self.reset_game()


    def create_widgets(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text())
        self.score_label.grid(row=0, columnspan=self.grid_size + 3)

        self.turn_label = tk.Label(self.root, text=f"À {self.current_player} de jouer")
        self.turn_label.grid(row=1, columnspan=self.grid_size + 3)

        # Grille de jeu
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(self.root, text="", width=15, height=5,
                                command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row + 3, column=col + 2)
                self.buttons[row][col] = button

        self.pass_button = tk.Button(self.root, text="Passe ton tour", command=self.pass_turn)
        self.pass_button.grid(row=self.grid_size + 5, columnspan=self.grid_size + 3)

        self.draw_button = tk.Button(self.root, text="Match nul", command=self.confirm_draw)
        self.draw_button.grid(row=self.grid_size + 6, columnspan=self.grid_size + 3)

        # Ajouter les widgets pour la recherche en bas
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=self.grid_size + 7, column=0, columnspan=2)

        self.search_button = tk.Button(self.root, text="Rechercher", command=self.search_player)
        self.search_button.grid(row=self.grid_size + 7, column=2)

        self.search_result_label = tk.Label(self.root, text="")
        self.search_result_label.grid(row=self.grid_size + 8, column=0, columnspan=self.grid_size + 3)


    def confirm_draw(self):
        response = messagebox.askyesno("Confirmation", "Voulez-vous vraiment déclarer un match nul?")
        if response:
            self.reset_game()

    def get_score_text(self):
        return f"Joueur 1: {self.scores['Joueur 1']} - Joueur 2: {self.scores['Joueur 2']}"

    def make_move(self, row, col):
        player_name = simpledialog.askstring("Input", f"{self.current_player}, entrez le nom du joueur:")
        if player_name and self.grid[row][col] == "" and self.check_validity(player_name, row, col):
            self.grid[row][col] = player_name
            self.buttons[row][col].config(text=player_name, bg=self.colors[self.current_player])
            if self.check_winner():
                self.scores[self.current_player] += 1
                messagebox.showinfo("Gagné", f"{self.current_player} a gagné cette manche!")
                self.update_score()
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Match nul", "Il n'y a plus de coup possible. Match nul!")
                self.reset_game()
            else:
                self.switch_player()
        else:
            messagebox.showwarning("Erreur", "Mouvement invalide ou case déjà occupée!")
            self.switch_player()

    def check_validity(self, player, row, col):
        category_col = self.column_categories[col]
        category_row = self.row_categories[row]
        if player in self.players_db:
            player_info = self.players_db[player]
            if ((category_col in player_info["competitions"] or category_col == player_info["country"] or category_col in player_info["clubs"]) and
                (category_row in player_info["competitions"] or category_row == player_info["country"] or category_row in player_info["clubs"])):
                return True
        return False

    def check_winner(self):
        def same_color(buttons):
            color = buttons[0].cget('bg')
            return all(button.cget('bg') == color and color in self.colors.values() for button in buttons)

        for row in range(self.grid_size):
            if same_color([self.buttons[row][col] for col in range(self.grid_size)]):
                return True
        for col in range(self.grid_size):
            if same_color([self.buttons[row][col] for row in range(self.grid_size)]):
                return True
        if same_color([self.buttons[i][i] for i in range(self.grid_size)]) or same_color([self.buttons[i][self.grid_size - 1 - i] for i in range(self.grid_size)]):
            return True

        return False

    def check_draw(self):
        return all(self.grid[row][col] != "" for row in range(self.grid_size) for col in range(self.grid_size))

    def switch_player(self):
        self.current_player = "Joueur 1" if self.current_player == "Joueur 2" else "Joueur 2"
        self.turn_label.config(text=f"À {self.current_player} de jouer", bg=self.colors[self.current_player])

    def update_score(self):
        self.score_label.config(text=self.get_score_text())
        if self.scores["Joueur 1"] == self.rounds_to_win:
            messagebox.showinfo("Gagné", "Joueur 1 a gagné la partie!")
            self.reset_game(True)
        elif self.scores["Joueur 2"] == self.rounds_to_win:
            messagebox.showinfo("Gagné", "Joueur 2 a gagné la partie!")
            self.reset_game(True)


    def reset_game(self, reset_scores=False):
        if reset_scores:
            self.scores = {"Joueur 1": 0, "Joueur 2": 0}
            self.update_score()

        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.row_categories, self.column_categories = self.generate_valid_categories()

        # Effacer les anciens labels de catégories
        for label in self.labels:
            label.destroy()
        self.labels.clear()

        # Afficher les catégories des lignes et colonnes
        for i in range(self.grid_size):
            if self.row_categories[i] in self.flags:
                row_label = tk.Label(self.root, image=self.flags[self.row_categories[i]], text=self.row_categories[i], compound="top")
            else:
                row_label = tk.Label(self.root, image=self.clubs.get(self.row_categories[i], None), text=self.row_categories[i], compound="top")
            row_label.grid(row=i + 3, column=0)
            self.labels.append(row_label)

            if self.column_categories[i] in self.flags:
                column_label = tk.Label(self.root, image=self.flags[self.column_categories[i]], text=self.column_categories[i], compound="top")
            else:
                column_label = tk.Label(self.root, image=self.clubs.get(self.column_categories[i], None), text=self.column_categories[i], compound="top")
            column_label.grid(row=2, column=i + 2)
            self.labels.append(column_label)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.buttons[row][col].config(text="", bg="SystemButtonFace")

        self.current_player = self.first_player
        self.first_player = "Joueur 1" if self.first_player == "Joueur 2" else "Joueur 2"
        self.turn_label.config(text=f"À {self.current_player} de jouer", bg=self.colors[self.current_player])
        self.draw_button.config(state=tk.NORMAL)

        # Réinitialiser les résultats de recherche
        self.search_result_label.config(text="")

    
    def pass_turn(self):
        self.switch_player()

    def generate_valid_categories(self):
        while True:
            all_categories = ["Argentine", "France", "Espagne", "Angleterre", "Brésil", "Portugal", "Croatie","Allemagne","Belgique",
                              "Coupe du monde", "Copa America", "Ligue des Champions", "Euro", "Ligue 1", "Liga","Bundesliga","Serie A",
                              "Real Madrid", "PSG", "Barcelone","Liverpool","Juventus","AC Milan","Chelsea","Manchester United","Atletico Madrid","Borussia Dortmund","Manchester City","Bayern Munich","+100 buts","+300 matchs"]
            random.shuffle(all_categories)

            row_categories = random.sample(all_categories, self.grid_size)
            all_categories= [a for a in all_categories if a not in row_categories]
            column_categories = random.sample(all_categories, self.grid_size)

            if self.validate_grid(row_categories, column_categories):
                return row_categories, column_categories

    def validate_grid(self, row_categories, column_categories):
        for row in row_categories:
            for col in column_categories:
                if not any((row in self.players_db[player]["competitions"] or row == self.players_db[player]["country"] or row in self.players_db[player]["clubs"] or
                             (row == "+300 matchs" and self.players_db[player]["matches"] > 300) or (row == "+100 buts" and self.players_db[player]["goals"] > 100)) and
                           (col in self.players_db[player]["competitions"] or col == self.players_db[player]["country"] or col in self.players_db[player]["clubs"] or 
                           (col == "+300 matchs" and self.players_db[player]["matches"] > 300) or (col == "+100 buts" and self.players_db[player]["goals"] > 100))
                           for player in self.players_db):
                    return False
        return True
        
    def search_player(self):
        query = self.search_entry.get()
        if not query:
            self.search_result_label.config(text="Veuillez entrer un nom de joueur.")
            return

        matches = difflib.get_close_matches(query, self.players_db.keys(), n=3, cutoff=0.0)
        result_text = "Résultats de la recherche :\n"
        for match in matches:
            similarity = difflib.SequenceMatcher(None, query, match).ratio()
            result_text += f"{match} - {similarity * 100:.0f}%\n"

        self.search_result_label.config(text=result_text)












    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio() * 100

    def search_player2(self):
        query = self.player_search_entry.get().strip().lower()
        if not query:
            self.search_results_label.config(text="Veuillez entrer un nom de joueur.", style="TLabel")
            return

        results = []
        for player in self.players_db:
            similarity = self.similarity(query, player.lower())
            if similarity > 0:
                results.append((player, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        top_results = results[:3]

        if not top_results:
            self.search_results_label.config(text="Aucun joueur trouvé.", style="TLabel")
            return

        results_text = "\n".join([f"{player} - {similarity:.2f}%" for player, similarity in top_results])
        self.search_results_label.config(text=results_text, style="TLabel")

    def reset_game2(self, reset_scores=False):
        if reset_scores:
            self.scores = {"Joueur 1": 0, "Joueur 2": 0}
            self.update_score()

        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.row_categories, self.column_categories = self.generate_valid_categories()

        # Effacer les anciens labels de catégories
        for label in self.labels:
            label.destroy()
        self.labels.clear()

        # Afficher les catégories des lignes et colonnes
        for i in range(self.grid_size):
            if self.row_categories[i] in self.flags:
                row_label = ttk.Label(self.root, image=self.flags[self.row_categories[i]], text=self.row_categories[i], compound="top", style="TLabel")
            else:
                row_label = ttk.Label(self.root, image=self.clubs.get(self.row_categories[i], None), text=self.row_categories[i], compound="top", style="TLabel")
            row_label.grid(row=i + 3, column=0)
            self.labels.append(row_label)

            if self.column_categories[i] in self.flags:
                column_label = ttk.Label(self.root, image=self.flags[self.column_categories[i]], text=self.column_categories[i], compound="top", style="TLabel")
            else:
                column_label = ttk.Label(self.root, image=self.clubs.get(self.column_categories[i], None), text=self.column_categories[i], compound="top", style="TLabel")
            column_label.grid(row=2, column=i + 2)
            self.labels.append(column_label)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.buttons[row][col].config(text="", style="TButton")

        self.current_player = self.first_player
        self.first_player = "Joueur 1" if self.first_player == "Joueur 2" else "Joueur 2"
        self.turn_label.config(text=f"À {self.current_player} de jouer", background=self.colors[self.current_player])

    def create_widgets2(self):
        setup_styles()

        # Titre principal
        create_title_label(self.root, "Morpion Football", row=0, columnspan=self.grid_size + 3)

        self.score_label = ttk.Label(self.root, text=self.get_score_text(), style="TLabel")
        self.score_label.grid(row=1, columnspan=self.grid_size + 3)

        self.turn_label = ttk.Label(self.root, text=f"À {self.current_player} de jouer", style="TLabel", background=self.colors[self.current_player])
        self.turn_label.grid(row=2, columnspan=self.grid_size + 3)

        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = ttk.Button(self.root, text="", width=5, command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row + 4, column=col + 2, ipadx=10, ipady=10)  # Ajuster ipadx et ipady pour rendre les boutons carrés
                self.buttons[row][col] = button

        self.pass_button = ttk.Button(self.root, text="Passe ton tour", command=self.pass_turn)
        self.pass_button.grid(row=self.grid_size + 5, columnspan=self.grid_size + 3)

        # Partie recherche joueur
        search_title = ttk.Label(self.root, text="Rechercher un joueur", style="Title.TLabel")
        search_title.grid(row=self.grid_size + 6, columnspan=self.grid_size + 3)

        self.player_search_entry = ttk.Entry(self.root)
        self.player_search_entry.grid(row=self.grid_size + 7, column=1, columnspan=2)

        self.search_button = ttk.Button(self.root, text="Chercher", command=self.search_player)
        self.search_button.grid(row=self.grid_size + 7, column=3)

        self.search_results_frame = ttk.Frame(self.root, style="SearchResult.TLabel")
        self.search_results_frame.grid(row=self.grid_size + 8, column=1, columnspan=3, sticky="ew")

        self.search_results_label = ttk.Label(self.search_results_frame, text="", style="SearchResult.TLabel")
        self.search_results_label.grid(row=0, column=0, sticky="ew")
