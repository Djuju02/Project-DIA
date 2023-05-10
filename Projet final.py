import copy
# Couleurs ANSI pour la sortie du terminal
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Classe représentant un seul morpion (tic-tac-toe)
class Morpion:
    def __init__(self):
        # Initialise une grille de morpion vide
        self.grille = [['.' for _ in range(3)] for _ in range(3)]

    def jouer(self, x, y, joueur_actuel):
        # Effectue un coup si la cellule est vide et retourner True, sinon retourner False
        if self.grille[x][y] == '.':
            self.grille[x][y] = joueur_actuel
            return True
        return False

    def gagnant(self):
        # Vérifie si un joueur a gagné dans ce morpion et retourne le symbole du joueur gagnant, sinon retourne None
        for i in range(3):
            if self.grille[i][0] == self.grille[i][1] == self.grille[i][2] != '.':
                return self.grille[i][0]
            if self.grille[0][i] == self.grille[1][i] == self.grille[2][i] != '.':
                return self.grille[0][i]
        if self.grille[0][0] == self.grille[1][1] == self.grille[2][2] != '.':
            return self.grille[0][0]
        if self.grille[0][2] == self.grille[1][1] == self.grille[2][0] != '.':
            return self.grille[0][2]
        return None

    def __str__(self):
        # Représentation sous forme de chaîne de caractères pour l'affichage
        return "\n".join(" ".join(row) for row in self.grille)

    def coups_disponibles(self):
        # Renvoie la liste des cellules vides (coups disponibles) sous forme de tuples (x, y)
        coups = []
        for x in range(3):
            for y in range(3):
                if self.grille[x][y] == '.':
                    coups.append((x, y))
        return coups
    
    def complet(self):
        # Retourne True si le morpion est complet (aucune cellule vide), sinon retourne False
        for x in range(3):
            for y in range(3):
                if self.grille[x][y] == '.':
                    return False
        return True


# Classe représentant tout le morpion (tic-tac-toe)
class UltimateTicTacToe:
    def __init__(self):
        self.plateau = [[Morpion() for _ in range(3)] for _ in range(3)]
        self.position_dernier_coup = None
        self.joueur_actuel = 'X'

    def jouer(self, morpion_x, morpion_y, x, y):
        # Effectue un coup dans un morpion particulier en fonction des coordonnées morpion_x, morpion_y et x, y
        # Retourne True si le coup a été joué avec succès, sinon retourne False
        if self.position_dernier_coup is None or self.plateau[morpion_x][morpion_y].gagnant() is not None or self.plateau[morpion_x][morpion_y].complet():
            morpion = self.plateau[morpion_x][morpion_y]
            if morpion.jouer(x, y, self.joueur_actuel):
                self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'
                self.position_dernier_coup = (x, y)
                return True
        else:
            morpion = self.plateau[morpion_x][morpion_y]
            if morpion.jouer(x, y, self.joueur_actuel):
                self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'
                self.position_dernier_coup = (x, y)
                return True
        return False

    # Le reste du code reste inchangé

    def gagnant(self):
        # Vérifie si un joueur a gagné l'Ultimate Tic Tac Toe et retourne le symbole du joueur gagnant, sinon retourne None
        morpions_gagnants = [[morpion.gagnant() for morpion in row] for row in self.plateau]

        for i in range(3):
            if morpions_gagnants[i][0] == morpions_gagnants[i][1] == morpions_gagnants[i][2] != None:
                return morpions_gagnants[i][0]
            if morpions_gagnants[0][i] == morpions_gagnants[1][i] == morpions_gagnants[2][i] != None:
                return morpions_gagnants[0][i]
        if morpions_gagnants[0][0] == morpions_gagnants[1][1] == morpions_gagnants[2][2] != None:
            return morpions_gagnants[0][0]
        if morpions_gagnants[0][2] == morpions_gagnants[1][1] == morpions_gagnants[2][0] != None:
            return morpions_gagnants[0][2]
        return None

    def __str__(self):
        # Représentation sous forme de chaîne de caractères pour l'affichage
        rows = []
        for i in range(3):
            for j in range(3):
                row = " | ".join(" ".join(self.plateau[i][k].grille[j]) for k in range(3))
                rows.append(row)
            if i != 2:
                rows.append("." * 23)
        return "\n".join(rows)


    def match_nul(self):
        # Vérifie si le match est nul, c'est-à-dire si tous les morpions sont terminés sans gagnant
        # Retourne True si c'est un match nul, sinon retourne False
        for row in self.plateau:
            for morpion in row:
                if morpion.gagnant() is None:
                    return False
        return True

    def coups_disponibles(self):
        # Retourne une liste des coups disponibles dans le morpion actuel
        # Chaque coup est représenté par un tuple (x, y) correspondant à la position de la case vide
        coups = []
        for x in range(3):
            for y in range(3):
                if self.grille[x][y] == '.':
                    coups.append((x, y))
        return coups


class MinMaxIA:
    def __init__(self, profondeur_max):
        self.profondeur_max = profondeur_max

    def meilleur_coup(self, ultimate_tic_tac_toe, joueur):
        max_eval = float('-inf')
        meilleur_coup = None

        for coup in self.coups_possibles(ultimate_tic_tac_toe):
            ultimate_tic_tac_toe_copie = copy.deepcopy(ultimate_tic_tac_toe)
            ultimate_tic_tac_toe_copie.jouer(*coup)
            eval_coup = self.minimax(ultimate_tic_tac_toe_copie, 0, float('-inf'), float('inf'), False, joueur)
            if eval_coup > max_eval:
                max_eval = eval_coup
                meilleur_coup = coup

        return meilleur_coup

    def minimax(self, ultimate_tic_tac_toe, profondeur, alpha, beta, maximising_player, joueur):
        if profondeur == self.profondeur_max or ultimate_tic_tac_toe.gagnant() is not None or ultimate_tic_tac_toe.match_nul():
            return self.evaluation(ultimate_tic_tac_toe, joueur)

        if maximising_player:
            max_eval = float('-inf')
            for coup in self.coups_possibles(ultimate_tic_tac_toe):
                ultimate_tic_tac_toe_copie = copy.deepcopy(ultimate_tic_tac_toe)
                ultimate_tic_tac_toe_copie.jouer(*coup)
                eval_coup = self.minimax(ultimate_tic_tac_toe_copie, profondeur + 1, alpha, beta, False, joueur)
                max_eval = max(max_eval, eval_coup)
                alpha = max(alpha, eval_coup)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for coup in self.coups_possibles(ultimate_tic_tac_toe):
                ultimate_tic_tac_toe_copie = copy.deepcopy(ultimate_tic_tac_toe)
                ultimate_tic_tac_toe_copie.jouer(*coup)
                eval_coup = self.minimax(ultimate_tic_tac_toe_copie, profondeur + 1, alpha, beta, True, joueur)
                min_eval = min(min_eval, eval_coup)
                beta = min(beta, eval_coup)
                if beta <= alpha:
                    break
            return min_eval

    def evaluation(self, ultimate_tic_tac_toe, joueur):
        gagnant = ultimate_tic_tac_toe.gagnant()
        if gagnant is None:
            return 0
        elif gagnant == joueur:
            return 1
        else:
            return -1

    def coups_possibles(self, ultimate_tic_tac_toe):
        if ultimate_tic_tac_toe.position_dernier_coup is None:
            morpion_x, morpion_y = 1, 1
        else:
            morpion_x, morpion_y = ultimate_tic_tac_toe.position_dernier_coup

        morpion = ultimate_tic_tac_toe.plateau[morpion_x][morpion_y]
        coups_morpion = morpion.coups_disponibles()

        # Ajouter les coordonnées du morpion aux coups possibles
        coups_complets = [(morpion_x, morpion_y, x, y) for x, y in coups_morpion]
        return coups_complets



def main():
    ultimate_tic_tac_toe = UltimateTicTacToe()
    ia = MinMaxIA(profondeur_max=3)  # Vous pouvez ajuster la profondeur_max pour modifier la difficulté de l'IA

    print("Ultimate Tic Tac Toe\n")
    print("Qui commence ?")
    print("1. Joueur (X)")
    print("2. IA (O)")

    choix = int(input("Entrez le numéro correspondant à votre choix : "))

    while ultimate_tic_tac_toe.gagnant() is None and not ultimate_tic_tac_toe.match_nul():
        color = RED if ultimate_tic_tac_toe.joueur_actuel == "X" else BLUE
        print(color + str(ultimate_tic_tac_toe) + RESET)

        libre_de_choisir_grande_case = ultimate_tic_tac_toe.position_dernier_coup is None or ultimate_tic_tac_toe.plateau[ultimate_tic_tac_toe.position_dernier_coup[0]][ultimate_tic_tac_toe.position_dernier_coup[1]].gagnant() is not None or ultimate_tic_tac_toe.plateau[ultimate_tic_tac_toe.position_dernier_coup[0]][ultimate_tic_tac_toe.position_dernier_coup[1]].complet()

        if libre_de_choisir_grande_case:
            print(f"{color}Vous pouvez choisir une grande case.{RESET}")
        else:
            print(f"{color}Vous devez jouer dans la grande case ({ultimate_tic_tac_toe.position_dernier_coup[0]}, {ultimate_tic_tac_toe.position_dernier_coup[1]}).{RESET}")

        if (choix == 1 and ultimate_tic_tac_toe.joueur_actuel == 'X') or (choix == 2 and ultimate_tic_tac_toe.joueur_actuel == 'O'):
            while True:
                try:
                    if libre_de_choisir_grande_case:
                        morpion_x, morpion_y = map(int, input(f"{color}Joueur {ultimate_tic_tac_toe.joueur_actuel}, entrez les coordonnées de la grande case (Morpion x, Morpion y) : {RESET}").split())
                    else:
                        morpion_x, morpion_y = ultimate_tic_tac_toe.position_dernier_coup

                    x, y = map(int, input(f"{color}Joueur {ultimate_tic_tac_toe.joueur_actuel}, entrez les coordonnées de la petite case (x, y) : {RESET}").split())

                    if 0 <= morpion_x <= 2 and 0 <= morpion_y <= 2 and 0 <= x <= 2 and 0 <= y <= 2:
                        if ultimate_tic_tac_toe.jouer(morpion_x, morpion_y, x, y):
                            break
                        else:
                            print("Coup invalide, veuillez réessayer.")
                    else:
                        print("Veuillez entrer des coordonnées valides (Morpion x, Morpion y, x, y) comprises entre 0 et 2.")
                except ValueError:
                    print("Veuillez entrer des coordonnées valides (Morpion x, Morpion y, x, y) comprises entre 0 et 2.")
        else:
            coup_ia = ia.meilleur_coup(ultimate_tic_tac_toe, ultimate_tic_tac_toe.joueur_actuel)
            ultimate_tic_tac_toe.jouer(coup_ia[0], coup_ia[1], coup_ia[2], coup_ia[3])
            print(f"{color}L'IA joue en ({coup_ia[0]}, {coup_ia[1]}) dans la grande case, et en ({coup_ia[2]}, {coup_ia[3]}) dans la petite case.{RESET}")

    print(color + str(ultimate_tic_tac_toe) + RESET)
    if ultimate_tic_tac_toe.gagnant() is not None:
        print(f"{color}Le joueur {ultimate_tic_tac_toe.gagnant()} gagne la partie !{RESET}")
    else:
        print("Match nul !")

if __name__ == "__main__":
    main()