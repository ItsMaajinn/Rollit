import string
from fltk import *

alphabetMaj = string.ascii_uppercase

def makeDict():
    dict = {}
    for i in range(8):
        for j in range(1, 9):
            dict[alphabetMaj[i] + str(j)] = "N"
    return dict

# Création de la fenêtre
largeur_fenetre, hauteur_fenetre = 1280, 720
cree_fenetre(largeur_fenetre, hauteur_fenetre)

# Taille du quadrillage (8x8)
taille_grille = 8

# Calcule la taille de chaque case pour que le quadrillage soit un carré centré
taille_case = min(hauteur_fenetre, largeur_fenetre) / taille_grille

# Calcule l'espace à gauche et à droite pour centrer le quadrillage horizontalement
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) / 2

# Calcule l'espace en haut et en bas pour centrer le quadrillage verticalement
marge_haut_bas = (hauteur_fenetre - (taille_case * taille_grille)) / 2

def dessine_quadrillage():
    # Dessine les lignes horizontales
    for i in range(taille_grille + 1):
        y = marge_haut_bas + i * taille_case
        ligne(marge_gauche_droite, y, largeur_fenetre - marge_gauche_droite, y)

    # Dessine les lignes verticales
    for i in range(taille_grille + 1):
        x = marge_gauche_droite + i * taille_case
        ligne(x, marge_haut_bas, x, hauteur_fenetre - marge_haut_bas)

# Appel de la fonction pour dessiner le quadrillage centré
dessine_quadrillage()

# Attente d'un événement pour fermer la fenêtre
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    # Action dépendant du type d'événement reçu :

    if tev == 'Touche':
        print('Appui sur la touche', touche(ev))

    elif tev == "ClicDroit":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))

    elif tev == "ClicGauche":
        print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))

    elif tev == 'Quitte':  # on sort de la boucle
        break

    else:  # dans les autres cas, on ne fait rien
        pass

    mise_a_jour()

ferme_fenetre()
