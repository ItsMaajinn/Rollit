import string
from fltk import *

# Liste pour stocker les positions des boules (images) à afficher
boules = []

# Dictionnaire global pour stocker les cases par leur nom
case_dict = {}

def createGrid():
    """
    Crée une grille de coordonnées et remplit un dictionnaire global pour un accès rapide.
    Chaque entrée est un tuple contenant le nom de la case et ses coordonnées.
    :return: grille (liste de listes de tuples)
    """
    grid = []
    for i in range(8):  # Pour les rangées de A à H
        row = []
        for j in range(8):  # Pour les colonnes de 1 à 8
            col = chr(ord('A') + j)  # Ajuster pour A à H
            row_num = 8 - i  # Ajuster pour 8 à 1
            x1 = marge_gauche_droite + j * taille_case
            y1 = (marge_supplementaire // 2) + i * taille_case
            x2 = x1 + taille_case
            y2 = y1 + taille_case
            cell_name = f"{col}{row_num}"
            cell_info = [cell_name, (x1, y1, x2, y2)]
            row.append(cell_info)
            # Ajouter au dictionnaire
            case_dict[cell_name] = {
                "nom": cell_name,
                "coordonnees": (x1, y1, x2, y2),
                "completion": None,
                "cote": None
            }
        grid.append(row)
    return grid


def coordToCase(tab, ev):
    # Récupère les coordonnées x et y de l'événement
    x, y = abscisse(ev), ordonnee(ev)
    # Vérifie si les coordonnées x et y sont dans les limites de la grille
    if marge_gauche_droite <= x <= (marge_gauche_droite + taille_case * 8) and (marge_supplementaire // 2) <= y <= (marge_supplementaire // 2 + taille_case * 8):
        # Calcule la colonne en fonction de la position x
        col = (x - marge_gauche_droite) // taille_case
        # Calcule la ligne en fonction de la position y
        row = (y - (marge_supplementaire // 2)) // taille_case
        # Retourne le nom de la case correspondante
        return tab[row][col][0]

    # Retourne None si les coordonnées ne sont pas dans les limites de la grille
    return None


def caseToCoord(var, tab):
    for i in range(8):
        for j in range(8):
            if tab[i][j][0] == var:
                return tab[i][j][1]
    return None


def get_case(nameCase):
    """
    Retourne les informations d'une case à partir du dictionnaire global.

    :param nameCase: Le nom de la case (ex: "A1")
    :return: Un dictionnaire contenant les informations de la case, ou None si elle n'existe pas
    """
    return case_dict.get(nameCase)

def poserBoule(cell_coords, image_path):
    """
    Ajoute une boule (image) à la liste des boules à poser.
    L'image sera dessinée au centre de la case.
    :param cell_coords: Tuple des coordonnées (x1, y1, x2, y2) de la case
    :param image_path: Chemin vers l'image à afficher
    """
    x1, y1, x2, y2 = cell_coords
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    boules.append((center_x, center_y, image_path))

def dessineBoules():
    """
    Dessine toutes les boules stockées dans la liste boules.
    """
    for boule in boules:
        x, y, path = boule
        image(x, y, path, largeur=taille_case, hauteur=taille_case, ancrage="center")
        get_case(coordToCase(grid, ev))["completion"] = path

def dessine_quadrillage():
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
    dessineBoules()

def dessineInitiales():
    imgRouge = "assets/Ruby.png"
    # Exemple d'images initiales, si nécessaire
    # poserBoule(caseToCoord("C5", grid), imgRouge)
    # poserBoule(caseToCoord("D4", grid), imgRouge)
    # Décommentez les lignes ci-dessus si vous souhaitez placer des boules initiales

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

# Création de la grille
grid = createGrid()

def redraw():
    efface_tout()
    dessine_quadrillage()
    dessineInitiales()  # Si vous avez des boules initiales à dessiner
    mise_a_jour()

# Initial dessin
redraw()

def gerer_evenement_clic_gauche(ev):
    cell_name = coordToCase(grid, ev)
    if cell_name:
        cell_coords = caseToCoord(cell_name, grid)
        print(f"{get_case(cell_name)}")
        print(f"Clic gauche sur la case {cell_name} avec coordonnées {cell_coords}")
        # Définir le chemin de l'image à poser, vous pouvez le modifier selon vos besoins
        chemin_image = "assets/pionBleu.png"  # Remplacez par le chemin de votre image
        poserBoule(cell_coords, chemin_image)
        redraw()
    else:
        print("Clic gauche en dehors de la grille.")
    print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))

# Boucle principale
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == 'Touche':
        print('Appui sur la touche', touche(ev))
    elif tev == "ClicDroit":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))
    elif tev == "ClicGauche":
        gerer_evenement_clic_gauche(ev)
    elif tev == 'Quitte':  # on sort de la boucle
        break
    else:  # dans les autres cas, on ne fait rien
        pass

    # Mise à jour de la fenêtre
    mise_a_jour()

ferme_fenetre()
