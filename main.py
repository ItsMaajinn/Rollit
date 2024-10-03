import string
from fltk import *


def createGrid():
    """
    Crée une grille de coordonnées sous forme de liste de listes.
    Chaque entrée est un tuple contenant le nom de la case et ses coordonnées.
    :return: grille (liste de listes de tuples)
    """
    grid = []
    for i in range(8):  # Pour les rangées de A à H
        row = []
        for j in range(8):  # Pour les colonnes de 1 à 8
            col = chr(ord('A') + j)  # Ajuster pour A à droite
            row_num = 8 - i  # Ajuster pour 8 à 1
            x1 = 280 + j * 90
            y1 = i * 90
            x2 = x1 + 90
            y2 = y1 + 90
            cell_name = f"{col}{row_num}"
            row.append([cell_name, (x1, y1, x2, y2)])
        grid.append(row)
    return grid


def coordToCase(tab, ev):
    x, y = abscisse(ev), ordonnee(ev)
    if 280 <= x <= 1000 and 0 <= y <= 720:
        for i in range(8):
            for j in range(8):
                cell_name, (x1, y1, x2, y2) = tab[i][j]
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return cell_name


def caseToCoord(var, tab):
    for i in range(8):
        for j in range(8):
            if tab[i][j][0] == var:
                return tab[i][j][1]


def poserBoule():
    imgRouge = "assets/Ruby.png"
    image(322, 45, imgRouge, largeur=90, hauteur=90, ancrage="center")  # Placer l'image en haut
    image(412, 135, imgRouge, largeur=90, hauteur=90, ancrage="center")
    # pour x => ((x1+x2))//2)-3
    # pour y => (y1+y2)//2

# Création de la fenêtre
marge_supplementaire = 4  # Marge supplémentaire pour le haut et le bas
largeur_fenetre, hauteur_fenetre = 1280, 720 + marge_supplementaire  # Augmenter la hauteur de la fenêtre de 4 pixels
cree_fenetre(largeur_fenetre, hauteur_fenetre)

# Taille du quadrillage (8x8)
taille_grille = 8

# On réduit légèrement la taille des cases pour éviter les débordements
taille_case = (hauteur_fenetre - marge_supplementaire) // taille_grille

# Calcule l'espace à gauche pour centrer le quadrillage horizontalement
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2


def dessine_quadrillage():
    # Dessine les lignes horizontales (exactement 8 lignes)
    for i in range(taille_grille + 1):
        y = i * taille_case + (marge_supplementaire // 2)  # Ajouter la marge supplémentaire en haut
        if y <= hauteur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(marge_gauche_droite, y, largeur_fenetre - marge_gauche_droite, y)
    # Dessine les lignes verticales (exactement 8 colonnes)
    for i in range(taille_grille + 1):
        x = marge_gauche_droite + i * taille_case
        if x <= largeur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(x, (marge_supplementaire // 2), x, (taille_case * taille_grille) + (
                        marge_supplementaire // 2))  # Utilise juste la hauteur nécessaire pour le quadrillage


# Appel de la fonction pour dessiner le quadrillage centré
dessine_quadrillage()
poserBoule()

# Utilisation de la nouvelle fonction

# Attente d'un événement pour fermer la fenêtre
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == 'Touche':
        print('Appui sur la touche', touche(ev))
    elif tev == "ClicDroit":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))
    elif tev == "ClicGauche":
        grid = createGrid()
        cell_name = coordToCase(grid, ev)
        print(cell_name)
        print(caseToCoord(cell_name, grid))
        print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))
    elif tev == 'Quitte':  # on sort de la boucle
        break
    else:  # dans les autres cas, on ne fait rien
        pass

    mise_a_jour()

ferme_fenetre()
