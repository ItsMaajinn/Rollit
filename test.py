from fltk import *

boules = []

constanteColor = 0


marge_supplementaire = 4  # Marge supplémentaire pour le haut et le bas

largeur_fenetre, hauteur_fenetre = 1280, 720 + marge_supplementaire  # Augmenter la hauteur de la fenêtre de 4 pixels

cree_fenetre(largeur_fenetre, hauteur_fenetre)

def dessine_quadrillage(taille_grille, taille_case, marge_gauche_droite):
    # Dessine les lignes horizontales (exactement 9 lignes pour 8 cases)
    for i in range(taille_grille + 1):
        y = i * taille_case + (marge_supplementaire // 2)  # Ajouter la marge supplémentaire en haut
        if y <= hauteur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(marge_gauche_droite, y, marge_gauche_droite + taille_case * taille_grille, y)
    # Dessine les lignes verticales (exactement 9 colonnes pour 8 cases)
    for i in range(taille_grille + 1):
        x = marge_gauche_droite + i * taille_case
        if x <= largeur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(x, (marge_supplementaire // 2), x, (taille_case * taille_grille) + (marge_supplementaire // 2))

    # Dessine toutes les boules
def createGrid(marge_gauche_droite, taille_case):
    """
    Crée une grille de coordonnées et remplit un dictionnaire global pour un accès rapide.
    Chaque entrée est un tuple contenant le nom de la case et ses coordonnées.
    :return: grille (liste de listes de tuples)
    """
    grid = []
    for i in range(8):  # Pour les rangées de A à H
        row = []
        for j in range(8):  # Pour les colonnes de 1 à 8
            x1 = marge_gauche_droite + j * taille_case
            y1 = (marge_supplementaire // 2) + i * taille_case
            x2 = x1 + taille_case
            y2 = y1 + taille_case
            row.append([(x1, y1, x2, y2), None])

        grid.append(row)
    return grid


def coordToCase(grid, ev):
    # Récupère les coordonnées x et y de l'événement
    x, y = abscisse(ev), ordonnee(ev)
    # Vérifie si les coordonnées x et y sont dans les limites de la grille
    if marge_gauche_droite <= x <= (marge_gauche_droite + taille_case * 8) and (marge_supplementaire // 2) <= y <= (marge_supplementaire // 2 + taille_case * 8):
        # Calcule la colonne en fonction de la position x
        col = (x - marge_gauche_droite) // taille_case
        # Calcule la ligne en fonction de la position y
        row = (y - (marge_supplementaire // 2)) // taille_case
        # Retourne le nom de la case correspondante
        return grid[row][col][0]


def getCase(grid, coordRel, taille_case, marge_gauche_droite):
    """
    Renvoie la case (coordonnées de la case et son état) à partir des coordonnées relatives en utilisant des calculs directs.
    :param grid: la grille contenant les informations des cases
    :param coordRel: tuple (x, y) contenant les coordonnées de l'événement
    :param taille_case: la taille d'une case de la grille
    :param marge_gauche_droite: la marge à gauche/droite de la grille
    :return: tuple (coordonnées de la case, état de la case) ou None si hors de la grille
    """
    x, y = coordRel  # Décompose les coordonnées

    # Vérifie si les coordonnées sont dans les limites de la grille
    if not (marge_gauche_droite <= x < marge_gauche_droite + taille_case * 8 and
            marge_supplementaire // 2 <= y < (marge_supplementaire // 2) + taille_case * 8):
        return None

    # Calcule l'index de la colonne et de la ligne
    col = (x - marge_gauche_droite) // taille_case
    row = (y - (marge_supplementaire // 2)) // taille_case

    return grid[row][col]  # Retourne la case correspondante





def placerBoule(grid, taille_case, marge_gauche_droite, cell_coords, image_path, cell):
    x1, y1, x2, y2 = cell_coords
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    if cell:
        cell[1] = image_path
        image(center_x, center_y, image_path, largeur=taille_case, hauteur=taille_case, ancrage="center")



def changeColor(path1, path2, path3, path4):
    global constanteColor  # Utilise la variable globale i

    # Alterne entre 4 couleurs en fonction de la valeur de i
    if constanteColor % 4 == 0:
        path = path1  # Pion Bleu
    elif constanteColor % 4 == 1:
        path = path2  # Pion Rouge
    elif constanteColor % 4 == 2:
        path = path3  # Pion Jaune
    else:
        path = path4  # Pion Vert

    constanteColor += 1  # Incrémente i après chaque appel
    return path

def bouleNextTo(grid, coordRel, taille_case, marge_gauche_droite):
    x, y = coordRel  # Decompose the coordinates
    possibilities = [
        (x - taille_case, y), (x + taille_case, y),
        (x, y - taille_case), (x, y + taille_case),
        (x - taille_case, y - taille_case), (x + taille_case, y - taille_case),
        (x - taille_case, y + taille_case), (x + taille_case, y + taille_case)
    ]
    for i in possibilities:
        case = getCase(grid, i, taille_case, marge_gauche_droite)
        if case is not None and case[1] is not None:
            return True
    return False






"""def gerer_evenement_clic_gauche(ev):
    cell_coord = coordToCase(grid, ev)
    if cell_coord:
        """




# Var et main

# Taille du quadrillage (8x8)
taille_grille = 8

# On réduit légèrement la taille des cases pour éviter les débordements
taille_case = (hauteur_fenetre - marge_supplementaire) // taille_grille

# Calcule l'espace à gauche pour centrer le quadrillage horizontalement
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2

grid = createGrid(marge_gauche_droite, taille_case)
dessine_quadrillage(taille_grille, taille_case, marge_gauche_droite)
center_row, center_col = taille_grille // 2, taille_grille // 2
center_coords = grid[center_row][center_col][0]

center_path = changeColor("assets/pionBleu.png", "assets/pionRouge.png", "assets/pionJaune.png", "assets/pionVert.png")
placerBoule(grid, taille_case, marge_gauche_droite, center_coords, center_path, grid[center_row][center_col])


while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == 'Quitte':  # on sort de la boucle
        break
    elif tev == 'ClicGauche':
        case = getCase(grid, (abscisse(ev), ordonnee(ev)), taille_case, marge_gauche_droite)
        if case and case[1] == None:  # Vérifie si la case est valide
            if bouleNextTo(grid, (abscisse(ev), ordonnee(ev)), taille_case, marge_gauche_droite):
                path = changeColor("assets/pionBleu.png", "assets/pionRouge.png", "assets/pionJaune.png", "assets/pionVert.png")
                placerBoule(grid, taille_case, marge_gauche_droite, case[0], path, case)
    mise_a_jour()
