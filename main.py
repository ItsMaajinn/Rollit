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

# On réduit légèrement la taille des cases pour éviter les débordements
taille_case = (hauteur_fenetre) // taille_grille

# Calcule l'espace à gauche pour centrer le quadrillage horizontalement
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2

def dessine_quadrillage():
    # Dessine les lignes horizontales (exactement 8 lignes)
    for i in range(taille_grille + 1):
        y = i * taille_case
        if y <= hauteur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(marge_gauche_droite, y, largeur_fenetre - marge_gauche_droite, y)

    # Dessine les lignes verticales (exactement 8 colonnes)
    for i in range(taille_grille + 1):
        x = marge_gauche_droite + i * taille_case
        if x <= largeur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(x, 0, x, taille_case * taille_grille)  # Utilise juste la hauteur nécessaire pour le quadrillage

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