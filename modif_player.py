import tkinter as tk
from tkinter import ttk, messagebox
import json
import players_db  # Assurez-vous que ce chemin est correct

class PlayerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Joueurs")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.add_tab = ttk.Frame(self.notebook)
        self.modify_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Ajouter un joueur")
        self.notebook.add(self.modify_tab, text="Modifier un joueur")

        self.create_add_widgets()
        self.create_modify_widgets()

    def create_add_widgets(self):
        tk.Label(self.add_tab, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        self.add_name_entry = tk.Entry(self.add_tab)
        self.add_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_tab, text="Nationalité:").grid(row=1, column=0, padx=5, pady=5)
        self.add_nationality_var = tk.StringVar()
        self.add_nationality_menu = ttk.Combobox(self.add_tab, textvariable=self.add_nationality_var, values=["Argentine", "France", "Brésil", "Portugal", "Italie", "Allemagne",
                                                                                                               "Angleterre", "Belgique", "Croatie","Espagne","Pays-Bas"])
        self.add_nationality_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_tab, text="Compétitions:").grid(row=2, column=0, padx=5, pady=5)
        self.add_competition_vars = {comp: tk.BooleanVar() for comp in ["Coupe du monde", "Copa America", "Ligue des Champions", "Euro", "Ligue 1", "Liga", "Serie A", "Premier League","Bundesliga"]}
        for i, comp in enumerate(self.add_competition_vars):
            tk.Checkbutton(self.add_tab, text=comp, variable=self.add_competition_vars[comp]).grid(row=2+i//3, column=1+i%3, sticky="w")

        tk.Label(self.add_tab, text="Clubs:").grid(row=6, column=0, padx=5, pady=5)
        self.add_club_vars = {club: tk.BooleanVar() for club in ["Real Madrid", "PSG", "Barcelone", "Liverpool", "Juventus", "AC Milan", "Chelsea", "Manchester United",
                                                                 "Manchester City", "Bayern Munich", "Arsenal", "Monaco", "Borussia Dortmund", 
                                                                 "Atletico Madrid","Inter Milan","Benfica","Porto","Ajax"]}
        for i, club in enumerate(self.add_club_vars):
            tk.Checkbutton(self.add_tab, text=club, variable=self.add_club_vars[club]).grid(row=6+i//3, column=1+i%3, sticky="w")

        tk.Label(self.add_tab, text="Nombre de matchs:").grid(row=12, column=0, padx=5, pady=5)
        self.add_matches_entry = tk.Entry(self.add_tab)
        self.add_matches_entry.grid(row=12, column=1, padx=5, pady=5)

        tk.Label(self.add_tab, text="Nombre de buts:").grid(row=13, column=0, padx=5, pady=5)
        self.add_goals_entry = tk.Entry(self.add_tab)
        self.add_goals_entry.grid(row=13, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.add_tab, text="Ajouter", command=self.add_player)
        self.add_button.grid(row=14, column=0, columnspan=3, pady=10)

    def create_modify_widgets(self):
        tk.Label(self.modify_tab, text="Nationalité:").grid(row=0, column=0, padx=5, pady=5)
        self.modify_nationality_var = tk.StringVar()
        self.modify_nationality_menu = ttk.Combobox(self.modify_tab, textvariable=self.modify_nationality_var, values=["Argentine", "France", "Brésil", "Portugal", "Italie", "Allemagne", 
                                                                                                                       "Angleterre", "Belgique", "Croatie","Espagne","Pays-Bas"])
        self.modify_nationality_menu.grid(row=0, column=1, padx=5, pady=5)
        self.modify_nationality_menu.bind("<<ComboboxSelected>>", self.update_player_list)

        tk.Label(self.modify_tab, text="Joueur:").grid(row=1, column=0, padx=5, pady=5)
        self.player_var = tk.StringVar()
        self.player_menu = ttk.Combobox(self.modify_tab, textvariable=self.player_var)
        self.player_menu.grid(row=1, column=1, padx=5, pady=5)
        self.player_menu.bind("<<ComboboxSelected>>", lambda e: self.on_player_selected(self.player_var.get()))

        tk.Label(self.modify_tab, text="Nom:").grid(row=2, column=0, padx=5, pady=5)
        self.modify_name_entry = tk.Entry(self.modify_tab, state='readonly')
        self.modify_name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.modify_tab, text="Compétitions:").grid(row=3, column=0, padx=5, pady=5)
        self.modify_competition_vars = {comp: tk.BooleanVar() for comp in ["Coupe du monde", "Copa America", "Ligue des Champions", "Euro", "Ligue 1", "Liga", "Serie A","Premier League","Bundesliga"]}
        for i, comp in enumerate(self.modify_competition_vars):
            tk.Checkbutton(self.modify_tab, text=comp, variable=self.modify_competition_vars[comp]).grid(row=3+i//3, column=1+i%3, sticky="w")

        tk.Label(self.modify_tab, text="Clubs:").grid(row=7, column=0, padx=5, pady=5)
        self.modify_club_vars = {club: tk.BooleanVar() for club in ["Real Madrid", "PSG", "Barcelone", "Liverpool", "Juventus", "AC Milan", "Chelsea", "Manchester United",
                                                                    "Manchester City", "Bayern Munich", "Arsenal", "Monaco", "Borussia Dortmund", "Atletico Madrid",
                                                                    "Inter Milan","Benfica","Porto","Ajax"]}
        for i, club in enumerate(self.modify_club_vars):
            tk.Checkbutton(self.modify_tab, text=club, variable=self.modify_club_vars[club]).grid(row=7+i//3, column=1+i%3, sticky="w")

        tk.Label(self.modify_tab, text="Nombre de matchs:").grid(row=13, column=0, padx=5, pady=5)
        self.modify_matches_entry = tk.Entry(self.modify_tab)
        self.modify_matches_entry.grid(row=13, column=1, padx=5, pady=5)

        tk.Label(self.modify_tab, text="Nombre de buts:").grid(row=14, column=0, padx=5, pady=5)
        self.modify_goals_entry = tk.Entry(self.modify_tab)
        self.modify_goals_entry.grid(row=14, column=1, padx=5, pady=5)

        self.modify_button = tk.Button(self.modify_tab, text="Modifier", command=self.modify_player)
        self.modify_button.grid(row=15, column=0, columnspan=3, pady=10)

    def add_player(self):
        name = self.add_name_entry.get()
        nationality = self.add_nationality_var.get()
        competitions = [comp for comp, var in self.add_competition_vars.items() if var.get()]
        clubs = [club for club, var in self.add_club_vars.items() if var.get()]
        matches = int(self.add_matches_entry.get())
        goals = int(self.add_goals_entry.get())

        # Ajouter le joueur au dictionnaire
        players_db.players_db[name] = {
            "country": nationality,
            "competitions": competitions,
            "clubs": clubs,
            "matches": matches,
            "goals": goals
        }

        # Sauvegarder les changements
        self.save_players_db()

        # Afficher une alerte
        messagebox.showinfo("Succès", f"Le joueur {name} a été ajouté avec succès!")

        # Réinitialiser les champs du formulaire
        self.reset_add_form()

    def save_players_db(self):
        with open("players_db.py", "w") as f:
            f.write("players_db = ")
            json.dump(players_db.players_db, f, indent=4)

    def reset_add_form(self):
        self.add_name_entry.delete(0, "end")
        self.add_nationality_var.set("")
        for var in self.add_competition_vars.values():
            var.set(False)
        for var in self.add_club_vars.values():
            var.set(False)
        self.add_matches_entry.delete(0, "end")
        self.add_goals_entry.delete(0, "end")

    def update_player_list(self, _):
        nationality = self.modify_nationality_var.get()
        players = [player for player in players_db.players_db if players_db.players_db[player]["country"] == nationality]
        self.player_var.set(players[0] if players else "")
        menu = self.player_menu["values"] = players

        if players:
            self.prefill_player_info(players[0])
        else:
            self.reset_modify_form()

    def on_player_selected(self, player_name):
        if player_name:
            self.prefill_player_info(player_name)

    def prefill_player_info(self, player_name):
        if player_name in players_db.players_db:
            player_info = players_db.players_db[player_name]
            # Pré-remplir les champs avec les informations du joueur
            self.modify_name_entry.config(state='normal')
            self.modify_name_entry.delete(0, "end")
            self.modify_name_entry.insert(0, player_name)
            self.modify_name_entry.config(state='readonly')
            
            # Pré-remplir les cases à cocher des compétitions
            for competition, var in self.modify_competition_vars.items():
                var.set(competition in player_info["competitions"])
            
            # Pré-remplir les cases à cocher des clubs
            for club, var in self.modify_club_vars.items():
                var.set(club in player_info["clubs"])
            
            # Pré-remplir les entrées pour le nombre de matchs et de buts
            self.modify_matches_entry.delete(0, "end")
            self.modify_matches_entry.insert(0, str(player_info.get("matches", "")))
            self.modify_goals_entry.delete(0, "end")
            self.modify_goals_entry.insert(0, str(player_info.get("goals", "")))
        else:
            # Réinitialiser les champs si le joueur n'est pas trouvé
            self.reset_modify_form()

    def modify_player(self):
        name = self.player_var.get()
        competitions = [comp for comp, var in self.modify_competition_vars.items() if var.get()]
        clubs = [club for club, var in self.modify_club_vars.items() if var.get()]
        matches = int(self.modify_matches_entry.get())
        goals = int(self.modify_goals_entry.get())

        # Mettre à jour le joueur dans le dictionnaire
        if name in players_db.players_db:
            players_db.players_db[name]["competitions"] = competitions
            players_db.players_db[name]["clubs"] = clubs
            players_db.players_db[name]["matches"] = matches
            players_db.players_db[name]["goals"] = goals

            # Sauvegarder les changements
            self.save_players_db()

            # Afficher une alerte
            messagebox.showinfo("Succès", f"Le joueur {name} a été modifié avec succès!")

            # Réinitialiser les champs du formulaire
            self.reset_modify_form()

    def reset_modify_form(self):
        self.modify_name_entry.delete(0, "end")
        self.modify_nationality_var.set("")
        for var in self.modify_competition_vars.values():
            var.set(False)
        for var in self.modify_club_vars.values():
            var.set(False)
        self.modify_matches_entry.delete(0, "end")
        self.modify_goals_entry.delete(0, "end")

def main():
    root = tk.Tk()
    app = PlayerManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()


