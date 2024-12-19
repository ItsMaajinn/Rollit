# Initialiser le plateau (vide au départ)
plateau = [
    [' ' for _ in range(8)] for _ in range(8)
]

# Afficher le plateau de manière lisible
def afficher_plateau(plateau):
    for ligne in plateau:
        print('|'.join(ligne))
        print('-' * 15)

# Vérifier si un joueur a gagné
def verifier_vainqueur(plateau, joueur):
    # Vérifier lignes, colonnes et diagonales
    for i in range(8):
        if all(plateau[i][j] == joueur for j in range(8)):  # Lignes
            return True
        if all(plateau[j][i] == joueur for j in range(8)):  # Colonnes
            return True
    # Diagonales
    if all(plateau[i][i] == joueur for i in range(8)):
        return True
    if all(plateau[i][7 - i] == joueur for i in range(8)):
        return True
    return False

# Vérifier si le plateau est plein (égalité)
def est_plein(plateau):
    return all(plateau[i][j] != ' ' for i in range(8) for j in range(8))

# Fonction Minimax : explore tous les coups possibles pour déterminer le meilleur score
# Fonction Minimax avec élagage alpha-bêta
def minimax(plateau, profondeur, est_maximisation, profondeur_max, alpha, beta):
    # Cas de base : État terminal ou profondeur maximale atteinte
    if verifier_vainqueur(plateau, 'O'):  # O est l'IA
        return 10 - profondeur
    if verifier_vainqueur(plateau, 'X'):  # X est le joueur humain
        return profondeur - 10
    if est_plein(plateau) or profondeur == profondeur_max:
        return 0

    if est_maximisation:  # Tour de l'IA
        meilleur_score = -float('inf')
        for i in range(8):
            for j in range(8):
                if plateau[i][j] == ' ':
                    plateau[i][j] = 'O'
                    score = minimax(plateau, profondeur + 1, False, profondeur_max, alpha, beta)
                    plateau[i][j] = ' '
                    meilleur_score = max(meilleur_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return meilleur_score
    else:  # Tour du joueur humain
        meilleur_score = float('inf')
        for i in range(8):
            for j in range(8):
                if plateau[i][j] == ' ':
                    plateau[i][j] = 'X'
                    score = minimax(plateau, profondeur + 1, True, profondeur_max, alpha, beta)
                    plateau[i][j] = ' '
                    meilleur_score = min(meilleur_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return meilleur_score

# Trouver le meilleur coup pour l'IA
def meilleur_coup(plateau, profondeur_max):
    meilleur_score = -float('inf')
    coup = None
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == ' ':
                plateau[i][j] = 'O'
                score = minimax(plateau, 0, False, profondeur_max, -float('inf'), float('inf'))
                plateau[i][j] = ' '
                if score > meilleur_score:
                    meilleur_score = score
                    coup = (i, j)
    return coup

# Fonction principale pour jouer au Tic-Tac-Toe
def jouer():
    joueur = 'X'  # Le joueur humain commence
    profondeur_max = 3  # Définir la profondeur maximale ici
    while True:
        afficher_plateau(plateau)

        # Vérifier les états de fin
        if verifier_vainqueur(plateau, 'X'):
            print("Vous avez gagné !")
            break
        if verifier_vainqueur(plateau, 'O'):
            print("L'IA a gagné !")
            break
        if est_plein(plateau):
            print("Match nul !")
            break

        if joueur == 'X':  # Tour du joueur humain
            while True:
                try:
                    ligne, col = map(int, input("Entrez votre coup (ligne et colonne) : ").split())
                    if plateau[ligne][col] == ' ':
                        plateau[ligne][col] = 'X'
                        joueur = 'O'
                        break
                    else:
                        print("Case occupée !")
                except ValueError:
                    print("Veuillez entrer deux valeurs entières séparées par un espace.")
                except IndexError:
                    print("Veuillez entrer des valeurs entre 0 et 7.")
        else:  # Tour de l'IA
            print("L'IA joue...")
            ligne, col = meilleur_coup(plateau, profondeur_max)
            plateau[ligne][col] = 'O'
            joueur = 'X'

# Lancer le jeu
jouer()