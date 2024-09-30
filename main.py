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
largeur_fenetre, hauteur_fenetre = 1024, 720
cree_fenetre(largeur_fenetre, hauteur_fenetre)

def dessine_quadrillage(hauteur_ligne, largeur_colonne):
    for i in range(1, 8):
        y = i * hauteur_ligne
        ligne(0, y, largeur_fenetre, y)

    for i in range(1, 8):
        x = i * largeur_colonne
        ligne(x, 0, x, hauteur_fenetre)

# Appel de la fonction avec les bonnes dimensions
dessine_quadrillage(hauteur_fenetre // 8, largeur_fenetre // 8)

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
